"""
T7.6b — fatigue-rate sensitivity. The GATE 3 carry-over (design §4.5).

lambda and mu set how fast an operator tires and recovers. They are calibrated,
not measured: the exponential form comes from Calzavara et al. (2019), the two
numbers do not appear there or anywhere else. The condition attached to using
them was that the conclusion must survive being wrong about them.

So both rates are scaled together by 0.5, 1 and 2 — a fourfold span — and the
question asked at each is not whether the numbers move (they will) but whether
the ORDERING of the two policies moves. If the proposed framework beats the
Industry 4.0 baseline on the human measures at every scaling, the finding is
about the framework. If the ordering flips, it was about the calibration.

Scaling both together preserves mu > lambda, which the design requires.

Run:  python src/sensitivity_fatigue.py
Writes results/sensitivity_fatigue.csv
"""

from __future__ import annotations

import sys
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

ALLOCATORS = {"B2": industry40_allocator, "B3": weighted_allocator}

# Lower is better for every one of these.
HUMAN_KPIS = ["mean_fatigue", "max_fatigue", "mean_rula",
              "constraint_violations"]


def scaled_setup(scenario: str, factor: float) -> Setup:
    setup = load_setup(scenario)
    f = setup.cfg["fatigue"]
    f["lambda_per_min"] *= factor
    f["mu_per_min"] *= factor
    return setup


def run_cell(scenario: str, baseline: str, factor: float,
             seeds: int | None = None) -> dict:
    setup = scaled_setup(scenario, factor)
    n = seeds if seeds is not None else setup.cfg["experiment"]["seeds"]
    rows = [run_shift(setup, seed=s, allocator=ALLOCATORS[baseline])
            for s in range(n)]
    keys = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
    return {k: sum(r[k] for r in rows) / n for k in keys}


def main() -> None:
    cfg = load_setup("S1").cfg
    factors = cfg["sensitivity"]["fatigue_rate_scalings"]
    scenario = cfg["sensitivity"]["fatigue_scenario"]
    seeds = cfg["experiment"]["seeds"]

    print(f"=== T7.6b · fatigue-rate sensitivity · scenario {scenario} "
          f"· {seeds} seeds ===")
    print(f"    lambda and mu scaled by {factors} — a "
          f"{max(factors) / min(factors):.0f}-fold span")
    print(f"    question: does the ORDERING of B2 and B3 move?")
    print()
    print(f"  {'scale':>6s} {'pol':>4s} {'meanF':>7s} {'maxF':>7s} "
          f"{'RULA':>6s} {'viol':>7s} {'thru':>7s} {'rest':>6s}")

    records, verdicts = [], []
    for factor in factors:
        cells = {b: run_cell(scenario, b, factor) for b in ALLOCATORS}
        for b, r in cells.items():
            records.append({"scenario": scenario, "scaling": factor,
                            "baseline": b, **r})
            print(f"  {factor:6.1f} {b:>4s} {r['mean_fatigue']:7.3f} "
                  f"{r['max_fatigue']:7.3f} {r['mean_rula']:6.2f} "
                  f"{r['constraint_violations']:7.1f} {r['throughput']:7.1f} "
                  f"{r['rest_episodes']:6.1f}")

        held = all(cells["B3"][k] <= cells["B2"][k] for k in HUMAN_KPIS)
        verdicts.append(held)
        print(f"  {'':6s} {'':4s} ranking {'holds' if held else 'FLIPPED'}"
              f"   fatigue {(cells['B3']['mean_fatigue'] - cells['B2']['mean_fatigue']) / cells['B2']['mean_fatigue'] * 100:+.1f}%"
              f"   throughput {(cells['B3']['throughput'] - cells['B2']['throughput']) / cells['B2']['throughput'] * 100:+.1f}%")
        print()

    out = ROOT / "results" / "sensitivity_fatigue.csv"
    pd.DataFrame(records).to_csv(out, index=False)

    if all(verdicts):
        print("  VERDICT: the ordering holds across a fourfold span of the")
        print("  calibrated rates. The conclusion is about the framework, not")
        print("  about the values chosen for lambda and mu.")
        print()
        print("  Wording for the paper:")
        print("    \"Under a fourfold variation of the fatigue accumulation and")
        print("     recovery rates, the ranking of the proposed framework over")
        print("     the machine-only baseline was preserved on every")
        print("     human-centric measure.\"")
    else:
        print("  VERDICT: the ordering flips. The result depends on the")
        print("  calibrated rates and cannot be reported as it stands.")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
