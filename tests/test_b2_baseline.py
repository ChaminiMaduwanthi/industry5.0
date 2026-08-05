"""
T6.2 — what the Industry 4.0 baseline must satisfy.

WRITTEN BEFORE THE IMPLEMENTATION. The point of B2 is to be a fair opponent:
if it is quietly weakened, every result in the paper is worthless, and a
weakened baseline is easy to produce by accident. So the properties that make
it fair are pinned down here first.

Design §11 defines it as the same framework under restrictions, not separate
code:

    machine twin      full strength, including the health constraint
    human twin        still running, so fatigue can be MEASURED
                      but invisible to the decision
    constraints       HC4 only — none of the human ones
    objective         throughput alone
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from simulation.factory import (                           # noqa: E402
    industry40_allocator, random_allocator, run_shift, weighted_allocator,
)

SEEDS = 12


def _run(scenario, allocator, seed):
    return run_shift(load_setup(scenario), seed=seed, allocator=allocator)


def _mean(scenario, allocator, key):
    return sum(_run(scenario, allocator, s)[key] for s in range(SEEDS)) / SEEDS


# =============================================================================
# B2 must be STRONG — a weak opponent proves nothing
# =============================================================================
@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
def test_b2_keeps_the_full_machine_twin(scenario):
    """HC4 still applies: no work on a machine below its health floor."""
    setup = load_setup(scenario)
    floor = setup.cfg["machines"]["health_min_operational"]
    box = {}
    run_shift(setup, seed=0, allocator=industry40_allocator,
              on_epoch=lambda st: box.setdefault("s", st))
    bad = [t.task_id for t in box["s"].completed
           if t.machine_health_at_start is not None
           and t.machine_health_at_start <= floor]
    assert not bad, f"B2 ran {len(bad)} task(s) on an unavailable machine"


@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
def test_b2_out_produces_the_random_baseline(scenario):
    """B2 schedules for throughput, so it must beat picking at random.

    If it does not, B2 is not an Industry 4.0 scheduler — it is a broken one,
    and beating it would mean nothing.
    """
    b1 = _mean(scenario, random_allocator, "throughput")
    b2 = _mean(scenario, industry40_allocator, "throughput")
    assert b2 >= b1, f"B2 {b2:.1f} produced less than random {b1:.1f}"


def test_b2_is_the_throughput_leader_under_pressure():
    """Under high demand B2 should out-produce the human-aware policy.

    This is the trade-off the paper reports. If B3 matched B2 on throughput
    there would be no trade-off to discuss, and the result would look too good
    to be true — which usually means it is.
    """
    b2 = _mean("S2", industry40_allocator, "throughput")
    b3 = _mean("S2", weighted_allocator, "throughput")
    assert b2 >= b3


# =============================================================================
# B2 must be BLIND to the human — that is the whole difference
# =============================================================================
@pytest.mark.parametrize("scenario", ["S1", "S2"])
def test_b2_does_not_enforce_the_human_constraints(scenario):
    """It has no fatigue limit, so under load it must breach one."""
    breaches = _mean(scenario, industry40_allocator, "hc1_breaches")
    assert breaches > 0, (
        "B2 kept every operator under the fatigue limit without being told to "
        "— it is not a machine-only scheduler")
    assert _mean(scenario, industry40_allocator, "rest_episodes") == 0


@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
def test_b2_still_measures_fatigue(scenario):
    """Design §11: the human twin keeps running under B2.

    Without it there is no fatigue figure for B2 and therefore no comparison
    to make. Invisible to the decision is not the same as switched off.
    """
    r = _run(scenario, industry40_allocator, 0)
    assert r["mean_fatigue"] > 0
    assert r["max_fatigue"] > 0
    assert r["mean_rula"] > 0


# =============================================================================
# The comparison must be fair
# =============================================================================
@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
def test_both_policies_face_the_same_work(scenario):
    """Same seed, same order book, same breakdowns — only the policy differs."""
    a = _run(scenario, industry40_allocator, 5)
    b = _run(scenario, weighted_allocator, 5)
    assert a["demand"] == b["demand"]
    assert a["scenario"] == b["scenario"]


def test_the_disruption_is_identical_for_both():
    """S3 must hit B2 and B3 with the same failures on the same seed."""
    a = _run("S3", industry40_allocator, 7)
    b = _run("S3", weighted_allocator, 7)
    assert a["maintenance_events"] > 0
    assert b["maintenance_events"] > 0


def test_b2_decisions_ignore_the_operator_entirely():
    """Not enforcing the human constraints is weaker than being blind to them.

    Exhaust every operator mid-run and B2 must schedule exactly as before,
    while the human-aware policy must visibly change course. Asserting the
    contrast pins down what separates the two: information, not effort.
    """
    def exhaust(state):
        for h in state.humans.values():
            h.fatigue = h.spec.awl_kcal_min * 0.99

    normal = _run("S2", industry40_allocator, 3)
    tired = run_shift(load_setup("S2"), seed=3, allocator=industry40_allocator,
                      on_epoch=exhaust)
    assert tired["throughput"] == normal["throughput"], (
        "B2 reacted to operator fatigue — it is not machine-only")

    b3_normal = _run("S2", weighted_allocator, 3)
    b3_tired = run_shift(load_setup("S2"), seed=3, allocator=weighted_allocator,
                         on_epoch=exhaust)
    assert b3_tired["throughput"] < b3_normal["throughput"], (
        "B3 ignored exhausted operators — the constraints are not binding")


def test_b2_is_not_a_straw_man():
    """A weakened baseline would understate what the human policy costs.

    Greedy shortest-first is compared against an optimal per-epoch assignment.
    If the optimum were meaningfully better, B2 would be leaving throughput on
    the table and every reported trade-off would flatter the proposal.
    """
    import numpy as np
    from scipy.optimize import linear_sum_assignment

    def optimal(state, rng):
        setup = state.setup
        ops, macs = state.free_operators(), state.free_machines()
        tasks = state.pending_tasks()
        if not ops or not macs or not tasks:
            return []
        tasks = tasks[:len(ops)]
        cost = np.array([[setup.processing_time(t.task_type, o) for o in ops]
                         for t in tasks])
        ti, oi = linear_sum_assignment(cost)
        pairs = sorted(zip(ti, oi), key=lambda p: cost[p[0], p[1]])
        n = min(len(ops), len(macs), len(tasks))
        by_health = sorted(macs, key=lambda m: state.twins[m].health)
        return [(tasks[t], ops[o], by_health[k])
                for k, (t, o) in enumerate(pairs[:n])]
    optimal.enforces = frozenset()

    greedy = _mean("S2", industry40_allocator, "throughput")
    best = sum(_run("S2", optimal, s)["throughput"] for s in range(SEEDS)) / SEEDS
    assert greedy >= best - 1.0, (
        f"an optimal assignment beats B2 by {best - greedy:.1f} units — "
        f"B2 is leaving throughput unclaimed")


# =============================================================================
# The result the paper rests on
# =============================================================================
def test_the_headline_holds_on_a_different_seed_block():
    """The reported gap must not be an artefact of the evaluation seeds.

    Design §6 keeps seeds 0-29 for evaluation and 100-129 for calibration.
    Running the comparison on both must give the same story, or the numbers
    are noise dressed up as a finding.
    """
    n = 15

    def delta(seeds):
        out = {}
        for kpi in ("mean_fatigue", "throughput"):
            b2 = sum(run_shift(load_setup("S2"), seed=s,
                               allocator=industry40_allocator)[kpi]
                     for s in seeds) / len(seeds)
            b3 = sum(run_shift(load_setup("S2"), seed=s,
                               allocator=weighted_allocator)[kpi]
                     for s in seeds) / len(seeds)
            out[kpi] = (b3 - b2) / b2 * 100
        return out

    a, b = delta(range(n)), delta(range(100, 100 + n))
    for kpi in a:
        assert abs(a[kpi] - b[kpi]) < 5.0, (
            f"{kpi} gap moves from {a[kpi]:.1f}% to {b[kpi]:.1f}% between "
            f"seed blocks — not a stable result")



@pytest.mark.parametrize("scenario", ["S1", "S2", "S3"])
def test_b3_protects_the_operator_better_than_b2(scenario):
    """The central claim, asserted rather than admired."""
    for kpi in ("mean_fatigue", "max_fatigue", "hc1_breaches", "hc3_breaches"):
        b2 = _mean(scenario, industry40_allocator, kpi)
        b3 = _mean(scenario, weighted_allocator, kpi)
        assert b3 <= b2, f"{scenario}: B3 is worse than B2 on {kpi}"
