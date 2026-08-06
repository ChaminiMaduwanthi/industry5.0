"""
How much room the objective actually has (supports §V.E.1).

The weight study found the four configurations indistinguishable and gave the
reason as a feasible set that is usually empty or a singleton. That reason was
written into the narrative as "95.8% of decisions" without being computed from
anything — a literal in a print statement, reproducible by nobody. This
measures it.

Every call to the decision layer reports two things: how many admissible
options it had after the hard filter, and the spread between the best and
worst score among them. From those:

    - the share of decisions with nothing to choose between (0 or 1 option)
    - among the rest, the median gap the weights are competing over

Neither number can be improved by tuning; they are properties of how tightly
the constraints bind. That is the point of measuring them.

Run:  python src/decision_pressure.py
Writes results/decision_pressure.csv
"""

from __future__ import annotations

import statistics
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import load_setup                                 # noqa: E402
from simulation.factory import run_shift, weighted_allocator  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHIFTS = 30          # the evaluation seed block, as the KPI table uses
SCENARIOS = ("S1", "S2", "S3")


def measure(scenario: str, shifts: int = SHIFTS) -> dict:
    setup = load_setup(scenario)
    sizes: list[int] = []
    spreads: list[float] = []

    def probe(n_options: int, spread: float | None) -> None:
        sizes.append(n_options)
        if spread is not None:
            spreads.append(spread)

    for seed in range(shifts):
        run_shift(setup, seed=seed, allocator=weighted_allocator,
                  on_epoch=_attach(probe))

    n = len(sizes)
    constrained = sum(1 for s in sizes if s <= 1)
    return {
        "scenario": scenario,
        "shifts": shifts,
        "decisions": n,
        "no_choice": constrained,
        "share_no_choice": round(constrained / n, 4) if n else 0.0,
        "share_with_choice": round(1 - constrained / n, 4) if n else 0.0,
        "median_options": statistics.median(sizes) if sizes else 0,
        "max_options": max(sizes) if sizes else 0,
        "median_spread": round(statistics.median(spreads), 4) if spreads else 0.0,
        "mean_spread": round(statistics.fmean(spreads), 4) if spreads else 0.0,
        "max_spread": round(max(spreads), 4) if spreads else 0.0,
    }


def _attach(probe):
    """Hang the probe on the state the first time an epoch is observed.

    run_shift builds its own state, so there is no earlier hook; on_epoch fires
    before the first dispatch it needs to cover, which is why this works.
    """
    def on_epoch(state):
        if getattr(state, "decision_probe", None) is None:
            state.decision_probe = probe
    return on_epoch


def main() -> None:
    print("=== how much room does the objective have? ===")
    print(f"    {SHIFTS} shifts per scenario, every call to the decision layer")
    print()
    print(f"  {'scen':6s} {'decisions':>10s} {'0 or 1 option':>15s} "
          f"{'median opts':>12s} {'median spread':>15s} {'max spread':>12s}")

    rows = []
    for scenario in SCENARIOS:
        r = measure(scenario)
        rows.append(r)
        print(f"  {r['scenario']:6s} {r['decisions']:10d} "
              f"{r['share_no_choice']:14.1%} {r['median_options']:12.0f} "
              f"{r['median_spread']:15.4f} {r['max_spread']:12.4f}")

    out = ROOT / "results" / "decision_pressure.csv"
    pd.DataFrame(rows).to_csv(out, index=False)

    s2 = next(r for r in rows if r["scenario"] == "S2")
    print()
    print(f"  S2, the scenario §V reports: {s2['share_no_choice']:.1%} of decisions")
    print(f"  have nothing to choose between. In the remaining "
          f"{s2['share_with_choice']:.1%} the")
    print(f"  best and worst admissible option differ by a median of "
          f"{s2['median_spread']:.3f}")
    print(f"  on the objective's own scale.")
    print()
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
