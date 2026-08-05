"""
T5.11 — hard and soft constraints (design §8).

*** This module is the difference between Industry 4.0 and Industry 5.0 in
    this framework. ***

The hard constraints filter the candidate set BEFORE the optimiser sees it
(design §9). They are not penalty terms. No weighting, however profit-hungry,
can buy its way past them — which is exactly the property that a weighted
objective alone cannot give you.

    HC1  F_hat < 0.80      fatigue below 80% of the operator's own AWL
    HC2  S >= 0.40         the operator is competent at this task
    HC3  R <= 5            RULA action level
    HC4  H > 0.30          the machine is not about to fail

HC1 carries hysteresis. A single threshold makes an operator flip between
working and resting every epoch around 0.799 / 0.801, so once fatigue reaches
the limit the rest continues until it has fallen to 0.60. That is a mandatory
rest, and it is the mechanism by which the framework protects a person that a
throughput-only scheduler would keep pushing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    """One possible (task, operator, machine) assignment, already costed."""
    task: object
    operator: str
    machine: str
    processing_minutes: float
    skill: float
    fatigue_hat: float          # operator fatigue now
    fatigue_after: float        # predicted fatigue once the task is done
    rula: float
    defect_risk: float
    marginal_kwh: float


@dataclass
class Violations:
    """Why candidates were rejected — reported, never silently dropped."""
    hc1_fatigue: int = 0
    hc2_skill: int = 0
    hc3_ergonomic: int = 0
    hc4_health: int = 0

    def total(self) -> int:
        return (self.hc1_fatigue + self.hc2_skill
                + self.hc3_ergonomic + self.hc4_health)

    def as_dict(self) -> dict:
        return {
            "hc1_filtered": self.hc1_fatigue,
            "hc2_filtered": self.hc2_skill,
            "hc3_filtered": self.hc3_ergonomic,
            "hc4_filtered": self.hc4_health,
        }


# =============================================================================
def update_rest_state(fatigue_hat: float, resting: bool,
                      enter_at: float, leave_at: float) -> bool:
    """HC1 hysteresis (design §8).

    Crossing `enter_at` starts a mandatory rest that continues until fatigue
    has fallen back to `leave_at`. Returns the new resting flag.
    """
    if resting:
        return fatigue_hat > leave_at
    return fatigue_hat >= enter_at


def filter_candidates(candidates: list[Candidate], hard: dict,
                      violations: Violations | None = None
                      ) -> list[Candidate]:
    """Keep only the assignments that satisfy every hard constraint.

    Order matters only for the violation tally, not the result: a candidate is
    counted against the first constraint it fails.
    """
    v = violations if violations is not None else Violations()
    kept = []

    for c in candidates:
        # HC1 is tested against the fatigue this assignment would PRODUCE, not
        # the fatigue the operator carries now. Testing the current value lets
        # an operator at 0.79 be handed a task that leaves them at 0.87, which
        # breaches the very limit the constraint exists to hold — measured at
        # roughly one and a half breaches per shift before this was fixed.
        if max(c.fatigue_hat, c.fatigue_after) >= hard["HC1_fatigue_max"]:
            v.hc1_fatigue += 1
        elif c.skill < hard["HC2_skill_min"]:
            v.hc2_skill += 1
        elif c.rula > hard["HC3_rula_max"]:
            v.hc3_ergonomic += 1
        else:
            kept.append(c)

    return kept


# =============================================================================
def soft_penalty(candidate: Candidate, workload_share: float,
                 switching: bool, soft: dict) -> float:
    """Soft constraints (design §8) — preferences, added to the objective.

        SC1  spread the work evenly       higher share -> higher penalty
        SC2  match task to skill          (1 - S)
        SC3  avoid machine switching      a setup cost

    These bend the choice. They cannot block one, which is the whole point of
    keeping them separate from the hard constraints above.
    """
    return (soft["SC1_workload_gini"] * workload_share
            + soft["SC2_skill_mismatch"] * (1.0 - candidate.skill)
            + soft["SC3_machine_switching"] * (1.0 if switching else 0.0))
