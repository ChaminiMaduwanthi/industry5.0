"""
T7.3 / T7.4 — the two result figures.

    fig3_tradeoff    the efficiency-versus-wellbeing frontier
    fig4_comparison  the three baselines across the three pillars

Both are written for an IEEE two-column page and for the black-and-white
check in T8.11, so colour never carries meaning on its own: every series also
differs in marker, line style or hatch, and the values are printed on the marks.

The palette is the first slots of the validated categorical order (blue,
orange, aqua), which clears the all-pairs colour-blindness gates. Aqua sits
below 3:1 against the surface, so the series that uses it is directly labelled
rather than left to the legend — that is the documented relief for the warning,
not an oversight.

Run:  python src/make_figures.py
Writes figures/fig3_tradeoff.{png,pdf} and figures/fig4_comparison.{png,pdf}
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- validated categorical slots 1-3 (see references/palette.md) -------------
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
AXIS = "#c3c2b7"

SCENARIO_STYLE = {
    "S1": {"color": BLUE,   "marker": "o", "ls": "-",  "name": "S1 Normal"},
    "S2": {"color": ORANGE, "marker": "s", "ls": "--", "name": "S2 High-demand"},
    "S3": {"color": AQUA,   "marker": "^", "ls": "-.", "name": "S3 Disruption"},
}

# B1 is a floor for sanity, not a subject of the comparison, so it takes the
# neutral ink rather than a categorical hue. That leaves the real contrast —
# Industry 4.0 against the proposal — carrying the only two hues in the figure.
BASELINE_STYLE = {
    "B1": {"color": "#bdbcb6", "hatch": "",   "name": "B1 Random"},
    "B2": {"color": ORANGE,    "hatch": "//", "name": "B2 Industry 4.0"},
    "B3": {"color": BLUE,      "hatch": "",   "name": "B3 Proposed"},
}


def _style_axes(ax) -> None:
    """Recessive chrome: hairline grid, no box, muted ticks."""
    ax.set_axisbelow(True)
    ax.grid(True, color=GRID, linewidth=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=8, length=3, width=0.8)


# =============================================================================
# Figure 3 — the trade-off frontier
# =============================================================================
def figure_three() -> None:
    """Throughput against fatigue, as the fatigue limit is swept.

    This is the trade-off the paper is about, and it is traced by moving the
    CONSTRAINT rather than the objective weights — which is the honest way to
    draw it here, since the weight sweep showed the weights do not move the
    outcome. Each line is one scenario; the three points on it are HC1 at 0.70,
    0.80 and 0.90, and the filled point is the threshold actually used.
    """
    sweep = pd.read_csv(RESULTS / "sensitivity_hc1.csv")
    sweep = sweep[sweep.policy == "B3a_constrained"]
    raw = pd.read_csv(RESULTS / "raw_results.csv")
    b2 = raw[raw.baseline == "B2"].groupby("scenario")[
        ["mean_fatigue", "throughput"]].mean()

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    _style_axes(ax)

    for scen, st in SCENARIO_STYLE.items():
        s = sweep[sweep.scenario == scen].sort_values("hc1")
        ax.plot(s.mean_fatigue, s.throughput, color=st["color"], marker=st["marker"],
                linestyle=st["ls"], linewidth=1.8, markersize=6,
                markerfacecolor="white", markeredgewidth=1.6, zorder=3,
                label=f"{st['name']} — proposed")

        # The operating point, filled so it reads as the chosen setting.
        op = s[s.hc1 == 0.80].iloc[0]
        ax.plot(op.mean_fatigue, op.throughput, marker=st["marker"],
                color=st["color"], markersize=7, markeredgecolor="white",
                markeredgewidth=1.2, zorder=4)

        # Industry 4.0 for the same scenario: an x, always to the right of its
        # own frontier. No connector is drawn between them — three of those
        # cross the whole plot and read as extra series.
        ref = b2.loc[scen]
        ax.plot(ref.mean_fatigue, ref.throughput, marker="X", color=st["color"],
                markersize=10, markeredgecolor="white", markeredgewidth=1.2,
                zorder=4)

        # Direct label — the relief for aqua's sub-3:1 contrast, and it keeps
        # the figure readable in grayscale where the hues collapse. Placed above
        # the leftmost point, which is the one end of the line nothing else uses.
        # Up and to the LEFT of the leftmost point: every line rises to the
        # right, so that quadrant is the only one guaranteed to be empty.
        start = s.iloc[0]
        ax.annotate(st["name"], xy=(start.mean_fatigue, start.throughput),
                    xytext=(-9, 7), textcoords="offset points",
                    fontsize=8.5, color=st["color"], fontweight="bold",
                    ha="right", va="bottom")

    # Which point is which threshold, marked once on the line with most room.
    # The legend already says what the sweep is, so no second caption here.
    s2 = sweep[sweep.scenario == "S2"].sort_values("hc1")
    for _, r in s2.iterrows():
        ax.annotate(f"{r.hc1:.2f}", xy=(r.mean_fatigue, r.throughput),
                    xytext=(0, -15), textcoords="offset points",
                    fontsize=7.5, color=MUTED, ha="center")

    # Left margin so the right-aligned labels have somewhere to sit.
    ax.set_xlim(0.355, 0.775)

    ax.set_xlabel("Mean operator fatigue  $\\hat{F}$   (lower is better)",
                  fontsize=9, color=INK)
    ax.set_ylabel("Throughput  (units per shift)", fontsize=9, color=INK)
    ax.set_title("Efficiency against wellbeing, swept over the fatigue limit",
                 fontsize=10, color=INK, pad=10, loc="left")

    handles = [
        plt.Line2D([], [], color=MUTED, marker="o", markerfacecolor="white",
                   markeredgewidth=1.6, linestyle="-", markersize=6,
                   label="Proposed, HC1 swept 0.70 / 0.80 / 0.90"),
        plt.Line2D([], [], color=MUTED, marker="o", linestyle="none",
                   markersize=7, label="Operating point (HC1 = 0.80)"),
        plt.Line2D([], [], color=MUTED, marker="X", linestyle="none",
                   markersize=9, label="B2 Industry 4.0"),
    ]
    leg = ax.legend(handles=handles, loc="lower right", fontsize=8,
                    frameon=True, framealpha=1.0, edgecolor=GRID)
    leg.get_frame().set_linewidth(0.8)
    for t in leg.get_texts():
        t.set_color(MUTED)

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGURES / f"fig3_tradeoff.{ext}", dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[ok] figures/fig3_tradeoff.{png,pdf}")


# =============================================================================
# Figure 4 — the three baselines, by pillar
# =============================================================================
PANELS = [
    ("mean_fatigue",          "Mean fatigue $\\hat{F}$",   "People", "{:.2f}", False),
    ("mean_rula",             "Mean RULA score",           "People", "{:.2f}", False),
    ("constraint_violations", "Constraint breaches",       "People", "{:.0f}", False),
    ("energy_per_unit",       "Energy per unit (kWh)",     "Planet", "{:.2f}", False),
    ("co2e_kg",               "CO$_2$e per shift (kg)",    "Planet", "{:.1f}", False),
    ("throughput",            "Throughput (units)",        "Profit", "{:.1f}", True),
]


def figure_four() -> None:
    """Six KPIs across the three baselines, in the high-demand scenario.

    Native units in six small panels rather than one indexed axis: indexing to
    "B2 = 100" would put a fatigue score and a kilogram of CO2 on the same
    scale and invite the reader to average them, which they are not.

    S2 is shown because it is the scenario the paper leads with — the one where
    demand exceeds what three operators can sustain, so protecting them has to
    cost something. S1 and S3 are in Table II.
    """
    raw = pd.read_csv(RESULTS / "raw_results.csv")
    s2 = raw[raw.scenario == "S2"].groupby("baseline")
    means = s2[[p[0] for p in PANELS]].mean()
    stds = s2[[p[0] for p in PANELS]].std()

    order = ["B1", "B2", "B3"]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.6))

    for ax, (key, label, pillar, fmt, higher_better) in zip(axes.flat, PANELS):
        _style_axes(ax)
        ax.grid(axis="x", visible=False)

        for i, b in enumerate(order):
            st = BASELINE_STYLE[b]
            value = means.loc[b, key]
            ax.bar(i, value, width=0.62, color=st["color"], hatch=st["hatch"],
                   edgecolor="white", linewidth=1.2, zorder=3)

            # A measured zero draws no bar, which reads as missing data rather
            # than as the result it is. A stub on the baseline says the series
            # is present and equal to zero.
            if value == 0:
                ax.plot([i - 0.31, i + 0.31], [0, 0], color=st["color"],
                        linewidth=3.0, solid_capstyle="butt", zorder=5)

            err = stds.loc[b, key]
            if err > 0:
                ax.errorbar(i, value, yerr=err, fmt="none", ecolor=MUTED,
                            elinewidth=0.9, capsize=2.5, zorder=4)
            ax.annotate(fmt.format(value), xy=(i, value),
                        xytext=(0, 4 + (6 if err > 0 else 0)),
                        textcoords="offset points", ha="center",
                        fontsize=7.5, color=INK, fontweight="bold")

        arrow = "higher is better" if higher_better else "lower is better"
        ax.set_title(f"{label}\n{pillar} · {arrow}", fontsize=8.5, color=INK,
                     pad=6, linespacing=1.5)
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels(order, fontsize=8.5, color=INK)
        ax.set_xlim(-0.6, len(order) - 0.4)
        ax.margins(y=0.24)

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=BASELINE_STYLE[b]["color"],
                             hatch=BASELINE_STYLE[b]["hatch"],
                             edgecolor="white", linewidth=1.2,
                             label=BASELINE_STYLE[b]["name"]) for b in order]
    leg = fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8.5,
                     frameon=False, bbox_to_anchor=(0.5, -0.015))
    for t in leg.get_texts():
        t.set_color(MUTED)

    fig.suptitle("Baseline comparison under high demand (S2), 30 runs per bar",
                 fontsize=10, color=INK, x=0.02, ha="left", y=0.995)
    fig.tight_layout(rect=(0, 0.045, 1, 0.985))
    for ext in ("png", "pdf"):
        fig.savefig(FIGURES / f"fig4_comparison.{ext}", dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[ok] figures/fig4_comparison.{png,pdf}")


if __name__ == "__main__":
    figure_three()
    figure_four()
