"""
Checks on the human twin (T5.7, T5.8) — the part of the model the paper's
contribution rests on, so it gets tested against the design rather than against
whatever the code happens to produce.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from models.human import fatigue as fat                    # noqa: E402
from simulation.factory import run_shift                   # noqa: E402
from twins.human_twin import HumanTwin                     # noqa: E402

SETUP = load_setup("S1")
CFG = SETUP.cfg
LAM = CFG["fatigue"]["lambda_per_min"]
MU = CFG["fatigue"]["mu_per_min"]


def _twin(op: str) -> HumanTwin:
    return HumanTwin(spec=SETUP.operators[op], cfg=CFG)


def _work_for(twin: HumanTwin, task: str, minutes: float,
              epoch: float, start: float = 0.0) -> float:
    """Work continuously from `start` for `minutes`, advancing epoch by epoch.

    Returns the clock time reached, so a test can carry on with rest.
    """
    demand = SETUP.tasks[task].energy_demand_kcal_min
    twin.begin_task(start, demand)
    twin.end_task(start + minutes)

    now = start
    while now < start + minutes:
        now += epoch
        twin.advance(now, epoch)
    return now


def _rest_for(twin: HumanTwin, minutes: float, epoch: float,
              start: float) -> float:
    now = start
    while now < start + minutes:
        now += epoch
        twin.advance(now, epoch)
    return now


# =============================================================================
# The equations themselves
# =============================================================================
def test_recovery_is_faster_than_accumulation():
    """mu > lambda is a stated condition of the calibration (design §4.5)."""
    assert MU > LAM
    assert fat.half_life_minutes(MU) < fat.half_life_minutes(LAM)


def test_fatigue_approaches_the_task_demand_and_stops_there():
    """Design §4.1: light work must never exhaust anyone.

    This is the reason for modelling energy expenditure instead of an abstract
    counter — the asymptote is the task's own demand, not 1.
    """
    twin = _twin("OP1")
    demand = SETUP.tasks["L"].energy_demand_kcal_min
    _work_for(twin, "L", 480, 15)
    assert twin.fatigue <= demand + 1e-9
    assert abs(twin.fatigue - demand) < 0.05        # essentially converged


def test_op1_matches_the_design_validation_figure():
    """Design §4.10 reports OP1 ending a shift of continuous medium work at
    F_hat = 0.74 with no rest episodes. Reproduce it from the code."""
    twin = _twin("OP1")
    _work_for(twin, "M", 480, 15)
    assert twin.fatigue_hat == pytest.approx(0.74, abs=0.01)


def test_the_same_task_tires_operators_differently():
    """The whole personalisation claim in one assertion.

    Identical work, no per-operator rule anywhere — the difference comes only
    from Mifflin-St Jeor and Price acting on age, sex and weight.
    """
    hats = {}
    for op in ("OP1", "OP2", "OP3"):
        twin = _twin(op)
        _work_for(twin, "M", 240, 15)
        hats[op] = twin.fatigue_hat

    assert hats["OP2"] > hats["OP3"] > hats["OP1"], hats
    assert hats["OP2"] - hats["OP1"] > 0.2, (
        f"personalisation is too weak to matter: {hats}")


def test_resting_sheds_fatigue():
    twin = _twin("OP2")
    now = _work_for(twin, "H", 120, 15)
    tired = twin.fatigue_hat
    _rest_for(twin, 120, 15, now)         # two hours of rest
    assert twin.fatigue_hat < tired
    assert twin.fatigue >= twin.spec.e_rest_kcal_min - 1e-9


def test_every_worked_minute_reaches_the_fatigue_model():
    """A task longer than an epoch must still be charged in full.

    Heavy work takes 19 to 28 minutes against a 15 minute epoch. Crediting
    those minutes only when the task ends, then capping at the epoch length,
    discarded about a quarter of all work and understated fatigue to match.
    """
    setup = load_setup("S2")
    box = {}
    run_shift(setup, seed=0, on_epoch=lambda st: box.setdefault("s", st))
    state = box["s"]
    for op_id, op in state.operators.items():
        charged = state.humans[op_id].charged_minutes
        assert charged == pytest.approx(op.busy_minutes, rel=0.02), (
            f"{op_id}: worked {op.busy_minutes:.1f} min but only "
            f"{charged:.1f} min reached the fatigue model")


def test_normalised_fatigue_stays_in_range():
    twin = _twin("OP2")                   # the operator who goes over AWL
    _work_for(twin, "H", 480, 15)
    assert 0.0 <= twin.fatigue_hat <= 1.0


# =============================================================================
# The couplings, as they appear in a real run
# =============================================================================
@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
@pytest.mark.parametrize("seed", range(5))
def test_fatigue_within_range_over_a_whole_shift(scenario, seed):
    setup = load_setup(scenario)
    box = {}
    run_shift(setup, seed=seed, on_epoch=lambda st: box.setdefault("s", st))
    for h in box["s"].humans.values():
        assert all(0.0 <= f <= 1.0 for f in h.fatigue_trace)
        assert h.fatigue >= h.spec.e_rest_kcal_min - 1e-9


@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
@pytest.mark.parametrize("seed", range(5))
def test_rula_within_its_scale(scenario, seed):
    setup = load_setup(scenario)
    box = {}
    run_shift(setup, seed=seed, on_epoch=lambda st: box.setdefault("s", st))
    for h in box["s"].humans.values():
        assert all(1 <= r <= 7 for r in h.rula_samples)
        assert all(0.0 <= c <= 1.0 for c in h.cognitive_samples)


def test_cp2_actually_changes_the_outcome():
    """Fatigue must measurably raise defect risk, or CP2 is decorative.

    Run the shift, then recompute every unit's risk with the fatigue term
    zeroed. If the totals match, the coupling does nothing.
    """
    setup = load_setup("S2")
    box = {}
    run_shift(setup, seed=0, on_epoch=lambda st: box.setdefault("s", st))
    state = box["s"]

    with_fatigue = sum(t.defect_risk for t in state.completed)
    without = 0.0
    for t in state.completed:
        twin = state.twins[t.assigned_machine]
        without += twin.defect_risk(
            skill=setup.operators[t.assigned_operator].skill[t.task_type],
            kappa=setup.tasks[t.task_type].severity_kappa,
            fatigue_hat=0.0)

    assert with_fatigue > without * 1.05, (
        f"CP2 barely moves defect risk: {with_fatigue:.2f} vs {without:.2f}")
