"""
T7.6 — what the weight sensitivity study must satisfy.

WRITTEN BEFORE THE STUDY. It carries one claim worth being careful with. The
experiment plan predicts that the profit-weighted configuration approximates
the Industry 4.0 baseline, and reads that as showing Industry 4.0 to be a
special case of this framework.

That cannot be true in general, and asserting the limit here stops it being
written carelessly later: the profit configuration still enforces every hard
constraint. It can converge on the baseline's THROUGHPUT. It cannot converge
on its fatigue or its breach count, because the constraints do not depend on
the weights at all. That is the point of making them constraints.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from weight_sensitivity import CONFIGS, measure            # noqa: E402

SEEDS = 10


@pytest.fixture(scope="module")
def cells() -> dict:
    out = {name: measure("S2", name, seeds=SEEDS) for name in CONFIGS}
    out["B2"] = measure("S2", "W-Profit", seeds=SEEDS, baseline="B2")
    return out


# =============================================================================
# The weights must steer what they name
# =============================================================================
def test_the_weights_barely_move_the_outcome(cells):
    """The measured result, pinned so it is not misreported.

    The first version of this file assumed the weights would steer and checked
    only direction, with <= — which passes when nothing moves at all. It did
    pass, on four configurations identical to three decimal places.

    They are indistinguishable, and the cause is upstream: after the hard
    constraints filter, 95.8% of decisions in S2 offer zero or one candidate.
    There is nothing left to weigh. This is asserted rather than explained away
    so that a future change making the weights matter shows up as a failure
    here and gets reported, instead of quietly altering what §V claims.
    """
    fatigue = [cells[n]["mean_fatigue"] for n in CONFIGS]
    throughput = [cells[n]["throughput"] for n in CONFIGS]
    assert max(fatigue) - min(fatigue) < 0.01, (
        f"the weights now separate on fatigue — update §V: "
        f"{dict(zip(CONFIGS, fatigue))}")
    assert max(throughput) - min(throughput) < 1.0, (
        f"the weights now separate on throughput — update §V: "
        f"{dict(zip(CONFIGS, throughput))}")


def test_no_configuration_can_reach_the_baseline_on_the_human_side(cells):
    """Whatever the weights do or fail to do, they cannot lift a constraint."""
    for name in CONFIGS:
        assert cells[name]["constraint_violations"] == 0
        assert cells[name]["mean_fatigue"] < cells["B2"]["mean_fatigue"] * 0.9


# =============================================================================
# The limit of the "special case" reading
# =============================================================================
def test_the_profit_configuration_approaches_the_baseline_on_throughput(cells):
    gap = abs(cells["W-Profit"]["throughput"] - cells["B2"]["throughput"])
    assert gap / cells["B2"]["throughput"] < 0.10, (
        f"W-Profit is {gap:.1f} units from B2 — too far to describe as "
        f"approaching it")


def test_but_never_becomes_the_baseline(cells):
    """Weights cannot switch off a constraint. This is the whole architecture.

    If this ever passes trivially — if W-Profit did reach B2's breach count —
    the hard constraints would have become negotiable and the paper's central
    distinction would be gone.
    """
    assert cells["W-Profit"]["constraint_violations"] == 0
    assert cells["B2"]["constraint_violations"] > 0
    assert cells["W-Profit"]["mean_fatigue"] < cells["B2"]["mean_fatigue"] * 0.9


def test_all_configurations_hold_the_limits(cells):
    for name in CONFIGS:
        assert cells[name]["constraint_violations"] == 0, (
            f"{name} breached a hard constraint — weights reached the "
            f"constraint layer")


def test_the_weights_are_all_valid():
    weights = load_setup("S1").cfg["objective"]["weight_scenarios"]
    for name, w in weights.items():
        assert abs(sum(w.values()) - 1.0) < 1e-9, name
        assert all(v >= 0 for v in w.values()), name
