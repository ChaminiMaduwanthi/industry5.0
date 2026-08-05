"""
T6.5 / T6.6 / T6.7 — what the experiment run must satisfy.

WRITTEN BEFORE THE RUNNER. The output of this stage becomes every table and
figure in the paper, so a silent defect here — a missing cell, a duplicated
run, a result that does not reproduce — propagates into published claims and
is close to undetectable once the numbers look plausible.

Design: experiment-plan §6 (3 baselines x 3 scenarios x 30 seeds = 270 runs)
and §11 (reproducibility).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd                                        # noqa: E402
import pytest                                              # noqa: E402
from loader import load_setup                              # noqa: E402
from run_experiments import BASELINES, build_matrix, run_one  # noqa: E402

CFG = load_setup("S1").cfg

# experiment-plan §6 names these as the columns of raw_results.csv.
REQUIRED = [
    "run_id", "scenario", "baseline", "seed",
    "mean_fatigue", "max_fatigue", "mean_rula", "workload_gini",
    "energy_kwh", "energy_per_unit", "co2e_kg", "scrap_rate",
    "throughput", "downtime_hrs", "oee",
    "constraint_violations", "runtime_sec",
]


@pytest.fixture(scope="module")
def small() -> pd.DataFrame:
    """Four seeds instead of thirty — the shape is what is being checked."""
    return build_matrix(seeds=4, progress=False)


# =============================================================================
# The matrix must be complete and unambiguous
# =============================================================================
def test_every_cell_of_the_matrix_is_present(small):
    scenarios = CFG["experiment"]["scenarios"]
    expected = len(scenarios) * len(BASELINES) * 4
    assert len(small) == expected, f"expected {expected} runs, got {len(small)}"

    for scenario in scenarios:
        for baseline in BASELINES:
            cell = small[(small.scenario == scenario)
                         & (small.baseline == baseline)]
            assert len(cell) == 4, f"{scenario}/{baseline} has {len(cell)} runs"


def test_no_run_is_duplicated(small):
    key = small[["scenario", "baseline", "seed"]]
    assert not key.duplicated().any(), "the same run appears twice"
    assert small.run_id.is_unique


def test_every_required_column_is_present_and_populated(small):
    missing = [c for c in REQUIRED if c not in small.columns]
    assert not missing, f"raw_results is missing {missing}"
    for col in REQUIRED:
        assert small[col].notna().all(), f"{col} has empty cells"


# =============================================================================
# The numbers must be physically possible
# =============================================================================
def test_values_stay_within_their_ranges(small):
    for col in ("mean_fatigue", "max_fatigue", "scrap_rate",
                "workload_gini", "oee"):
        assert small[col].between(0, 1).all(), f"{col} left [0,1]"
    assert small.mean_rula.between(1, 7).all()
    assert (small.energy_kwh > 0).all()
    assert (small.throughput >= 0).all()
    assert (small.downtime_hrs >= 0).all()
    assert (small.runtime_sec > 0).all()


def test_peak_fatigue_is_never_below_the_mean(small):
    assert (small.max_fatigue >= small.mean_fatigue - 1e-9).all()


def test_only_the_human_aware_policy_holds_the_limits(small):
    """B3 must record no violations; B1 and B2 must record some."""
    b3 = small[small.baseline == "B3"]
    assert (b3.constraint_violations == 0).all(), (
        "B3 breached a hard constraint")
    for baseline in ("B1", "B2"):
        other = small[small.baseline == baseline]
        assert other.constraint_violations.sum() > 0, (
            f"{baseline} enforced limits it was never given")


# =============================================================================
# T6.7 — reproducibility
# =============================================================================
def test_the_same_seed_gives_the_same_row():
    a = run_one("S2", "B3", seed=11)
    b = run_one("S2", "B3", seed=11)
    for k, v in a.items():
        if k == "runtime_sec":          # wall clock, not part of the result
            continue
        assert b[k] == v, f"{k} changed between identical runs"


def test_rerunning_the_matrix_reproduces_it_exactly(small):
    again = build_matrix(seeds=4, progress=False)
    left = small.drop(columns=["runtime_sec"]).reset_index(drop=True)
    right = again.drop(columns=["runtime_sec"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(left, right)


def test_different_seeds_give_different_results():
    """A runner that ignored its seed would pass every check above."""
    a = run_one("S2", "B3", seed=1)
    b = run_one("S2", "B3", seed=2)
    assert a["throughput"] != b["throughput"] or a["mean_fatigue"] != b["mean_fatigue"]
