"""
T7.8 — what the coupling ablation must satisfy.

WRITTEN BEFORE THE ABLATION. This study is the direct evidence for the central
claim: that carrying state between the two twins is worth something. It is also
the last cover for the coupling coefficients, which no dataset can fit.

The design decision it rests on, and the one most likely to be got wrong: a
coupling is switched off in the SCHEDULER'S VIEW, not in the factory. A tired
operator still makes more mistakes when CP2 is ablated — the scheduler simply
cannot see that when choosing. Removing it from the physics as well would
simulate a different, kinder world for each ablation and make the runs
incomparable, which is the same error as disabling the couplings for the
Industry 4.0 baseline.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from ablation import ABLATIONS, measure                    # noqa: E402

SEEDS = 10


@pytest.fixture(scope="module")
def cells() -> dict:
    return {name: measure("S2", name, seeds=SEEDS) for name in ABLATIONS}


# =============================================================================
# The physics must survive the ablation
# =============================================================================
def test_the_factory_is_the_same_in_every_run(cells):
    """Same seed, same order book — only the scheduler's view changes."""
    demands = {name: c["demand"] for name, c in cells.items()}
    assert len(set(demands.values())) == 1, demands


def test_fatigue_still_drives_defects_when_the_scheduler_cannot_see_it():
    """Ablating CP2 must not make tired operators harmless.

    If it did, every ablated run would be scored in a world of its own and the
    comparison would be meaningless.
    """
    from loader import load_setup
    from simulation.factory import run_shift
    from ablation import allocator_for

    box = {}
    run_shift(load_setup("S2"), seed=0, allocator=allocator_for("CP2"),
              on_epoch=lambda st: box.setdefault("s", st))
    state = box["s"]

    tired = [t for t in state.completed
             if t.fatigue_at_start and t.fatigue_at_start > 0.4]
    assert tired, "no fatigued work to check"

    # Recompute from the conditions RECORDED for each task. Asking the twin
    # again would use its health at the end of the shift, not at the moment the
    # task ran, and a worn machine raises risk on its own — which is what an
    # earlier version of this check tripped over.
    import math
    b = state.setup.cfg["quality"]["fallback_coefficients"]

    def risk(health, skill, fatigue, kappa):
        z = (b["b0"] + b["b1"] * (1 - health) + b["b2"] * (1 - skill)
             + b["b3"] * fatigue + b["b4"] * kappa)
        return 1 / (1 + math.exp(-z))

    for task in tired[:20]:
        spec = state.setup.tasks[task.task_type]
        skill = state.setup.operators[task.assigned_operator].skill[task.task_type]
        recorded = risk(task.machine_health_at_start, skill,
                        task.fatigue_at_start, spec.severity_kappa)
        blind = risk(task.machine_health_at_start, skill, 0.0,
                     spec.severity_kappa)

        assert task.defect_risk == pytest.approx(recorded, abs=1e-9), (
            "the outcome was not scored on the conditions the task ran under")
        assert task.defect_risk > blind, (
            "the recorded defect risk ignored fatigue — the ablation reached "
            "the physics, not just the decision")


# =============================================================================
# The ablation must actually do something
# =============================================================================
def test_every_ablation_changes_the_outcome(cells):
    full = cells["none"]
    for name, c in cells.items():
        if name == "none":
            continue
        assert any(abs(c[k] - full[k]) > 1e-9
                   for k in ("mean_fatigue", "throughput", "scrap_rate",
                             "constraint_violations")), (
            f"ablating {name} changed nothing — it is not reaching the decision")


def test_removing_the_ergonomic_coupling_causes_real_breaches(cells):
    """CP5 feeds the ergonomic score that HC3 filters on.

    Blind to it, the scheduler filters on a score that understates the risk and
    lets through pairings that breach the limit in fact. That breach count is
    the coupling's value, made visible.
    """
    assert cells["none"]["hc3_breaches"] == 0
    assert cells["CP5"]["hc3_breaches"] > 0


def test_the_full_framework_is_not_beaten_by_any_ablation_on_the_human_side(cells):
    """Removing information should not help the operator. If it did, the
    coupling would be a liability rather than a contribution."""
    full = cells["none"]
    for name, c in cells.items():
        if name == "none":
            continue
        assert c["constraint_violations"] >= full["constraint_violations"], (
            f"ablating {name} produced fewer violations than the full "
            f"framework — the coupling is not doing what is claimed")
