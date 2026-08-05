"""
T7.1 / T7.2 — the KPI table and its statistics (experiment-plan §7, §8).

Produces Table II of the paper: every KPI, every baseline, the gap between the
proposed framework and the Industry 4.0 baseline, and whether that gap survives
a test that assumes nothing about the distribution.

Three decisions worth stating, because each of them changes what the table
means:

Mann-Whitney U rather than a t-test. Thirty runs is not many, several KPIs are
bounded (fatigue on [0,1], breach counts at zero), and one of them is
identically zero under the proposed policy. Normality is tested and reported,
but the rank test is used throughout so every row is comparable.

Cliff's delta rather than Cohen's d. Same reason: it needs no normality and no
equal variance, and it stays interpretable when a sample has no spread at all.

Bonferroni across the KPIs in a scenario. Ten tests at 0.05 will hand you a
significant result on noise about forty percent of the time. The corrected
threshold is reported next to every p-value so nothing is hidden in a footnote.

Run:  python src/analyse_results.py
Writes results/kpi_table.csv and results/kpi_table.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, shapiro

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ALPHA = 0.05

# (column, label, pillar, lower_is_better)
KPIS = [
    ("mean_fatigue",          "Mean fatigue",        "People", True),
    ("max_fatigue",           "Peak fatigue",        "People", True),
    ("mean_rula",             "Mean RULA",           "People", True),
    ("constraint_violations", "Constraint breaches", "People", True),
    ("workload_gini",         "Workload Gini",       "People", True),
    ("energy_per_unit",       "Energy per unit",     "Planet", True),
    ("co2e_kg",               "CO2e",                "Planet", True),
    ("scrap_rate",            "Scrap rate",          "Planet", True),
    ("throughput",            "Throughput",          "Profit", False),
    ("downtime_hrs",          "Downtime",            "Profit", True),
    ("oee",                   "OEE",                 "Profit", False),
]


# =============================================================================
# Statistics
# =============================================================================
def cliffs_delta(a, b) -> float:
    """Probability a random value from `a` exceeds one from `b`, minus the
    reverse. Runs from -1 to +1 and needs no distributional assumption."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return 0.0
    diff = a[:, None] - b[None, :]
    return float((np.sum(diff > 0) - np.sum(diff < 0)) / (a.size * b.size))


def interpret_delta(delta: float) -> str:
    """experiment-plan §8 thresholds, on magnitude."""
    d = abs(delta)
    if d < 0.2:
        return "negligible"
    if d < 0.5:
        return "small"
    if d < 0.8:
        return "medium"
    return "large"


def compare(treatment, baseline, n_comparisons: int = 1) -> dict:
    """One row's worth of statistics, with the correction applied."""
    t = np.asarray(treatment, dtype=float)
    b = np.asarray(baseline, dtype=float)
    alpha = ALPHA / max(n_comparisons, 1)

    # Both samples constant and identical: no difference exists to test.
    if np.allclose(t, b):
        return {"p_value": 1.0, "effect": 0.0, "effect_label": "negligible",
                "alpha": alpha, "significant": False, "normal": False,
                "test": "none (identical samples)"}

    try:
        _, p = mannwhitneyu(t, b, alternative="two-sided")
    except ValueError:                      # every value tied
        p = 1.0

    normal = False
    if t.std() > 0 and b.std() > 0 and len(t) >= 3:
        normal = shapiro(t)[1] > ALPHA and shapiro(b)[1] > ALPHA

    delta = cliffs_delta(t, b)
    return {
        "p_value": float(p),
        "effect": delta,
        "effect_label": interpret_delta(delta),
        "alpha": alpha,
        "significant": bool(p < alpha),
        "normal": bool(normal),
        "test": "Mann-Whitney U",
    }


# =============================================================================
# The table
# =============================================================================
def load_results(path: Path | None = None) -> pd.DataFrame:
    return pd.read_csv(path or ROOT / "results" / "raw_results.csv")


def build_kpi_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n = len(KPIS)                           # Bonferroni across KPIs per scenario

    for scenario in sorted(df.scenario.unique()):
        cell = df[df.scenario == scenario]
        samples = {b: cell[cell.baseline == b] for b in ("B1", "B2", "B3")}

        for col, label, pillar, lower_better in KPIS:
            b1, b2, b3 = (samples[b][col] for b in ("B1", "B2", "B3"))
            stats = compare(b3, b2, n_comparisons=n)

            # Percentages are computed from the ROUNDED means that the table
            # prints, so a reader recomputing the column arrives at the same
            # number. Deriving them from full precision left the published
            # figure disagreeing with the published means — by five points on
            # the workload measure, whose base is close to zero.
            m1, m2, m3 = (round(x.mean(), 5) for x in (b1, b2, b3))
            delta_abs = round(m3 - m2, 5)
            delta_pct = (m3 - m2) / m2 * 100 if m2 else 0.0
            improved = (delta_abs < 0) if lower_better else (delta_abs > 0)

            # A percentage on a near-zero base is arithmetically correct and
            # rhetorically useless: workload balance moves from 0.009 to 0.084
            # on a 0-1 scale, which is +863%. Report the absolute difference
            # for those and let the percentage stay in the file for anyone who
            # wants it.
            pct_meaningful = abs(m2) >= 0.05

            rows.append({
                "scenario": scenario, "pillar": pillar, "kpi": label,
                "column": col,
                "B1_mean": m1, "B1_std": round(b1.std(), 5),
                "B2_mean": m2, "B2_std": round(b2.std(), 5),
                "B3_mean": m3, "B3_std": round(b3.std(), 5),
                "delta_abs": delta_abs,
                "pct_meaningful": pct_meaningful,
                "delta_pct": round(delta_pct, 2),
                "improved": bool(improved),
                "p_value": round(stats["p_value"], 6),
                "alpha": round(stats["alpha"], 6),
                "significant": stats["significant"],
                "effect": round(stats["effect"], 4),
                "effect_label": stats["effect_label"],
                "normal": stats["normal"],
                "test": stats["test"],
            })

    return pd.DataFrame(rows)


def to_markdown(table: pd.DataFrame) -> str:
    out = ["# Table II — KPI comparison (B3 vs B2)", "",
           f"30 runs per cell. Mann-Whitney U, Bonferroni-corrected across "
           f"{len(KPIS)} KPIs per scenario (alpha = "
           f"{ALPHA / len(KPIS):.4f}). Effect size is Cliff's delta.", ""]

    for scenario in sorted(table.scenario.unique()):
        part = table[table.scenario == scenario]
        out += [f"## {scenario}", "",
                "| Pillar | KPI | B1 Random | B2 Industry 4.0 | B3 Proposed | "
                "Δ vs B2 | p | Effect |", "|---|---|---|---|---|---|---|---|"]
        for r in part.itertuples():
            sig = " ✓" if r.significant else ""
            arrow = "▼" if r.delta_abs < 0 else "▲"
            p = "<0.001" if r.p_value < 0.001 else f"{r.p_value:.3f}"
            change = (f"{arrow} {r.delta_pct:+.1f}%" if r.pct_meaningful
                      else f"{arrow} {r.delta_abs:+.3f} abs")
            out.append(
                f"| {r.pillar} | {r.kpi} | {r.B1_mean:.3f} ± {r.B1_std:.3f} | "
                f"{r.B2_mean:.3f} ± {r.B2_std:.3f} | "
                f"**{r.B3_mean:.3f} ± {r.B3_std:.3f}** | "
                f"{change} | {p}{sig} | "
                f"{r.effect:+.2f} ({r.effect_label}) |")
        out.append("")
    out += ["✓ = significant after Bonferroni correction.",
            "",
            "Changes are given as a percentage except where the baseline sits "
            "close to zero, in which case the absolute difference is shown — a "
            "percentage on a near-zero base is correct arithmetic and "
            "misleading reporting.", ""]
    return "\n".join(out)


def main() -> None:
    df = load_results()
    table = build_kpi_table(df)

    print(f"=== T7.1 / T7.2 · KPI table · {len(df)} runs ===")
    print(f"    Mann-Whitney U · Bonferroni across {len(KPIS)} KPIs "
          f"(alpha = {ALPHA / len(KPIS):.4f}) · Cliff's delta")
    print()

    for scenario in sorted(table.scenario.unique()):
        part = table[table.scenario == scenario]
        print(f"  {scenario}")
        print(f"    {'KPI':22s} {'B2':>10s} {'B3':>10s} {'Δ%':>8s} "
              f"{'p':>9s} {'effect':>8s}  ")
        for r in part.itertuples():
            sig = "✓" if r.significant else " "
            p = "<0.001" if r.p_value < 0.001 else f"{r.p_value:.3f}"
            good = "+" if r.improved else "-"
            print(f"    {r.kpi:22s} {r.B2_mean:10.3f} {r.B3_mean:10.3f} "
                  f"{r.delta_pct:+7.1f}% {p:>9s} {r.effect:+7.2f} {sig}{good}")
        print()

    n_sig = int(table.significant.sum())
    n_imp = int((table.significant & table.improved).sum())
    print(f"  {n_sig}/{len(table)} comparisons significant after correction; "
          f"{n_imp} of those favour the proposed framework")

    table.to_csv(ROOT / "results" / "kpi_table.csv", index=False)
    (ROOT / "results" / "kpi_table.md").write_text(
        to_markdown(table), encoding="utf-8")
    print(f"  [ok] wrote results/kpi_table.csv and results/kpi_table.md")


if __name__ == "__main__":
    main()
