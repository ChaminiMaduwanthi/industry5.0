"""
HC1 threshold sensitivity — the check that answers "why 0.80?".

0.80 is a safety margin chosen for this study. The quantity it is a fraction of
(the acceptable work level) comes from Price (1990), but the fraction itself
appears in no publication. That is the same situation as the fatigue rates, and
it gets the same treatment: keep the value, declare it calibrated, and show the
conclusion does not depend on it.

Pass criterion: at EVERY threshold, the constrained policy must still beat the
unconstrained one on every human-centric measure. If the ranking flips
somewhere, 0.80 is doing the work and the result is an artefact of it.

Run:  python src/sensitivity_hc1.py
Writes results/sensitivity_hc1.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import load_setup                              # noqa: E402
from simulation.factory import (                           # noqa: E402
    random_allocator, run_shift, weighted_allocator,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SEEDS = 30

# Lower is better for all of these — they are the human cost of the shift.
HUMAN_KPIS = ["mean_fatigue", "max_fatigue", "hc1_breaches",
              "mean_rula", "hc3_breaches"]


def run(scenario: str, allocator, hc1: float | None) -> dict:
    setup = load_setup(scenario)
    if hc1 is not None:
        setup.cfg["constraints"]["hard"]["HC1_fatigue_max"] = hc1
        setup.cfg["constraints"]["hc1_hysteresis"]["enter_rest_at"] = hc1
        setup.cfg["constraints"]["hc1_hysteresis"]["leave_rest_at"] = hc1 - 0.20

    rows = [run_shift(setup, seed=s, allocator=allocator) for s in range(SEEDS)]
    keys = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
    return {k: sum(r[k] for r in rows) / SEEDS for k in keys}


def main() -> None:
    cfg = load_setup("S1").cfg
    thresholds = cfg["sensitivity"]["hc1_thresholds"]
    default = cfg["constraints"]["hard"]["HC1_fatigue_max"]

    print("=== HC1 sensitivity — does the conclusion depend on 0.80? ===")
    print(f"    {SEEDS} seeds per cell · unconstrained (B1) vs constrained (B3a)")
    print()

    records, verdicts = [], []

    for scenario in ("S1", "S2", "S3"):
        base = run(scenario, random_allocator, None)   # policy ignores HC1
        records.append({"scenario": scenario, "policy": "B1_unconstrained",
                        "hc1": None, **base})

        print(f"  {scenario}")
        print(f"    {'policy':22s} {'meanF':>7s} {'maxF':>7s} {'HC1!':>7s} "
              f"{'RULA':>6s} {'HC3!':>7s} {'thru':>7s}")
        print(f"    {'B1 unconstrained':22s} {base['mean_fatigue']:7.3f} "
              f"{base['max_fatigue']:7.3f} {base['hc1_breaches']:7.1f} "
              f"{base['mean_rula']:6.2f} {base['hc3_breaches']:7.1f} "
              f"{base['throughput']:7.1f}")

        for hc1 in thresholds:
            r = run(scenario, weighted_allocator, hc1)
            records.append({"scenario": scenario, "policy": "B3a_constrained",
                            "hc1": hc1, **r})

            better = all(r[k] <= base[k] for k in HUMAN_KPIS)
            verdicts.append(better)
            mark = "  better on all" if better else "  <-- RANKING FLIPPED"
            star = " *" if hc1 == default else "  "
            print(f"    {'B3a  HC1 = ' + f'{hc1:.2f}' + star:22s} "
                  f"{r['mean_fatigue']:7.3f} {r['max_fatigue']:7.3f} "
                  f"{r['hc1_breaches']:7.1f} {r['mean_rula']:6.2f} "
                  f"{r['hc3_breaches']:7.1f} {r['throughput']:7.1f}{mark}")
        print()

    out = ROOT / "results" / "sensitivity_hc1.csv"
    pd.DataFrame(records).to_csv(out, index=False)

    print("  * = the default threshold")
    print()
    if all(verdicts):
        print("  VERDICT: the constrained policy wins on every human measure at")
        print("  every threshold tested. The conclusion does not rest on 0.80.")
    else:
        print("  VERDICT: the ranking flips somewhere — 0.80 IS doing the work.")
        print("  The result would be an artefact of the threshold.")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
