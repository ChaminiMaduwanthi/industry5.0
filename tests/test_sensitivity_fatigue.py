"""
T7.6b — what the fatigue-rate sensitivity study must satisfy.

WRITTEN BEFORE THE STUDY. This is the condition under which lambda and mu may
be called calibrated rather than measured (design §4.5, carried over from
GATE 3). If the study is wrong, the honesty of the whole parameter story goes
with it.

The failure this guards against is a vacuous pass: a study that reports "the
ranking held" because the scaling never actually changed anything would look
identical to a real one. So the first thing checked is that the parameter does
something.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from sensitivity_fatigue import HUMAN_KPIS, run_cell, scaled_setup  # noqa: E402

CFG = load_setup("S1").cfg


# =============================================================================
# The parameter must actually bite — otherwise the study proves nothing
# =============================================================================
def test_scaling_changes_the_configuration():
    base = CFG["fatigue"]
    half = scaled_setup("S2", 0.5).cfg["fatigue"]
    double = scaled_setup("S2", 2.0).cfg["fatigue"]

    assert half["lambda_per_min"] == pytest.approx(base["lambda_per_min"] * 0.5)
    assert double["mu_per_min"] == pytest.approx(base["mu_per_min"] * 2.0)


def test_recovery_stays_faster_than_accumulation_at_every_scaling():
    """mu > lambda is a stated condition of the calibration (design §4.5).

    Scaling both by the same factor preserves it, but a study that broke it
    would be testing a model the design does not describe.
    """
    for factor in CFG["sensitivity"]["fatigue_rate_scalings"]:
        f = scaled_setup("S2", factor).cfg["fatigue"]
        assert f["mu_per_min"] > f["lambda_per_min"]


def test_scaling_visibly_changes_the_outcome():
    """A study whose knob does nothing would report a pass regardless."""
    slow = run_cell("S2", "B2", 0.5)
    fast = run_cell("S2", "B2", 2.0)
    assert slow["mean_fatigue"] != fast["mean_fatigue"]
    assert fast["mean_fatigue"] > slow["mean_fatigue"], (
        "faster accumulation must leave operators more tired, not less")


# =============================================================================
# The comparison must stay valid across the sweep
# =============================================================================
@pytest.mark.parametrize("factor", [0.5, 1.0, 2.0])
def test_the_constrained_policy_still_holds_its_limits(factor):
    """B3 must keep breaches at zero however fast fatigue accumulates."""
    assert run_cell("S2", "B3", factor)["constraint_violations"] == 0


@pytest.mark.parametrize("factor", [0.5, 1.0, 2.0])
def test_the_ranking_does_not_flip(factor):
    """The GATE 3 condition itself, asserted for every scaling."""
    b2 = run_cell("S2", "B2", factor)
    b3 = run_cell("S2", "B3", factor)
    for kpi in HUMAN_KPIS:
        assert b3[kpi] <= b2[kpi], (
            f"at {factor}x the fatigue rates, B3 is worse than B2 on {kpi} "
            f"({b3[kpi]:.3f} vs {b2[kpi]:.3f}) — the conclusion depends on "
            f"the calibrated values")


def test_the_baseline_never_holds_the_limits_by_accident():
    """B2 must breach at every scaling, or there is nothing to compare."""
    for factor in (0.5, 1.0, 2.0):
        assert run_cell("S2", "B2", factor)["constraint_violations"] > 0
