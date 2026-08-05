"""
What the cross-training analysis must satisfy.

WRITTEN BEFORE THE ANALYSIS. This one carries a specific hazard: it improves a
result that came out badly, so it is exactly the kind of study that turns into
cherry-picking if it is allowed to leak. The headline results must stay on the
configuration that was actually run, and the improvement must be reported for
what it is — a partial one.

So the first thing checked is not the finding. It is that running this changes
nothing else.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from crosstraining import BASE_SKILL, TRAINED, measure, retrained_setup  # noqa: E402
from loader import load_setup                              # noqa: E402


# =============================================================================
# It must not contaminate anything else
# =============================================================================
def test_the_stored_skill_matrix_is_never_written_to():
    before = (ROOT / "data" / "processed" / "skill_matrix.csv").read_bytes()
    retrained_setup("S2")
    measure("S2", trained=True, seeds=2)
    after = (ROOT / "data" / "processed" / "skill_matrix.csv").read_bytes()
    assert before == after, "the analysis edited the stored skill matrix"


def test_a_fresh_setup_still_has_the_original_skills():
    """The headline results must remain the ones that were actually run."""
    retrained_setup("S2")
    fresh = load_setup("S2")
    for op, skills in BASE_SKILL.items():
        for task, value in skills.items():
            assert fresh.operators[op].skill[task] == pytest.approx(value), (
                f"{op}/{task} leaked out of the cross-training analysis")


def test_only_the_named_operator_is_retrained():
    trained = retrained_setup("S2")
    for op in BASE_SKILL:
        for task in BASE_SKILL[op]:
            expected = TRAINED.get(op, {}).get(task, BASE_SKILL[op][task])
            assert trained.operators[op].skill[task] == pytest.approx(expected)


def test_the_change_clears_the_competence_floor():
    """Cross-training is only meaningful if it makes the pairing legal."""
    cfg = load_setup("S2").cfg
    floor = cfg["constraints"]["hard"]["HC2_skill_min"]
    for op, skills in TRAINED.items():
        for task, value in skills.items():
            assert BASE_SKILL[op][task] < floor <= value, (
                f"{op}/{task} was already allowed — training it changes nothing")


# =============================================================================
# The finding, asserted as the partial one it is
# =============================================================================
@pytest.fixture(scope="module")
def cells() -> dict:
    return {
        "B2": measure("S2", baseline="B2"),
        "B3": measure("S2", trained=False),
        "B3_trained": measure("S2", trained=True),
    }


def test_training_improves_the_workload_spread(cells):
    assert cells["B3_trained"]["workload_gini"] < cells["B3"]["workload_gini"]


def test_but_does_not_close_the_gap(cells):
    """The honest half. Claiming it was solved would be false."""
    assert cells["B3_trained"]["workload_gini"] > cells["B2"]["workload_gini"], (
        "the gap closed entirely — the reporting must be rewritten, not the "
        "claim quietly upgraded")


def test_the_limits_still_hold_after_training(cells):
    assert cells["B3_trained"]["constraint_violations"] == 0


def test_protection_is_not_traded_away_for_balance(cells):
    """Fatigue may rise a little, but must stay far below the baseline."""
    assert cells["B3_trained"]["mean_fatigue"] < cells["B2"]["mean_fatigue"] * 0.9


def test_throughput_does_not_suffer(cells):
    assert cells["B3_trained"]["throughput"] >= cells["B3"]["throughput"]
