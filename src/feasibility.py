"""
T5.16 — the GATE 3 carry-over feasibility check (design §12).

The concern behind it: hard constraints that filter before the optimiser can in
principle empty the candidate set, leaving work stalled with people and
machines standing free. Design §12 asks for the deferral rate to be measured
over 640 epochs — twenty shifts — before the framework is trusted, and sets the
threshold at 15%: above that, either HC1 is relaxed to 0.85 or the operator
profiles are reconsidered, and whichever is chosen must be recorded.

Run:  python src/feasibility.py
Writes results/feasibility.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from loader import load_setup                              # noqa: E402
from simulation.factory import run_shift, weighted_allocator  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHIFTS = 20          # 20 shifts x 32 epochs = 640 epochs, as design §12 asks


def measure(scenario: str, hc1: float | None = None) -> dict:
    setup = load_setup(scenario)
    if hc1 is not None:
        setup.cfg["constraints"]["hard"]["HC1_fatigue_max"] = hc1
        setup.cfg["constraints"]["hc1_hysteresis"]["enter_rest_at"] = hc1

    rows = [run_shift(setup, seed=s, allocator=weighted_allocator)
            for s in range(SHIFTS)]
    epochs = SHIFTS * setup.epochs_per_shift
    deferrals = sum(r["deferral_epochs"] for r in rows)

    return {
        "scenario": scenario,
        "hc1_threshold": hc1 if hc1 is not None
        else setup.cfg["constraints"]["hard"]["HC1_fatigue_max"],
        "shifts": SHIFTS,
        "epochs": epochs,
        "deferral_epochs": deferrals,
        "deferral_rate": round(deferrals / epochs, 4),
        "throughput": round(sum(r["throughput"] for r in rows) / SHIFTS, 2),
        "unfinished": round(sum(r["unfinished"] for r in rows) / SHIFTS, 2),
        "mean_fatigue": round(sum(r["mean_fatigue"] for r in rows) / SHIFTS, 4),
        "max_fatigue": round(max(r["max_fatigue"] for r in rows), 4),
        "hc1_breaches": sum(r["hc1_breaches"] for r in rows),
    }


def main() -> None:
    setup = load_setup("S1")
    threshold = setup.cfg["constraints"]["deferral_rate_threshold"]
    default_hc1 = setup.cfg["constraints"]["hard"]["HC1_fatigue_max"]

    rows = []
    print(f"=== T5.16 feasibility · {SHIFTS} shifts per cell "
          f"({SHIFTS * setup.epochs_per_shift} epochs) ===")
    print(f"    design §12 threshold: deferral rate must stay under "
          f"{threshold:.0%}")
    print()
    print(f"  {'scen':5s} {'HC1':>5s} {'defer':>7s} {'rate':>7s} "
          f"{'thru':>7s} {'unfin':>7s} {'meanF':>7s} {'maxF':>6s} {'HC1!':>5s}")

    for hc1 in (default_hc1, 0.85):
        for scenario in ("S1", "S2", "S3"):
            r = measure(scenario, hc1)
            rows.append(r)
            flag = "" if r["deferral_rate"] <= threshold else "  <- over"
            print(f"  {r['scenario']:5s} {r['hc1_threshold']:5.2f} "
                  f"{r['deferral_epochs']:7d} {r['deferral_rate']:7.1%} "
                  f"{r['throughput']:7.1f} {r['unfinished']:7.1f} "
                  f"{r['mean_fatigue']:7.3f} {r['max_fatigue']:6.3f} "
                  f"{r['hc1_breaches']:5d}{flag}")

    df = pd.DataFrame(rows)
    out = ROOT / "results" / "feasibility.csv"
    df.to_csv(out, index=False)

    worst = df[df.hc1_threshold == default_hc1].deferral_rate.max()
    print()
    print(f"  worst deferral rate at HC1 = {default_hc1}: {worst:.1%}")
    print(f"  {'WITHIN' if worst <= threshold else 'OVER'} the "
          f"{threshold:.0%} threshold")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
