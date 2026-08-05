"""
T6.5 / T6.6 — the experiment matrix (experiment-plan §6).

    3 baselines  x  3 scenarios  x  30 seeds  =  270 runs

Everything the paper reports comes out of this file, so it is deliberately
dull: no analysis, no filtering, no cleverness. Run the matrix, write every
row, and leave interpretation to analyse_results.py.

    B1  random assignment          no twin state consulted, no constraints
    B2  Industry 4.0               full machine twin, throughput only,
                                   blind to the operator
    B3  proposed (weighted sum)    both twins, all five couplings,
                                   HC1-HC4 filtering before the optimiser

One seed means the same order book and the same breakdowns for all three, so
differences between rows come from the policy and nothing else.

Run:  python src/run_experiments.py
Writes results/raw_results.csv
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import load_setup                              # noqa: E402
from simulation.factory import (                           # noqa: E402
    industry40_allocator, random_allocator, run_shift, weighted_allocator,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASELINES = {
    "B1": random_allocator,
    "B2": industry40_allocator,
    "B3": weighted_allocator,
}

# experiment-plan §6. Anything else the simulation reports is carried through
# as well, but these are the columns the tables are built from.
CORE_COLUMNS = [
    "run_id", "scenario", "baseline", "seed",
    "mean_fatigue", "max_fatigue", "mean_rula", "workload_gini",
    "energy_kwh", "energy_per_unit", "co2e_kg", "scrap_rate",
    "throughput", "downtime_hrs", "oee",
    "constraint_violations", "runtime_sec",
]


def run_one(scenario: str, baseline: str, seed: int) -> dict:
    """One cell of the matrix."""
    started = time.perf_counter()
    result = run_shift(load_setup(scenario), seed=seed,
                       allocator=BASELINES[baseline])
    elapsed = time.perf_counter() - started

    return {
        "run_id": f"{scenario}_{baseline}_s{seed:02d}",
        "scenario": scenario,
        "baseline": baseline,
        "seed": seed,
        **{k: v for k, v in result.items()
           if k not in ("scenario", "seed")},
        "runtime_sec": round(elapsed, 4),
    }


def build_matrix(seeds: int | None = None, progress: bool = True
                 ) -> pd.DataFrame:
    cfg = load_setup("S1").cfg
    scenarios = cfg["experiment"]["scenarios"]
    n_seeds = seeds if seeds is not None else cfg["experiment"]["seeds"]

    rows, total = [], len(scenarios) * len(BASELINES) * n_seeds
    for scenario in scenarios:
        for baseline in BASELINES:
            for seed in range(n_seeds):
                rows.append(run_one(scenario, baseline, seed))
            if progress:
                print(f"  {scenario} / {baseline}: {n_seeds} runs "
                      f"({len(rows)}/{total})")

    df = pd.DataFrame(rows)
    # Stable column order: the named columns first, the rest behind them.
    ordered = CORE_COLUMNS + [c for c in df.columns if c not in CORE_COLUMNS]
    return df[ordered]


def summarise(df: pd.DataFrame) -> None:
    print()
    print("=== means over the matrix ===")
    print(f"  {'scen':5s} {'pol':4s} {'thru':>7s} {'meanF':>7s} {'maxF':>7s} "
          f"{'RULA':>6s} {'viol':>6s} {'scrap':>7s} {'kWh/u':>7s} {'OEE':>6s}")
    for scenario, group in df.groupby("scenario", sort=False):
        for baseline, cell in group.groupby("baseline", sort=False):
            m = cell.mean(numeric_only=True)
            print(f"  {scenario:5s} {baseline:4s} {m.throughput:7.1f} "
                  f"{m.mean_fatigue:7.3f} {m.max_fatigue:7.3f} "
                  f"{m.mean_rula:6.2f} {m.constraint_violations:6.1f} "
                  f"{m.scrap_rate:7.3f} {m.energy_per_unit:7.3f} {m.oee:6.3f}")

    print()
    print("=== B3 against B2 ===")
    for scenario, group in df.groupby("scenario", sort=False):
        b2 = group[group.baseline == "B2"].mean(numeric_only=True)
        b3 = group[group.baseline == "B3"].mean(numeric_only=True)
        d = lambda k: (b3[k] - b2[k]) / b2[k] * 100 if b2[k] else 0.0
        print(f"  {scenario}: fatigue {d('mean_fatigue'):+6.1f}%  "
              f"RULA {d('mean_rula'):+6.1f}%  scrap {d('scrap_rate'):+6.1f}%  "
              f"energy/unit {d('energy_per_unit'):+6.1f}%  |  "
              f"throughput {d('throughput'):+6.1f}%")


def main() -> None:
    cfg = load_setup("S1").cfg
    n = len(cfg["experiment"]["scenarios"]) * len(BASELINES) * cfg["experiment"]["seeds"]
    print(f"=== running the experiment matrix: {n} runs ===")

    started = time.perf_counter()
    df = build_matrix()
    elapsed = time.perf_counter() - started

    out = ROOT / "results" / cfg["experiment"]["output_csv"].split("/")[-1]
    df.to_csv(out, index=False)

    summarise(df)
    print()
    print(f"  {len(df)} runs in {elapsed:.1f} s "
          f"({elapsed / len(df) * 1000:.0f} ms each)")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
