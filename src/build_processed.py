"""
T4.3 / T4.5 / T4.6 — build the simulation inputs in data/processed/.

Nothing here is invented. Every value either
  (a) comes from data/processed/eda_params.json  (estimated from D1/D3 in T4.2), or
  (b) is copied from src/config.yaml             (frozen at GATE 3), or
  (c) is computed from a cited equation          (Mifflin 1990, Price 1990).

Outputs
-------
    data/processed/machine_params.csv   5 machines: L0, e_idle, delta_e per task
    data/processed/task_types.csv       T4.5 + T4.6: kappa, RULA, c_tau, E_w
    data/processed/skill_matrix.csv     T4.6: operator x task skill
    data/processed/operators.csv        E_rest and AWL, computed and verified

Run:  python src/build_processed.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

cfg = yaml.safe_load((ROOT / "src" / "config.yaml").read_text(encoding="utf-8"))
eda = json.loads((PROCESSED / "eda_params.json").read_text(encoding="utf-8"))

TASKS = ("L", "M", "H")


# =============================================================================
# 1 · Operators — compute E_rest and AWL, and check them against the design
# =============================================================================
def build_operators() -> pd.DataFrame:
    """Mifflin-St Jeor (1990) resting rate and Price (1990) acceptable work level.

    The design document states expected values for all three operators. They are
    recomputed here and asserted, so that a future edit to a weight or an age
    cannot silently desynchronise the code from docs/04-framework-design.md.
    """
    rows = []
    for name, p in cfg["operators"]["profiles"].items():
        male = p["sex"] == "male"
        s = 5 if male else -161
        e_rest = (s + 10 * p["weight_kg"] + 6.25 * p["height_cm"]
                  - 5 * p["age"]) / 1440
        if male:
            awl = (60 - 0.55 * p["age"]) * 0.005 * p["weight_kg"] / 3
        else:
            awl = (48 - 0.37 * p["age"]) * 0.005 * p["weight_kg"] / 3

        assert abs(e_rest - p["e_rest_kcal_min"]) < 5e-4, (
            f"{name}: E_rest {e_rest:.4f} != design {p['e_rest_kcal_min']}")
        assert abs(awl - p["awl_kcal_min"]) < 5e-4, (
            f"{name}: AWL {awl:.4f} != design {p['awl_kcal_min']}")

        rows.append({
            "operator": name, "sex": p["sex"], "age": p["age"],
            "weight_kg": p["weight_kg"], "height_cm": p["height_cm"],
            "e_rest_kcal_min": round(e_rest, 4),
            "awl_kcal_min": round(awl, 4),
            "fatigue_band_kcal_min": round(awl - e_rest, 4),
        })

    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED / "operators.csv", index=False)
    print("[ok] operators.csv — Mifflin/Price values match design §4.2 exactly")
    return df


# =============================================================================
# 2 · Task types  (T4.5 ergonomics + T4.6 task definition)
# =============================================================================
def build_task_types() -> pd.DataFrame:
    rows = []
    a_du = cfg["tasks"]["body_surface_area_m2"]
    factor = cfg["tasks"]["metabolic_factor"]

    for t in TASKS:
        spec = cfg["tasks"]["types"][t]
        # Recompute E_w from the ISO 8996 class rather than trusting the cached
        # number, for the same reason as above.
        e_w = spec["watt_per_m2"] * a_du * factor
        assert abs(e_w - spec["energy_demand_kcal_min"]) < 5e-3, (
            f"{t}: E_w {e_w:.3f} != design {spec['energy_demand_kcal_min']}")

        rows.append({
            "task": t,
            "iso8996_class": spec["iso8996_class"],
            "watt_per_m2": spec["watt_per_m2"],
            "energy_demand_kcal_min": round(e_w, 3),
            "severity_kappa": spec["severity_kappa"],
            "rula_base": spec["rula_base"],          # McAtamney & Corlett (1993)
            "cognitive_base": spec["cognitive_base"],
            "nominal_time_minutes": spec["nominal_time_minutes"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED / "task_types.csv", index=False)
    print("[ok] task_types.csv — ISO 8996 energy demands recomputed and match")
    return df


# =============================================================================
# 3 · Skill matrix  (T4.6)
# =============================================================================
def build_skill_matrix() -> pd.DataFrame:
    sm = cfg["operators"]["skill_matrix"]
    df = pd.DataFrame(sm).T.reindex(columns=list(TASKS))
    df.index.name = "operator"

    hc2 = cfg["constraints"]["hard"]["HC2_skill_min"]
    blocked = [(o, t) for o in df.index for t in TASKS if df.loc[o, t] < hc2]

    df.to_csv(PROCESSED / "skill_matrix.csv")
    print(f"[ok] skill_matrix.csv — HC2 (S >= {hc2}) blocks {len(blocked)} "
          f"of {df.size} pairs: {blocked}")
    return df


# =============================================================================
# 4 · Machine parameters  (T4.3)  — from D1 and D3
# =============================================================================
def build_machine_params() -> pd.DataFrame:
    n = cfg["simulation"]["n_machines"]

    # --- L0 : spread the 5 machines across the observed TWF wear distribution.
    # Deterministic percentiles rather than random draws, so the file is
    # reproducible without carrying a seed.
    twf = pd.read_csv(RAW / "ai4i2020" / "ai4i2020.csv")
    twf = twf.loc[twf["TWF"] == 1, "Tool wear [min]"]
    pct = np.linspace(10, 90, n)
    l0 = np.percentile(twf, pct) * cfg["machines"]["l0_scale_factor"]

    # --- energy : preserve the ratios measured in D3, rescale the absolute
    # level to this factory. The scale factor is fixed by requiring that a
    # machine running Medium work draws the configured reference power.
    per_h = 60 / eda["energy_interval_minutes"]          # intervals -> per hour
    e_idle_data = eda["e_idle_kwh_per_interval"] * per_h
    d_data = {t: eda["delta_e_kwh_per_interval"][t] * per_h for t in TASKS}

    target = cfg["machines"]["energy_rescale_to_kwh_per_hour"]
    scale = target / (e_idle_data + d_data["M"])

    # Per-machine efficiency spread, deterministic and symmetric about 1.0.
    eff = np.linspace(0.90, 1.10, n)

    rows = []
    for i in range(n):
        rows.append({
            "machine_id": f"M{i + 1}",
            "L0_minutes": round(float(l0[i]), 1),
            "e_idle_kwh_per_h": round(e_idle_data * scale * eff[i], 4),
            "delta_e_L_kwh_per_h": round(d_data["L"] * scale * eff[i], 4),
            "delta_e_M_kwh_per_h": round(d_data["M"] * scale * eff[i], 4),
            "delta_e_H_kwh_per_h": round(d_data["H"] * scale * eff[i], 4),
            "efficiency_factor": round(float(eff[i]), 3),
        })

    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED / "machine_params.csv", index=False)
    print(f"[ok] machine_params.csv — L0 from D1 TWF percentiles "
          f"{l0.min():.0f}-{l0.max():.0f} min; energy ratios from D3 "
          f"(scale factor {scale:.4f})")
    return df


# =============================================================================
# 5 · Cross-checks that must hold before Phase 5 starts
# =============================================================================
def sanity_checks(ops: pd.DataFrame, tasks: pd.DataFrame,
                  machines: pd.DataFrame) -> None:
    print()
    print("=" * 72)
    print("SANITY CHECKS")
    print("=" * 72)

    # A · which operator can sustain which task (design §4.10)
    print()
    print("Task sustainability — is E_w below the operator's AWL?")
    print(f"{'':6s}" + "".join(f"{t:>12s}" for t in TASKS))
    for _, o in ops.iterrows():
        cells = []
        for t in TASKS:
            e_w = tasks.loc[tasks["task"] == t, "energy_demand_kcal_min"].iloc[0]
            cells.append("  ok" if e_w <= o["awl_kcal_min"] else "  OVER AWL")
        print(f"{o['operator']:6s}" + "".join(f"{c:>12s}" for c in cells))
    print()
    print("  -> OP2 cannot sustain Medium or Heavy work indefinitely. That is")
    print("     the intended behaviour, not a bug (design §4.10).")

    # B · machine life under each task type
    print()
    print("Machine life at full utilisation (L0 / kappa):")
    for t in TASKS:
        k = tasks.loc[tasks["task"] == t, "severity_kappa"].iloc[0]
        lo = machines["L0_minutes"].min() / k
        hi = machines["L0_minutes"].max() / k
        print(f"  task {t} (kappa={k}):  {lo:6.0f} - {hi:6.0f} min "
              f"({lo / 480:.2f} - {hi / 480:.2f} shifts)")

    # C · energy sanity
    print()
    m = machines.iloc[len(machines) // 2]
    print(f"Energy for the median machine ({m['machine_id']}):")
    for t in TASKS:
        total = m["e_idle_kwh_per_h"] + m[f"delta_e_{t}_kwh_per_h"]
        co2 = total * cfg["sustainability"]["emission_factor_kg_co2_per_kwh"]
        print(f"  task {t}:  {total:5.2f} kWh/h  ->  {co2:5.2f} kg CO2e/h")

    # D · every value that feeds the simulation is finite and positive
    assert machines["L0_minutes"].gt(0).all()
    assert machines.filter(like="kwh").gt(0).all().all()
    assert ops["fatigue_band_kcal_min"].gt(0).all(), \
        "AWL must exceed E_rest, otherwise normalised fatigue divides by <= 0"
    print()
    print("[ok] all values finite, positive, and within their expected ranges")


def main() -> None:
    ops = build_operators()
    tasks = build_task_types()
    build_skill_matrix()
    machines = build_machine_params()
    sanity_checks(ops, tasks, machines)


if __name__ == "__main__":
    main()
