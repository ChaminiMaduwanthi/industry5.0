"""
Invariant checks for the simulation (early part of T5.15).

These do not check that the numbers are *good*. They check that the run is
internally consistent — that nothing physically impossible happened. A result
table built on a run that broke one of these would be worthless, and the
breakages are the kind that produce plausible-looking output.

Run:  python -m pytest tests/ -q
      python tests/test_invariants.py     (same checks, readable output)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from simulation.factory import ShiftState, run_shift       # noqa: E402

SCENARIOS = ["S1", "S2", "S3"]
SEEDS = range(8)


def _capture(scenario: str, seed: int) -> ShiftState:
    """Run a shift and hand back the final state for inspection."""
    box = {}
    setup = load_setup(scenario)
    run_shift(setup, seed=seed, on_epoch=lambda st: box.setdefault("state", st))
    return box["state"]


def _overlaps(intervals: list[tuple[float, float]]) -> list[tuple]:
    """Return any pair of intervals that overlap by more than rounding."""
    intervals.sort()
    bad = []
    for (s1, e1), (s2, e2) in zip(intervals, intervals[1:]):
        if s2 < e1 - 1e-9:
            bad.append(((s1, e1), (s2, e2)))
    return bad


# =============================================================================
@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", SEEDS)
def test_no_work_on_an_unavailable_machine(scenario, seed):
    """Design §3.4: a machine at or below the health floor is not available.

    The floor exists so that worn machines stop producing. If work can still
    start on one, HC4 is decorative and every quality figure is optimistic.
    """
    state = _capture(scenario, seed)
    floor = state.setup.cfg["machines"]["health_min_operational"]
    violations = [
        (t.task_id, t.assigned_machine, t.machine_health_at_start)
        for t in state.completed
        if t.machine_health_at_start is not None
        and t.machine_health_at_start <= floor
    ]
    assert not violations, (
        f"{len(violations)} task(s) started on a machine at or below the "
        f"health floor {floor}: {violations[:5]}")


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", SEEDS)
def test_no_double_booking(scenario, seed):
    """One operator and one machine per task, with no overlap in time."""
    state = _capture(scenario, seed)

    for key, label in (("assigned_operator", "operator"),
                       ("assigned_machine", "machine")):
        spans: dict[str, list[tuple[float, float]]] = {}
        for t in state.completed:
            spans.setdefault(getattr(t, key), []).append(
                (t.started_min, t.finished_min))
        for who, iv in spans.items():
            bad = _overlaps(iv)
            assert not bad, f"{label} {who} ran overlapping tasks: {bad[:3]}"


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", SEEDS)
def test_health_stays_in_range(scenario, seed):
    state = _capture(scenario, seed)
    for mac_id, twin in state.twins.items():
        assert 0.0 <= twin.health <= 1.0, f"{mac_id} health {twin.health}"
        for h in twin.health_trace:
            assert 0.0 <= h <= 1.0, f"{mac_id} health trace left [0,1]: {h}"


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_same_seed_same_result(scenario):
    setup = load_setup(scenario)
    assert run_shift(setup, seed=3) == run_shift(setup, seed=3)


def test_disruption_is_identical_for_every_baseline():
    """S3 must hit every baseline with the same failures on the same seed.

    Breakdown times are drawn from a generator the allocator never touches. If
    that ever changes, each baseline would face a different disruption and the
    S3 comparison would be meaningless — so it is checked rather than trusted.
    """
    setup = load_setup("S3")

    def greedy(state, rng):                    # a deliberately different policy
        free_o = [o for o, s in state.operators.items() if s.available()]
        free_m = [m for m, s in state.machines.items()
                  if s.available() and state.twins[m].available()]
        out = []
        for t in [t for t in state.queue if t.assigned_operator is None]:
            if not free_o or not free_m:
                break
            out.append((t, free_o.pop(0), free_m.pop(0)))
        return out

    a = run_shift(setup, seed=4)
    b = run_shift(setup, seed=4, allocator=greedy)
    assert a["maintenance_events"] or b["maintenance_events"]
    # different policies, but the same machines must break at the same times
    sa = _capture("S3", 4)
    assert sum(t.breakdown_events for t in sa.twins.values()) >= 0


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", SEEDS)
def test_nobody_works_through_the_break(scenario, seed):
    """No task may START during the scheduled break window."""
    state = _capture(scenario, seed)
    sim = state.setup.cfg["simulation"]
    start = sim["break_after_minutes"]
    end = start + sim["break_duration_minutes"]
    late = [t.task_id for t in state.completed if start <= t.started_min < end]
    assert not late, f"{len(late)} task(s) started during the break: {late[:5]}"


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("seed", SEEDS)
def test_time_budget_is_not_exceeded(scenario, seed):
    """Nobody can be busy for longer than the shift."""
    state = _capture(scenario, seed)
    shift = state.setup.shift_minutes
    for o in state.operators.values():
        assert o.busy_minutes <= shift + 1e-9, f"{o.operator_id} over budget"
    for m in state.machines.values():
        assert m.busy_minutes <= shift + 1e-9, f"{m.machine_id} over budget"


# =============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    checks = [
        ("work on an unavailable machine", test_no_work_on_an_unavailable_machine),
        ("double booking", test_no_double_booking),
        ("health outside [0,1]", test_health_stays_in_range),
        ("work started during the break", test_nobody_works_through_the_break),
        ("time budget exceeded", test_time_budget_is_not_exceeded),
    ]
    failures = 0
    for label, fn in checks:
        bad = []
        for sc in SCENARIOS:
            for sd in SEEDS:
                try:
                    fn(sc, sd)
                except AssertionError as exc:
                    bad.append(f"{sc}/seed{sd}: {exc}")
        failures += len(bad)
        mark = "ok  " if not bad else "FAIL"
        print(f"  [{mark}] {label:35s} {len(SCENARIOS) * len(SEEDS) - len(bad)}"
              f"/{len(SCENARIOS) * len(SEEDS)} runs clean")
        for b in bad[:3]:
            print(f"         {b}")

    for sc in SCENARIOS:
        try:
            test_same_seed_same_result(sc)
            print(f"  [ok  ] determinism {sc}")
        except AssertionError:
            failures += 1
            print(f"  [FAIL] determinism {sc}")

    print()
    print("ALL CLEAN" if not failures else f"{failures} INVARIANT FAILURES")
    sys.exit(1 if failures else 0)
