"""Tests for the decision-pressure measurement (supports §V.E.1).

Two things have to hold. The probe must not change what the simulation does —
an observer that perturbs the run would invalidate every number reported
beside it. And the quantities must be computed, not asserted: this measurement
exists because the figures it replaces were literals in a print statement.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from decision.constraints import Candidate  # noqa: E402
from decision_pressure import measure  # noqa: E402
from loader import load_setup  # noqa: E402
from simulation.factory import run_shift, weighted_allocator  # noqa: E402


def _digest(with_probe: bool, shifts: int = 6) -> str:
    setup = load_setup("S2")
    rows = []
    for seed in range(shifts):
        if with_probe:
            def on_epoch(state):
                if getattr(state, "decision_probe", None) is None:
                    state.decision_probe = lambda n, spread: None
            rows.append(run_shift(setup, seed=seed,
                                  allocator=weighted_allocator,
                                  on_epoch=on_epoch))
        else:
            rows.append(run_shift(setup, seed=seed,
                                  allocator=weighted_allocator))
    return hashlib.md5(
        pd.DataFrame(rows).to_csv(index=False).encode()).hexdigest()


# =============================================================================
# The observer must not perturb what it observes
# =============================================================================
def test_probe_does_not_change_the_run():
    assert _digest(with_probe=False) == _digest(with_probe=True), (
        "attaching the decision probe changed the simulation output, so every "
        "figure measured alongside it would describe a different run")


def test_probe_is_absent_by_default():
    """No normal run carries one, so nothing pays for it."""
    setup = load_setup("S1")
    seen = {}
    run_shift(setup, seed=0, allocator=weighted_allocator,
              on_epoch=lambda st: seen.setdefault(
                  "probe", getattr(st, "decision_probe", None)))
    assert seen["probe"] is None


# =============================================================================
# The probe reports what it claims to report
# =============================================================================
def test_probe_fires_once_per_decision_with_a_plausible_count():
    setup = load_setup("S2")
    calls: list[tuple[int, float | None]] = []

    def on_epoch(state):
        if getattr(state, "decision_probe", None) is None:
            state.decision_probe = lambda n, spread: calls.append((n, spread))

    run_shift(setup, seed=0, allocator=weighted_allocator, on_epoch=on_epoch)

    assert calls, "the probe never fired"
    n_ops = len(setup.operators) * len(setup.machines)
    assert all(0 <= n <= n_ops for n, _ in calls), (
        "an option count outside 0..operators x machines is impossible")
    assert all(s is None for n, s in calls if n < 2), (
        "a spread was reported where there was nothing to compare")
    assert all(s is not None and s >= 0 for n, s in calls if n >= 2), (
        "no spread reported where two or more options existed")


def test_measure_reports_consistent_shares():
    r = measure("S2", shifts=3)
    assert r["decisions"] > 0
    assert r["no_choice"] <= r["decisions"]
    assert abs(r["share_no_choice"] + r["share_with_choice"] - 1.0) < 1e-9
    assert 0.0 <= r["share_no_choice"] <= 1.0
    assert r["median_spread"] <= r["max_spread"]


def test_the_claim_in_section_five_holds():
    """§V.E.1 says most decisions have nothing to choose between.

    Asserted as a band rather than a point so a real change in the framework
    fails here and gets reported, while ordinary noise does not.
    """
    r = measure("S2", shifts=10)
    assert 0.90 <= r["share_no_choice"] <= 0.99, (
        f"share with no choice is {r['share_no_choice']:.1%}; §V.E.1 describes "
        f"a heavily constrained decision and would need rewriting")
    assert r["median_spread"] < 0.05, (
        f"median spread is {r['median_spread']}; if the objective has this "
        f"much room, the claim that constraints rather than weights steer the "
        f"framework no longer follows")
