"""
T5.3 — the single place where configuration and prepared data are read.

Every other module gets its numbers from here. Nothing downstream opens
config.yaml or a CSV itself, and nothing downstream contains a literal that
also appears in config.yaml. That is what makes T7.6b (fatigue-rate
sensitivity) and T7.8 (coupling ablation) possible later: those studies work
by editing the configuration, so any value baked into code is a value they
cannot reach.

Usage:
    from loader import load_setup
    setup = load_setup(scenario="S1")
    setup.cfg["simulation"]["epoch_minutes"]
    setup.machines["M1"].L0_minutes
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# =============================================================================
# Row types — thin records straight out of data/processed/
# =============================================================================
@dataclass(frozen=True)
class MachineSpec:
    machine_id: str
    L0_minutes: float
    e_idle_kwh_per_h: float
    delta_e_kwh_per_h: dict[str, float]
    efficiency_factor: float


@dataclass(frozen=True)
class OperatorSpec:
    operator: str
    sex: str
    age: int
    weight_kg: float
    height_cm: float
    e_rest_kcal_min: float
    awl_kcal_min: float
    skill: dict[str, float]

    def fatigue_band(self) -> float:
        """AWL - E_rest, the denominator of normalised fatigue (design §4.4)."""
        return self.awl_kcal_min - self.e_rest_kcal_min


@dataclass(frozen=True)
class TaskSpec:
    task: str
    energy_demand_kcal_min: float
    severity_kappa: float
    rula_base: int
    cognitive_base: float
    nominal_time_minutes: float


@dataclass
class Setup:
    """Everything one simulation run needs, already validated."""
    cfg: dict[str, Any]
    machines: dict[str, MachineSpec]
    operators: dict[str, OperatorSpec]
    tasks: dict[str, TaskSpec]
    scenario: str
    scenario_cfg: dict[str, Any] = field(default_factory=dict)

    # --- convenience accessors, so callers never index deep into cfg ---
    @property
    def epoch_minutes(self) -> int:
        return self.cfg["simulation"]["epoch_minutes"]

    @property
    def shift_minutes(self) -> int:
        return self.cfg["simulation"]["shift_minutes"]

    @property
    def epochs_per_shift(self) -> int:
        return self.shift_minutes // self.epoch_minutes

    def energy_range(self) -> tuple[float, float]:
        """Fleet-wide [lowest idle draw, highest full-load draw], for CP5.

        Normalising machine 'speed' needs a scale, and the fleet's own range is
        the only one that does not import an arbitrary constant.
        """
        lo = min(m.e_idle_kwh_per_h for m in self.machines.values())
        hi = max(m.e_idle_kwh_per_h + max(m.delta_e_kwh_per_h.values())
                 for m in self.machines.values())
        return lo, hi

    def processing_time(self, task_type: str, operator: str) -> float:
        """p = p0 / (0.5 + 0.5 * S)  — design §4.6. Skilled operators are faster."""
        p0 = self.tasks[task_type].nominal_time_minutes
        s = self.operators[operator].skill[task_type]
        return p0 / (0.5 + 0.5 * s)


# =============================================================================
def load_setup(scenario: str = "S1", root: Path = ROOT) -> Setup:
    cfg = yaml.safe_load((root / "src" / "config.yaml").read_text(encoding="utf-8"))
    proc = root / "data" / "processed"

    task_types = list(cfg["tasks"]["types"].keys())

    # --- machines ---------------------------------------------------------
    mdf = pd.read_csv(proc / "machine_params.csv")
    scale = cfg["machines"]["l0_scale_factor"]
    machines = {
        r.machine_id: MachineSpec(
            machine_id=r.machine_id,
            L0_minutes=float(r.L0_minutes) * scale,
            e_idle_kwh_per_h=float(r.e_idle_kwh_per_h),
            delta_e_kwh_per_h={t: float(getattr(r, f"delta_e_{t}_kwh_per_h"))
                               for t in task_types},
            efficiency_factor=float(r.efficiency_factor),
        )
        for r in mdf.itertuples()
    }

    # --- operators --------------------------------------------------------
    odf = pd.read_csv(proc / "operators.csv")
    sdf = pd.read_csv(proc / "skill_matrix.csv", index_col="operator")
    operators = {
        r.operator: OperatorSpec(
            operator=r.operator, sex=r.sex, age=int(r.age),
            weight_kg=float(r.weight_kg), height_cm=float(r.height_cm),
            e_rest_kcal_min=float(r.e_rest_kcal_min),
            awl_kcal_min=float(r.awl_kcal_min),
            skill={t: float(sdf.loc[r.operator, t]) for t in task_types},
        )
        for r in odf.itertuples()
    }

    # --- task types -------------------------------------------------------
    tdf = pd.read_csv(proc / "task_types.csv")
    tasks = {
        r.task: TaskSpec(
            task=r.task,
            energy_demand_kcal_min=float(r.energy_demand_kcal_min),
            severity_kappa=float(r.severity_kappa),
            rula_base=int(r.rula_base),
            cognitive_base=float(r.cognitive_base),
            nominal_time_minutes=float(r.nominal_time_minutes),
        )
        for r in tdf.itertuples()
    }

    setup = Setup(cfg=cfg, machines=machines, operators=operators, tasks=tasks,
                  scenario=scenario,
                  scenario_cfg=cfg["experiment"]["scenario_settings"][scenario])
    _validate(setup, task_types)
    return setup


# =============================================================================
def _validate(s: Setup, task_types: list[str]) -> None:
    """Fail loudly at load time rather than halfway through 270 runs."""
    sim = s.cfg["simulation"]

    assert len(s.machines) == sim["n_machines"], (
        f"config says {sim['n_machines']} machines, "
        f"machine_params.csv has {len(s.machines)}")
    assert len(s.operators) == sim["n_operators"], (
        f"config says {sim['n_operators']} operators, "
        f"operators.csv has {len(s.operators)}")

    assert s.shift_minutes % s.epoch_minutes == 0, (
        "shift length must be a whole number of decision epochs")

    mix = sim["task_type_mix"]
    assert set(mix) == set(task_types), "task_type_mix must cover every task type"
    assert abs(sum(mix.values()) - 1.0) < 1e-9, (
        f"task_type_mix sums to {sum(mix.values())}, must be 1.0")

    for name, w in s.cfg["objective"]["weight_scenarios"].items():
        assert abs(sum(w.values()) - 1.0) < 1e-9, (
            f"weight scenario {name} sums to {sum(w.values())}, must be 1.0")

    for o in s.operators.values():
        assert o.fatigue_band() > 0, (
            f"{o.operator}: AWL must exceed resting rate, "
            f"otherwise normalised fatigue divides by <= 0")
        assert set(o.skill) == set(task_types)

    for m in s.machines.values():
        assert m.L0_minutes > 0 and m.e_idle_kwh_per_h > 0

    hc = s.cfg["constraints"]["hard"]
    hy = s.cfg["constraints"]["hc1_hysteresis"]
    assert hy["leave_rest_at"] < hy["enter_rest_at"] == hc["HC1_fatigue_max"], (
        "the hysteresis band must sit below the HC1 threshold and start at it")

    f = s.cfg["fatigue"]
    assert f["mu_per_min"] > f["lambda_per_min"], (
        "recovery must be faster than accumulation (design §4.5)")
    assert f["mu_per_min"] < f["literature_upper_bound_mu"], (
        "recovery rate exceeds the localized-muscle bound from Yi et al. (2022)")


# =============================================================================
if __name__ == "__main__":
    s = load_setup()
    print(f"scenario {s.scenario}: {s.scenario_cfg}")
    print(f"{len(s.machines)} machines, {len(s.operators)} operators, "
          f"{len(s.tasks)} task types")
    print(f"shift {s.shift_minutes} min = {s.epochs_per_shift} epochs "
          f"of {s.epoch_minutes} min")
    print()
    print("processing time p0/(0.5+0.5S)  [minutes]")
    print("        " + "".join(f"{t:>8s}" for t in s.tasks))
    for o in s.operators:
        print(f"  {o:5s} " + "".join(f"{s.processing_time(t, o):8.1f}"
                                     for t in s.tasks))
    print()
    print("[ok] configuration and prepared data load and validate")
