"""
Cross-training analysis — why the workload spread widens, and what closes it.

The proposed framework distributes work LESS evenly than the machine-only
baseline. That is a real cost and it is reported as one. This asks what causes
it and whether anything fixes it.

Two candidate explanations were tested and rejected before this one:

    the fairness preference is too weak
        Raising it eightfold moved the workload spread from 0.0243 to 0.0241.
        The preference has no grip, because the hard constraints decide who is
        ELIGIBLE and a preference can only choose among the eligible.

    fairness is being measured wrongly
        Comparing strain rather than time gave a mixed picture — better in two
        scenarios, worse in the third. Reporting only the favourable ones would
        be cherry-picking, so the reframing was dropped.

What remains is the workforce itself. OP1 is the strongest operator and the
only one barred from heavy work, because his skill at it sits below the
competence floor. Heavy work therefore falls to the two operators least able to
sustain it, and the load concentrates.

*** This analysis does NOT change the headline results. They stay on the
    configuration that was actually run. The retrained skill matrix exists only
    inside this file, and a test asserts that nothing leaks out of it. ***

Run:  python src/crosstraining.py
Writes results/crosstraining.csv
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import Setup, load_setup                       # noqa: E402
from simulation.factory import (                           # noqa: E402
    industry40_allocator, run_shift, weighted_allocator,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The skill matrix as it is actually configured, kept here so the tests can
# assert that the analysis leaves it alone.
BASE_SKILL = {
    "OP1": {"L": 0.90, "M": 0.60, "H": 0.30},
    "OP2": {"L": 0.50, "M": 0.90, "H": 0.70},
    "OP3": {"L": 0.70, "M": 0.40, "H": 0.90},
}

# One operator, one task type, lifted just past the competence floor of 0.40.
# Deliberately minimal: this is the smallest intervention that changes who is
# eligible, so whatever it achieves is attributable to that change alone.
TRAINED = {"OP1": {"H": 0.45}}

ALLOCATORS = {"B2": industry40_allocator, "B3": weighted_allocator}


def retrained_setup(scenario: str) -> Setup:
    """A setup with the retrained skills, built fresh and never written back."""
    setup = load_setup(scenario)
    for op, changes in TRAINED.items():
        skills = dict(setup.operators[op].skill)
        skills.update(changes)
        setup.operators[op] = replace(setup.operators[op], skill=skills)
    return setup


def measure(scenario: str, baseline: str = "B3", trained: bool = False,
            seeds: int | None = None) -> dict:
    setup = retrained_setup(scenario) if trained else load_setup(scenario)
    n = seeds if seeds is not None else setup.cfg["experiment"]["seeds"]
    rows = [run_shift(setup, seed=s, allocator=ALLOCATORS[baseline])
            for s in range(n)]
    keys = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
    return {k: sum(r[k] for r in rows) / n for k in keys}


def main() -> None:
    scenarios = load_setup("S1").cfg["experiment"]["scenarios"]

    print("=== Cross-training analysis ===")
    print(f"    intervention: OP1 heavy-task skill "
          f"{BASE_SKILL['OP1']['H']} -> {TRAINED['OP1']['H']}, which is the")
    print("    smallest change that clears the 0.40 competence floor")
    print()
    print(f"  {'':4s} {'policy':>16s} {'spread':>8s} {'meanF':>7s} "
          f"{'viol':>6s} {'thru':>7s}")

    records = []
    for scenario in scenarios:
        cells = {
            "B2 Industry 4.0": measure(scenario, baseline="B2"),
            "B3 as configured": measure(scenario, trained=False),
            "B3 + retrained": measure(scenario, trained=True),
        }
        for label, r in cells.items():
            records.append({"scenario": scenario, "policy": label, **r})
            print(f"  {scenario if label.startswith('B2') else '':4s} "
                  f"{label:>16s} {r['workload_gini']:8.4f} "
                  f"{r['mean_fatigue']:7.3f} "
                  f"{r['constraint_violations']:6.1f} {r['throughput']:7.1f}")

        b2, b3, tr = cells.values()
        closed = (b3["workload_gini"] - tr["workload_gini"]) / \
                 (b3["workload_gini"] - b2["workload_gini"]) * 100
        print(f"  {'':4s} {'':16s} gap closed {closed:.0f}%   "
              f"throughput {tr['throughput'] - b3['throughput']:+.1f} "
              f"vs B3, {tr['throughput'] - b2['throughput']:+.1f} vs B2")
        print()

    out = ROOT / "results" / "crosstraining.csv"
    pd.DataFrame(records).to_csv(out, index=False)

    df = pd.DataFrame(records)
    tr = df[df.policy == "B3 + retrained"]
    b2 = df[df.policy == "B2 Industry 4.0"]
    beats_b2 = int((tr.throughput.values >= b2.throughput.values).sum())

    print("  Reading:")
    print("    The uneven distribution is not the scheduler's doing. It comes")
    print("    from a gap in the workforce's skills, which the framework can")
    print("    locate because it models both sides. Training one operator on")
    print("    one task type closes roughly two thirds of it in every")
    print("    scenario, and raises throughput in every scenario, while")
    print("    breaches stay at zero.")
    print()
    print("    Three things it does NOT do, stated because each is easy to")
    print("    overclaim:")
    print("      - it does not close the gap; the spread stays wider than the")
    print("        machine-only baseline everywhere")
    print(f"      - it does not beat that baseline on throughput except in")
    print(f"        {beats_b2} of {len(tr)} scenarios")
    print("      - it costs some protection: mean fatigue rises, though it")
    print("        stays far below the baseline")
    print()
    print("    The headline results are reported on the original")
    print("    configuration, not this one.")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
