"""Tests for the deferral diagnosis (T5.16).

The failure this guards against is the same one the fatigue-rate study had to
guard against: a probe whose knob does not reach the simulation reports "no
effect" in exactly the same way as a real null result. So every condition is
first asserted to change what it claims to change, before any conclusion is
drawn from it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from deferral_diagnosis import (  # noqa: E402
    CONDITIONS, BASE_SKILL, build_setup, measure,
)
from loader import load_setup  # noqa: E402


# =============================================================================
# The knobs must reach the simulation
# =============================================================================
def test_every_condition_is_defined_and_named():
    assert "configured" in CONDITIONS
    for name, spec in CONDITIONS.items():
        assert spec.get("label"), f"{name} has no label"


@pytest.mark.parametrize("hc,key", [
    ("HC1 off", "HC1_fatigue_max"),
    ("HC2 off", "HC2_skill_min"),
    ("HC3 off", "HC3_rula_max"),
    ("HC4 off", "HC4_health_min"),
])
def test_disabling_a_constraint_reaches_the_config(hc, key):
    """The relaxed threshold must actually be in the setup the run receives."""
    base = load_setup("S1").cfg["constraints"]["hard"][key]
    relaxed = build_setup("S1", hc).cfg["constraints"]["hard"][key]
    assert relaxed != base, f"{hc} did not change {key}"


def test_hc1_remedy_moves_threshold_and_hysteresis_together():
    """Loader asserts enter_rest_at == HC1, so the remedy must set both."""
    s = build_setup("S1", "HC1 -> 0.85")
    assert s.cfg["constraints"]["hard"]["HC1_fatigue_max"] == 0.85
    assert s.cfg["constraints"]["hc1_hysteresis"]["enter_rest_at"] == 0.85
    assert (s.cfg["constraints"]["hc1_hysteresis"]["leave_rest_at"]
            < 0.85), "hysteresis band must stay below the threshold"


def test_training_remedy_lifts_op1_past_the_floor():
    s = build_setup("S1", "OP1 trained")
    floor = s.cfg["constraints"]["hard"]["HC2_skill_min"]
    assert s.operators["OP1"].skill["H"] > floor
    assert s.operators["OP2"].skill == BASE_SKILL["OP2"], "OP2 must be untouched"
    assert s.operators["OP3"].skill == BASE_SKILL["OP3"], "OP3 must be untouched"


def test_combined_remedy_applies_both():
    s = build_setup("S1", "both remedies")
    assert s.cfg["constraints"]["hard"]["HC1_fatigue_max"] == 0.85
    assert s.operators["OP1"].skill["H"] > s.cfg["constraints"]["hard"]["HC2_skill_min"]


# =============================================================================
# Nothing leaks back into the configured setup
# =============================================================================
def test_probe_does_not_mutate_the_shipped_configuration():
    build_setup("S1", "HC1 off")
    build_setup("S1", "OP1 trained")
    build_setup("S1", "both remedies")

    fresh = load_setup("S1")
    assert fresh.cfg["constraints"]["hard"]["HC1_fatigue_max"] == 0.80
    assert fresh.cfg["constraints"]["hard"]["HC2_skill_min"] == 0.40
    for op, skills in BASE_SKILL.items():
        assert fresh.operators[op].skill == skills, f"{op} skills leaked"


# =============================================================================
# The measurement itself
# =============================================================================
def test_deferral_rate_is_a_fraction():
    r = measure("S1", "configured", shifts=4)
    assert 0.0 <= r["deferral_rate"] <= 1.0
    assert r["epochs"] == 4 * load_setup("S1").epochs_per_shift
    assert r["deferral_epochs"] <= r["epochs"]


def test_configured_run_breaches_nothing():
    """The whole point of the hard filter: zero breaches as configured."""
    r = measure("S1", "configured", shifts=4)
    assert r["hc1_breaches"] == 0
    assert r["hc3_breaches"] == 0
    assert r["fatigue_breaches_vs_ref"] == 0, (
        "as configured the threshold IS the reference, so the two counts "
        "must agree")


def test_disabling_hc1_has_a_visible_safety_cost():
    """If removing the fatigue limit costs nothing, it was not binding."""
    off = measure("S1", "HC1 off", shifts=4)
    assert off["fatigue_breaches_vs_ref"] > 0, (
        "removing the fatigue limit produced no breaches of the reference, so "
        "either the limit never bound or the knob did not reach the run")


def test_own_threshold_count_hides_the_cost_that_the_reference_shows():
    """Why the fixed yardstick exists — the same trap the HC1 sweep hit.

    A run with the limit lifted above the range of the quantity reports zero
    breaches of a limit it does not have, and would look as safe as the
    configured run. Only the reference count reveals otherwise.
    """
    off = measure("S1", "HC1 off", shifts=4)
    assert off["hc1_breaches"] == 0, "precondition: own-threshold count is blind"
    assert off["fatigue_breaches_vs_ref"] > off["hc1_breaches"]


def test_disabling_hc2_removes_its_filtering():
    off = measure("S1", "HC2 off", shifts=4)
    assert off["hc2_filtered"] == 0, "candidates still filtered by a floor of 0"


def test_conditions_are_measured_on_the_same_seeds():
    """Two conditions must be comparable, so the seed block cannot vary."""
    a = measure("S1", "configured", shifts=3)
    b = measure("S1", "configured", shifts=3)
    assert a["deferral_epochs"] == b["deferral_epochs"], "measurement not stable"
    assert a["throughput"] == b["throughput"]
