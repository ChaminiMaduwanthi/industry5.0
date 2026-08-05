"""
T7.1 / T7.2 — what the results analysis must satisfy.

WRITTEN BEFORE THE ANALYSIS. Statistics are the easiest place in this project
to be confidently wrong: an effect size with a flipped sign, a correction not
applied, a significance claim on a test that was never appropriate. None of it
shows up as an error, and all of it ends up in the paper as a number a reviewer
will check.

So the statistical helpers are pinned against cases whose answers are known
independently of the implementation.

Design: experiment-plan §7 (KPI table) and §8 (tests, effect sizes,
Bonferroni).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import numpy as np                                         # noqa: E402
import pandas as pd                                        # noqa: E402
import pytest                                              # noqa: E402
from analyse_results import (                              # noqa: E402
    build_kpi_table, cliffs_delta, compare, interpret_delta, load_results,
)


# =============================================================================
# Cliff's delta — checked against cases with known answers
# =============================================================================
def test_delta_of_a_sample_against_itself_is_zero():
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    assert cliffs_delta(x, x) == pytest.approx(0.0)


def test_delta_is_one_when_samples_do_not_overlap():
    """Every value in the first sample exceeds every value in the second."""
    assert cliffs_delta([10, 11, 12], [1, 2, 3]) == pytest.approx(1.0)
    assert cliffs_delta([1, 2, 3], [10, 11, 12]) == pytest.approx(-1.0)


def test_delta_has_the_sign_of_the_difference():
    rng = np.random.default_rng(0)
    a, b = rng.normal(10, 1, 200), rng.normal(8, 1, 200)
    assert cliffs_delta(a, b) > 0
    assert cliffs_delta(b, a) < 0
    assert cliffs_delta(a, b) == pytest.approx(-cliffs_delta(b, a), abs=1e-9)


def test_delta_stays_in_range():
    rng = np.random.default_rng(1)
    for _ in range(20):
        a = rng.normal(0, 1, 50)
        b = rng.normal(rng.uniform(-3, 3), 1, 50)
        assert -1.0 <= cliffs_delta(a, b) <= 1.0


def test_effect_size_labels_follow_the_documented_thresholds():
    """experiment-plan §8: 0.2 / 0.5 / 0.8."""
    assert interpret_delta(0.10) == "negligible"
    assert interpret_delta(0.30) == "small"
    assert interpret_delta(0.60) == "medium"
    assert interpret_delta(0.90) == "large"
    assert interpret_delta(-0.90) == "large"      # magnitude, not direction


# =============================================================================
# The comparison itself
# =============================================================================
def test_identical_samples_are_not_significant():
    """A test that finds a difference where there is none is worse than none."""
    x = list(np.random.default_rng(2).normal(5, 1, 30))
    r = compare(x, x, n_comparisons=1)
    assert r["p_value"] > 0.05
    assert not r["significant"]
    assert r["effect"] == pytest.approx(0.0)


def test_a_real_difference_is_detected():
    rng = np.random.default_rng(3)
    a, b = rng.normal(10, 1, 30), rng.normal(5, 1, 30)
    r = compare(a, b, n_comparisons=1)
    assert r["p_value"] < 0.001
    assert r["significant"]
    assert abs(r["effect"]) > 0.8


def test_bonferroni_makes_significance_harder():
    """Correcting for ten comparisons must not leave the threshold at 0.05."""
    rng = np.random.default_rng(4)
    a, b = rng.normal(10, 1, 30), rng.normal(9.4, 1, 30)
    loose = compare(a, b, n_comparisons=1)
    strict = compare(a, b, n_comparisons=10)
    assert strict["alpha"] == pytest.approx(loose["alpha"] / 10)
    assert strict["p_value"] == pytest.approx(loose["p_value"])
    assert not (strict["significant"] and not loose["significant"])


def test_p_values_stay_in_range():
    rng = np.random.default_rng(5)
    for _ in range(20):
        a, b = rng.normal(0, 1, 30), rng.normal(rng.uniform(-2, 2), 1, 30)
        r = compare(a, b, n_comparisons=10)
        assert 0.0 <= r["p_value"] <= 1.0


# =============================================================================
# The table the paper prints
# =============================================================================
@pytest.fixture(scope="module")
def results() -> pd.DataFrame:
    return load_results()


def test_the_matrix_is_the_one_that_was_run(results):
    assert len(results) == 270
    assert set(results.baseline) == {"B1", "B2", "B3"}
    assert set(results.scenario) == {"S1", "S2", "S3"}


def test_the_table_covers_every_kpi_and_scenario(results):
    table = build_kpi_table(results)
    assert set(table.scenario) == {"S1", "S2", "S3"}
    for col in ("kpi", "B1_mean", "B2_mean", "B3_mean",
                "delta_pct", "p_value", "effect", "effect_label",
                "significant"):
        assert col in table.columns
    assert table.notna().all().all()


def test_the_reported_delta_matches_the_means(results):
    """The percentage in the table must be derivable from the two means."""
    table = build_kpi_table(results)
    for row in table.itertuples():
        if row.B2_mean == 0:
            continue
        expected = (row.B3_mean - row.B2_mean) / row.B2_mean * 100
        assert row.delta_pct == pytest.approx(expected, abs=0.05), row.kpi


def test_significance_is_never_claimed_above_the_corrected_alpha(results):
    table = build_kpi_table(results)
    for row in table.itertuples():
        assert row.significant == (row.p_value < row.alpha)
