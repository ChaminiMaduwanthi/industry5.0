"""
T4.2 — Exploratory Data Analysis, targeted at the framework parameters.

This is NOT a general-purpose EDA. Every block below exists to estimate one
specific quantity that docs/04-framework-design.md leaves open:

    D1  AI4I 2020    ->  L0        nominal machine life in busy minutes  (§3.1)
    D3  Steel Energy ->  e_idle    idle power draw                       (§3.2)
                         delta_e   additional draw per task type         (§3.2)
    D4  SECOM        ->  sanity check for the quality model              (§3.3)

Outputs
-------
    results/eda_summary.md          human-readable findings
    results/eda/*.png               diagnostic plots (NOT paper figures)
    data/processed/eda_params.json  the estimated numbers, for T4.3

Run:  python src/eda.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "results"
PLOTS = OUT / "eda"

PLOTS.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

# The Windows console defaults to cp1252 and cannot print the arrows used in
# the report. The report file itself is always written as UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Task types in the framework, and how they map onto the D3 load categories.
LOAD_MAP = {"Light_Load": "L", "Medium_Load": "M", "Maximum_Load": "H"}

report: list[str] = []
params: dict = {}


def say(line: str = "") -> None:
    """Write a line to both the console and the markdown report."""
    print(line)
    report.append(line)


# =============================================================================
# D1 · AI4I 2020 -> nominal machine life L0
# =============================================================================
def analyse_d1() -> None:
    say("## D1 · AI4I 2020 Predictive Maintenance")
    say()

    df = pd.read_csv(RAW / "ai4i2020" / "ai4i2020.csv")
    say(f"- Rows: **{len(df):,}** · Columns: **{df.shape[1]}** · "
        f"Missing values: **{int(df.isna().sum().sum())}**")

    fail_rate = df["Machine failure"].mean()
    say(f"- Overall failure rate: **{fail_rate:.2%}** "
        f"({int(df['Machine failure'].sum())} failures)")
    say()
    say("> ⚠️ **AI4I 2020 is a *synthetic* dataset** (Matzka, 2020) built to "
        "reproduce the statistics of real milling-machine maintenance data. It "
        "is a standard public benchmark, but it is not a measurement log. The "
        "paper must therefore say *public benchmark datasets*, **not** "
        "*real-world datasets*, when describing D1. D3 (a Korean steel plant) "
        "and D4 (a semiconductor line) are real measurements.")

    modes = ["TWF", "HDF", "PWF", "OSF", "RNF"]
    say()
    say("### Failure modes")
    say()
    say("| Mode | Meaning | Count | Share of rows |")
    say("|---|---|---|---|")
    meanings = {
        "TWF": "Tool wear failure",
        "HDF": "Heat dissipation failure",
        "PWF": "Power failure",
        "OSF": "Overstrain failure",
        "RNF": "Random failure",
    }
    for m in modes:
        say(f"| {m} | {meanings[m]} | {int(df[m].sum())} | {df[m].mean():.2%} |")

    # --- L0 : nominal life -----------------------------------------------
    # Each row is an independent process snapshot, not a time series, so the
    # tool-wear value at which failures occur is what defines the usable life.
    wear = df["Tool wear [min]"]
    twf = df[df["TWF"] == 1]["Tool wear [min]"]
    any_fail = df[df["Machine failure"] == 1]["Tool wear [min]"]

    say()
    say("### Estimating L0 (nominal life, busy minutes) — design §3.1")
    say()
    say("| Population | n | mean wear | median | P5 | P95 | max |")
    say("|---|---|---|---|---|---|---|")
    for name, s in [("All rows", wear), ("Any failure", any_fail),
                    ("Tool-wear failures (TWF)", twf)]:
        say(f"| {name} | {len(s):,} | {s.mean():.1f} | {s.median():.1f} | "
            f"{s.quantile(0.05):.1f} | {s.quantile(0.95):.1f} | {s.max():.1f} |")

    # TWF is the only mode that is a direct function of accumulated wear, so it
    # is the defensible basis for a wear-driven life estimate.
    l0 = float(twf.mean())
    l0_lo, l0_hi = float(twf.min()), float(twf.max())
    params["L0_minutes"] = round(l0, 1)
    params["L0_range"] = [round(l0_lo, 1), round(l0_hi, 1)]
    params["L0_basis"] = "mean tool wear at TWF events, AI4I 2020"

    say()
    say(f"➜ **L0 = {l0:.0f} busy-minutes** (TWF range {l0_lo:.0f}-{l0_hi:.0f} min).")
    say()
    say("What this means for task allocation, via `H(t+dt) = H - dt*kappa/L0`:")
    say()
    say("| Task | kappa | Minutes until H reaches 0 |")
    say("|---|---|---|")
    for t, k in [("L Light", 0.7), ("M Medium", 1.0), ("H Heavy", 1.4)]:
        say(f"| {t} | {k} | **{l0 / k:.0f} min** |")
    say()
    say(f"➜ Continuous heavy work exhausts a machine **{1.4 / 0.7:.0f}x faster** "
        f"than light work. This ratio is what gives the decision layer a "
        f"data-grounded reason to rotate task types across machines.")

    # --- plot -------------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].hist(wear, bins=40, color="#8899aa", label="all rows")
    ax[0].hist(any_fail, bins=40, color="#cc5555", label="failures")
    ax[0].set_xlabel("Tool wear [min]"); ax[0].set_ylabel("count")
    ax[0].set_title("D1 · tool wear distribution"); ax[0].legend()

    ax[1].bar(modes, [df[m].sum() for m in modes], color="#5577aa")
    ax[1].set_ylabel("count"); ax[1].set_title("D1 · failure modes")
    fig.tight_layout(); fig.savefig(PLOTS / "d1_ai4i.png", dpi=120); plt.close(fig)
    say()
    say("![D1](eda/d1_ai4i.png)")
    say()


# =============================================================================
# D3 · Steel Industry Energy -> e_idle and delta_e
# =============================================================================
def analyse_d3() -> None:
    say("## D3 · Steel Industry Energy Consumption")
    say()

    df = pd.read_csv(RAW / "steel_energy" / "Steel_industry_data.csv")
    say(f"- Rows: **{len(df):,}** · Columns: **{df.shape[1]}** · "
        f"Missing values: **{int(df.isna().sum().sum())}**")

    # 35040 rows = 365 days x 96 intervals -> one row per 15 minutes.
    interval_min = round(365 * 24 * 60 / len(df))
    say(f"- Sampling interval: **{interval_min} minutes** "
        f"({len(df):,} rows = 365 days x {24 * 60 // interval_min} intervals)")
    say()
    say(f"> Note: the sampling interval of this dataset ({interval_min} min) is "
        f"identical to the decision epoch of the framework (15 min), so one row "
        f"corresponds to exactly one epoch of machine energy use.")
    say()

    say("### Energy by load type — design §3.2")
    say()
    say("| D3 Load_Type | Framework task | n | mean kWh/15min | median | std | mean kW |")
    say("|---|---|---|---|---|---|---|")
    stats = {}
    for load, task in LOAD_MAP.items():
        s = df.loc[df["Load_Type"] == load, "Usage_kWh"]
        stats[task] = s
        say(f"| {load} | **{task}** | {len(s):,} | {s.mean():.2f} | "
            f"{s.median():.2f} | {s.std():.2f} | {s.mean() * 4:.2f} |")

    # e_idle : the floor of the lightest category, taken as an outlier-robust
    # low percentile rather than the minimum (same reasoning as design §6).
    e_idle = float(stats["L"].quantile(0.05))
    delta = {t: float(stats[t].mean() - e_idle) for t in ("L", "M", "H")}

    params["energy_interval_minutes"] = interval_min
    params["e_idle_kwh_per_interval"] = round(e_idle, 3)
    params["delta_e_kwh_per_interval"] = {t: round(v, 3) for t, v in delta.items()}
    params["energy_ratio_H_over_L"] = round(
        stats["H"].mean() / stats["L"].mean(), 2)

    skew_l = stats["L"].mean() / stats["L"].median()
    say()
    say(f"> ⚠️ **Light_Load is strongly right-skewed** (mean/median = "
        f"{skew_l:.1f}): that category mixes genuine idling with light "
        f"production. The **mean** is used anyway, because energy is additive — "
        f"total kWh over a shift is the sum of expected draws, and the median "
        f"would systematically understate consumption and therefore CO2e. The "
        f"median is reported above so the choice is visible.")
    say()
    say(f"➜ **e_idle = {e_idle:.2f} kWh/15min** (P5 of Light_Load, "
        f"outlier-robust floor)")
    say()
    say("| Task | delta_e (kWh/15min) | E = e_idle + delta_e |")
    say("|---|---|---|")
    for t in ("L", "M", "H"):
        say(f"| {t} | {delta[t]:.2f} | {e_idle + delta[t]:.2f} |")

    ratio = stats["H"].mean() / stats["L"].mean()
    say()
    say(f"➜ **Heavy work draws {ratio:.1f}x the energy of light work.**")
    say()
    say("> ⚠️ Only this *ratio* is carried into the simulation. The absolute "
        "level is rescaled to the factory modelled here "
        "(`machines.energy_rescale_to_kwh_per_hour` in config.yaml), because a "
        "steel plant operates at a different scale. Every baseline uses the "
        "same rescaling, so the B1/B2/B3 comparison is unaffected.")

    # --- plot -------------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].boxplot([stats[t] for t in ("L", "M", "H")], labels=["L", "M", "H"],
                  showfliers=False)
    ax[0].axhline(e_idle, color="#cc5555", ls="--", label=f"e_idle = {e_idle:.2f}")
    ax[0].set_ylabel("kWh per 15 min"); ax[0].set_title("D3 · energy by task type")
    ax[0].legend()

    ax[1].bar(["L", "M", "H"], [stats[t].mean() for t in ("L", "M", "H")],
              color=["#88aa77", "#ddaa55", "#cc5555"])
    ax[1].set_ylabel("mean kWh per 15 min"); ax[1].set_title("D3 · mean draw")
    fig.tight_layout(); fig.savefig(PLOTS / "d3_energy.png", dpi=120); plt.close(fig)
    say()
    say("![D3](eda/d3_energy.png)")
    say()


# =============================================================================
# D4 · SECOM -> feasibility of fitting the quality model
# =============================================================================
def analyse_d4() -> None:
    say("## D4 · SECOM")
    say()

    path = RAW / "secom" / "secom.data"
    if not path.exists():
        say("- not downloaded, skipped")
        say()
        return

    x = pd.read_csv(path, sep=r"\s+", header=None)
    y = pd.read_csv(RAW / "secom" / "secom_labels.data", sep=r"\s+",
                    header=None, usecols=[0], names=["label"])

    miss = x.isna().sum().sum() / x.size
    pass_rate = (y["label"] == -1).mean()

    say(f"- Shape: **{x.shape[0]} x {x.shape[1]}** sensor features")
    say(f"- Missing values: **{miss:.1%}** of all cells")
    say(f"- Class balance: **{pass_rate:.1%} pass / {1 - pass_rate:.1%} fail** "
        f"({int((y['label'] == 1).sum())} failures)")

    params["secom_defect_rate"] = round(float(1 - pass_rate), 4)

    say()
    say(f"➜ Baseline defect rate **{1 - pass_rate:.2%}**. This anchors the "
        f"intercept b0 of the quality model so that a healthy machine operated "
        f"by a skilled, unfatigued operator produces a realistic defect rate.")
    say()
    say("> ⚠️ SECOM's features are anonymised sensor readings with no operator "
        "attributes, so b2 (skill) and b3 (fatigue) **cannot** be fitted from "
        "it. Those two coefficients stay as specified in design §3.3 with their "
        "signs constrained positive, and are covered by the CP ablation (T7.8).")
    say()


# =============================================================================
def main() -> None:
    say("# T4.2 · EDA Summary")
    say()
    say("> Generated by `src/eda.py` on **2026-08-05**. "
        "Every number here feeds a specific parameter in "
        "`docs/04-framework-design.md`.")
    say()
    say("---")
    say()

    analyse_d1()
    say("---")
    say()
    analyse_d3()
    say("---")
    say()
    analyse_d4()
    say("---")
    say()

    say("## Estimated parameters (also in `data/processed/eda_params.json`)")
    say()
    say("```json")
    say(json.dumps(params, indent=2))
    say("```")

    (OUT / "eda_summary.md").write_text("\n".join(report), encoding="utf-8")
    (PROCESSED / "eda_params.json").write_text(
        json.dumps(params, indent=2), encoding="utf-8")

    print()
    print(f"[ok] wrote {OUT / 'eda_summary.md'}")
    print(f"[ok] wrote {PROCESSED / 'eda_params.json'}")
    print(f"[ok] plots in {PLOTS}")


if __name__ == "__main__":
    main()
