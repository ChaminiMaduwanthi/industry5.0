"""
T5.16 — which constraint actually causes the deferrals, and what to do about it.

`feasibility.py` measured the deferral rate design §12 asks for and found it
over the 15% guard in two scenarios of three. §12 offers two remedies: relax
HC1 to 0.85, or reconsider the operator profiles. Both were measured and
NEITHER brings S1 under the guard — 24.4% falls only to 20.0% and 20.8%.

So the remedy cannot be chosen until the cause is known, and the cause cannot
be read off the filtered-candidate counts: those count how many (task,
operator, machine) triples each constraint rejected, which is not the same as
which constraint left the set empty. A constraint can reject thousands of
triples and never once be the last one standing.

This measures it directly instead. Each hard constraint is removed on its own
and the deferral rate re-measured. Whichever removal moves the rate is the one
that was closing the set; the safety cost of that removal is reported in the
same row, because a remedy that eliminates deferrals by allowing breaches is
not a remedy.

Run:  python src/deferral_diagnosis.py
Writes results/deferral_diagnosis.csv
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import Setup, load_setup                          # noqa: E402
from simulation.factory import run_shift, weighted_allocator  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHIFTS = 20          # 20 x 32 = 640 epochs, the window design §12 specifies
SCENARIOS = ("S1", "S2", "S3")

# Breaches are counted against ONE fixed yardstick, whatever threshold the row
# was actually run with — the same correction sensitivity_hc1.py needed. The
# in-simulation counters compare against the threshold in force, so a run with
# the fatigue limit removed reports zero breaches of a limit it does not have
# and looks perfectly safe. Both numbers are kept: the reference count is what
# the comparison uses, the own-threshold count is what the run enforced.
REFERENCE_FATIGUE = 0.80
REFERENCE_RULA = 5

# The configured skill matrix, repeated here so the tests can assert that this
# analysis leaves the real one alone.
BASE_SKILL = {
    "OP1": {"L": 0.90, "M": 0.60, "H": 0.30},
    "OP2": {"L": 0.50, "M": 0.90, "H": 0.70},
    "OP3": {"L": 0.70, "M": 0.40, "H": 0.90},
}

# Lifting one operator's one skill just past the floor — the smallest change
# that alters who is eligible, so whatever it achieves is attributable to it.
TRAINED = {"OP1": {"H": 0.45}}

# A threshold set outside the range of the quantity it bounds disables the
# constraint without touching any code path.
CONDITIONS: dict[str, dict] = {
    "configured":     {"label": "as configured"},
    "HC1 off":        {"label": "no fatigue limit",     "hc1": 1.01},
    "HC2 off":        {"label": "no competence floor",  "hard": {"HC2_skill_min": 0.0}},
    "HC3 off":        {"label": "no ergonomic ceiling", "hard": {"HC3_rula_max": 7}},
    "HC4 off":        {"label": "no health floor",      "hard": {"HC4_health_min": 0.0}},
    "HC1 -> 0.85":    {"label": "§12 remedy A",         "hc1": 0.85},
    "OP1 trained":    {"label": "§12 remedy B",         "trained": True},
    "both remedies":  {"label": "§12 A + B",            "hc1": 0.85, "trained": True},
}


def build_setup(scenario: str, condition: str) -> Setup:
    """A fresh setup with one condition applied. Never written back to disk."""
    spec = CONDITIONS[condition]
    setup = load_setup(scenario)

    # HC1 and the hysteresis entry point are the same number (the loader
    # asserts it), so they move together or the next load fails.
    if "hc1" in spec:
        setup.cfg["constraints"]["hard"]["HC1_fatigue_max"] = spec["hc1"]
        setup.cfg["constraints"]["hc1_hysteresis"]["enter_rest_at"] = spec["hc1"]
        # Keep the band width constant, as the HC1 sweep does, so a change in
        # the threshold is not confounded with a change in how long rests last.
        setup.cfg["constraints"]["hc1_hysteresis"]["leave_rest_at"] = spec["hc1"] - 0.20

    for key, value in spec.get("hard", {}).items():
        setup.cfg["constraints"]["hard"][key] = value

    if spec.get("trained"):
        for op, changes in TRAINED.items():
            skills = dict(setup.operators[op].skill)
            skills.update(changes)
            setup.operators[op] = replace(setup.operators[op], skill=skills)

    return setup


def measure(scenario: str, condition: str, shifts: int = SHIFTS) -> dict:
    setup = build_setup(scenario, condition)

    rows, ref_fatigue, ref_rula = [], [], []
    for seed in range(shifts):
        box: dict = {}
        rows.append(run_shift(setup, seed=seed, allocator=weighted_allocator,
                              on_epoch=lambda st: box.setdefault("s", st)))
        state = box["s"]
        ref_fatigue.append(sum(
            1 for h in state.humans.values()
            for f in h.fatigue_trace if f >= REFERENCE_FATIGUE))
        ref_rula.append(sum(
            1 for h in state.humans.values()
            for r in h.rula_samples if r > REFERENCE_RULA))

    epochs = shifts * setup.epochs_per_shift
    deferrals = sum(r["deferral_epochs"] for r in rows)

    def mean(key: str) -> float:
        return sum(r[key] for r in rows) / shifts

    return {
        "scenario": scenario,
        "condition": condition,
        "label": CONDITIONS[condition]["label"],
        "shifts": shifts,
        "epochs": epochs,
        "deferral_epochs": deferrals,
        "deferral_rate": round(deferrals / epochs, 4),
        "throughput": round(mean("throughput"), 2),
        "unfinished": round(mean("unfinished"), 2),
        "mean_fatigue": round(mean("mean_fatigue"), 4),
        # against the fixed yardstick — this is what the comparison uses
        "fatigue_breaches_vs_ref": int(sum(ref_fatigue)),
        "rula_breaches_vs_ref": int(sum(ref_rula)),
        # against whatever threshold the row itself enforced
        "hc1_breaches": int(sum(r["hc1_breaches"] for r in rows)),
        "hc3_breaches": int(sum(r["hc3_breaches"] for r in rows)),
        "hc1_filtered": int(sum(r["hc1_filtered"] for r in rows)),
        "hc2_filtered": int(sum(r["hc2_filtered"] for r in rows)),
        "hc3_filtered": int(sum(r["hc3_filtered"] for r in rows)),
        "hc4_filtered": int(sum(r["hc4_filtered"] for r in rows)),
    }


def queue_depth_at_deferral(shifts: int = SHIFTS) -> dict[str, dict]:
    """How much work was actually waiting when the feasible set closed.

    Asked because the scenario ordering looks wrong for a constraint-tightness
    reading: S2 carries half again the demand of S1 and defers half as often.
    The hypothesis was that deferrals cluster at a nearly empty queue, so the
    rate would be reporting queue thinness rather than constraint pressure.

    *** That hypothesis is wrong and is kept here because it was tested. ***
    The median queue at a deferral is 11, 24 and 18 tasks across the three
    scenarios and not one deferral in any scenario happens with two or fewer
    waiting. There is always plenty of work; none of it is legal.

    What the numbers do show is relative rather than absolute depletion. The
    queue at a deferral runs about a third of its depth at other epochs in
    every scenario, so deferrals gather in the part of the shift where the
    queue has drained down to a residue the available operators cannot take —
    which is the same story the constraint-removal table tells, seen from the
    queue's side.
    """
    print()
    print("  queue depth when the set closed (as configured):")
    print(f"  {'scen':6s} {'defer epochs':>13s} {'median':>8s} {'<=2 tasks':>11s} "
          f"{'mean queue':>11s} {'mean queue':>12s}")
    print(f"  {'':6s} {'':13s} {'':8s} {'':11s} {'when deferred':>11s} "
          f"{'otherwise':>12s}")

    summary = {}
    for scenario in SCENARIOS:
        setup = build_setup(scenario, "configured")
        deferred_depths, other_depths = [], []
        for seed in range(shifts):
            box: dict = {}
            run_shift(setup, seed=seed, allocator=weighted_allocator,
                      on_epoch=lambda st: box.setdefault("s", st))
            for e in box["s"].epoch_log:
                (deferred_depths if e["deferred"] else other_depths).append(
                    e["queue_pending"])

        depths = sorted(deferred_depths)
        n = len(depths)
        median = depths[n // 2] if n else 0
        shallow = sum(1 for d in depths if d <= 2) / n if n else 0.0
        summary[scenario] = {
            "deferral_epochs": n,
            "median_queue_when_deferred": median,
            "share_with_two_or_fewer": round(shallow, 4),
            "mean_queue_when_deferred": round(sum(depths) / n, 2) if n else 0.0,
            "mean_queue_otherwise": round(
                sum(other_depths) / len(other_depths), 2) if other_depths else 0.0,
        }
        s = summary[scenario]
        print(f"  {scenario:6s} {n:13d} {median:8d} {shallow:10.1%} "
              f"{s['mean_queue_when_deferred']:11.2f} "
              f"{s['mean_queue_otherwise']:12.2f}")

    ratios = [summary[s]["mean_queue_when_deferred"]
              / summary[s]["mean_queue_otherwise"] for s in SCENARIOS]
    print()
    print(f"  -> deferrals never happen on a near-empty queue (0% at <=2 "
          f"tasks), so the")
    print(f"     rate is not reporting queue thinness. The queue at a deferral "
          f"runs")
    print(f"     {min(ratios):.0%}-{max(ratios):.0%} of its usual depth: work is "
          f"waiting, none of it is legal.")

    pd.DataFrame(summary).T.rename_axis("scenario").to_csv(
        ROOT / "results" / "deferral_queue_depth.csv")
    return summary


def main() -> None:
    threshold = load_setup("S1").cfg["constraints"]["deferral_rate_threshold"]

    print(f"=== T5.16 · what closes the feasible set ===")
    print(f"    {SHIFTS} shifts per cell · design §12 guard: "
          f"deferral rate under {threshold:.0%}")
    print()
    print(f"  breaches are counted against the fixed reference "
          f"(fatigue {REFERENCE_FATIGUE}, RULA {REFERENCE_RULA}), not against "
          f"each row's own threshold")
    print()
    print(f"  {'condition':16s} {'label':22s} "
          + "".join(f"{s:>18s}" for s in SCENARIOS))
    print(f"  {'':16s} {'':22s}" + "".join(f"{'defer  thru  brch':>18s}"
                                           for _ in SCENARIOS))
    print("  " + "-" * 92)

    rows = []
    by_cell: dict[tuple[str, str], dict] = {}
    for condition, spec in CONDITIONS.items():
        cells = []
        for scenario in SCENARIOS:
            r = measure(scenario, condition)
            rows.append(r)
            by_cell[(condition, scenario)] = r
            breaches = r["fatigue_breaches_vs_ref"] + r["rula_breaches_vs_ref"]
            flag = "!" if breaches else " "
            cells.append(f"{r['deferral_rate']:6.1%} {r['throughput']:5.1f} "
                         f"{breaches:4d}{flag}")
        print(f"  {condition:16s} {spec['label']:22s}"
              + "".join(f"{c:>18s}" for c in cells))

    df = pd.DataFrame(rows)
    out = ROOT / "results" / "deferral_diagnosis.csv"
    df.to_csv(out, index=False)

    queue_depth_at_deferral()

    # --- read the result out loud rather than leaving it to the reader ------
    print()
    print("  effect of each removal on the deferral rate (percentage points):")
    print(f"  {'':16s}" + "".join(f"{s:>10s}" for s in SCENARIOS))
    for condition in CONDITIONS:
        if condition == "configured":
            continue
        deltas = []
        for scenario in SCENARIOS:
            base = by_cell[("configured", scenario)]["deferral_rate"]
            here = by_cell[(condition, scenario)]["deferral_rate"]
            deltas.append(f"{(here - base) * 100:+9.1f} ")
        print(f"  {condition:16s}" + "".join(deltas))

    print()
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
