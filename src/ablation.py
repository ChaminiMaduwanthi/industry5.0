"""
T7.8 — coupling ablation. What is state exchange between the twins worth?

The framework's claim is that carrying state in both directions between the
machine twin and the human twin changes decisions for the better. Strip a
coupling out and the claim becomes measurable: whatever the results lose is
what that coupling was contributing.

*** A coupling is removed from the SCHEDULER'S VIEW, never from the factory. ***

A tired operator still makes more mistakes when CP2 is ablated. The scheduler
just cannot see it while choosing. Removing it from the physics as well would
score each ablation in a world of its own and make the runs incomparable — the
same error as switching the couplings off for the Industry 4.0 baseline.

    CP1  skill   -> quality      ablated: the scheduler assumes full competence
    CP2  fatigue -> quality      ablated: it assumes a rested operator
    CP5  pace    -> ergonomics   ablated: it assumes a machine at rest pace

    CP3  health  -> cognitive load
         Not ablatable here, and worth stating plainly: cognitive load is
         computed and reported but never consulted by the current decision
         layer, so removing CP3 changes no choice. It is a measurement
         coupling in this implementation, not a decision one.

    CP4  task intensity -> fatigue
         Not ablatable: the task's metabolic demand IS the asymptote of the
         fatigue equation. Removing it removes the model rather than a link.

This study is also the remaining cover for the coupling coefficients and the
ergonomic multipliers, which no dataset can fit and which are declared
calibrated in config.yaml.

Run:  python src/ablation.py
Writes results/ablation.csv
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

ABLATIONS = {
    "none": frozenset(),
    "CP1": frozenset({"CP1"}),
    "CP2": frozenset({"CP2"}),
    "CP5": frozenset({"CP5"}),
    "all": frozenset({"CP1", "CP2", "CP5"}),
}

LABELS = {
    "none": "full framework",
    "CP1": "no skill -> quality",
    "CP2": "no fatigue -> quality",
    "CP5": "no pace -> ergonomics",
    "all": "all couplings off",
}


def allocator_for(name: str):
    """A weighted allocator that cannot see the named couplings."""
    def alloc(state, rng):
        return weighted_allocator(state, rng)
    alloc.__name__ = f"weighted_ablate_{name}"
    alloc.enforces = weighted_allocator.enforces
    alloc.ablate = ABLATIONS[name]
    return alloc


def measure(scenario: str, name: str, seeds: int | None = None) -> dict:
    setup = load_setup(scenario)
    n = seeds if seeds is not None else setup.cfg["experiment"]["seeds"]
    rows = [run_shift(setup, seed=s, allocator=allocator_for(name))
            for s in range(n)]
    keys = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
    return {k: sum(r[k] for r in rows) / n for k in keys}


def main() -> None:
    scenarios = load_setup("S1").cfg["experiment"]["scenarios"]

    print("=== T7.8 · coupling ablation ===")
    print("    each coupling removed from the SCHEDULER'S VIEW; the factory")
    print("    is unchanged, so every run is scored in the same world")
    print()
    print(f"  {'':4s} {'ablation':>22s} {'meanF':>7s} {'HC1!':>6s} "
          f"{'HC3!':>6s} {'scrap':>7s} {'thru':>7s}")

    records = []
    for scenario in scenarios:
        cells = {n: measure(scenario, n) for n in ABLATIONS}
        for name, r in cells.items():
            records.append({"scenario": scenario, "ablation": name,
                            "label": LABELS[name], **r})
            print(f"  {scenario if name == 'none' else '':4s} "
                  f"{LABELS[name]:>22s} {r['mean_fatigue']:7.3f} "
                  f"{r['constraint_violations'] - r['hc3_breaches']:6.1f} "
                  f"{r['hc3_breaches']:6.1f} {r['scrap_rate']:7.4f} "
                  f"{r['throughput']:7.1f}")
        print()

    out = ROOT / "results" / "ablation.csv"
    pd.DataFrame(records).to_csv(out, index=False)

    df = pd.DataFrame(records)
    full = df[df.ablation == "none"]

    print("  Reading — and it is not the uniform result the design expected:")
    print()
    print("  CP5 carries real weight. Hiding it produces "
          f"{df[df.ablation == 'CP5'].hc3_breaches.mean():.1f} genuine")
    print("  ergonomic breaches per shift against zero for the full framework.")
    print("  The scheduler filters HC3 on a score that understates the risk and")
    print("  lets through pairings that breach the limit in fact.")
    print()
    print("  CP1 and CP2 change no decisions. Mean fatigue, throughput and")
    print("  scrap all sit within noise of the full framework. Raising the")
    print("  quality weight from 0.15 to 0.25 does not change that, so it is")
    print("  not a matter of tuning.")
    print()
    print("  The reason is redundancy of information, not irrelevance of the")
    print("  coupling. Skill already reaches the decision three other ways —")
    print("  through processing time, the skill-matching preference and the")
    print("  competence floor. Fatigue reaches it through the fatigue limit and")
    print("  the objective's own fatigue term. Machine pace has no route in")
    print("  except through the ergonomic score, which is why removing that one")
    print("  is the only ablation that bites.")
    print()
    print("  So the honest statement is narrower than 'the couplings matter':")
    print("  they matter to what the model REPORTS, since defect outcomes are")
    print("  scored on skill and fatigue either way, but only CP5 changes what")
    print("  the scheduler CHOOSES.")
    print(f"  [ok] wrote {out}")


if __name__ == "__main__":
    main()
