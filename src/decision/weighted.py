"""
T5.11 — the weighted-sum decision layer, B3a (design §7.1, §9).

    Z = w1*F_hat + w2*R_hat + w3*E_hat + w4*W_hat - w5*T_hat

The design states that objective over a whole shift's policy. A decision epoch
cannot evaluate a whole shift, so each candidate assignment is scored on its
MARGINAL contribution to the same five terms, and the epoch takes the best
available. Throughput enters as its inverse — a shorter task returns the pair
to the queue sooner — which keeps the sign convention of the design while
leaving every term a cost to be minimised.

Every term is bounded on [0,1] by construction rather than by a calibration
run. That matters for a reason beyond convenience: the design's P5/P95
normalisation is fitted on B1 runs, and feeding fitted bounds into the decision
that produces the runs being fitted would be circular. The calibrated bounds
belong to reporting (T7.1) and to the Pareto axes (T5.12), where nothing is
being decided from them.

The order in `decide` is the one thing here that must not be rearranged: hard
constraints filter first, the optimiser only ever sees survivors. A penalty
large enough to be ignored is not a constraint.
"""

from __future__ import annotations

from decision.constraints import Candidate, Violations, filter_candidates, soft_penalty


def score(candidate: Candidate, weights: dict, scales: dict,
          workload_share: float, switching: bool, soft: dict) -> float:
    """Marginal cost of one assignment. Lower is better."""
    f_fatigue = candidate.fatigue_after                       # already [0,1]
    f_ergonomic = (candidate.rula - 1.0) / 6.0                # RULA 1..7
    f_energy = min(1.0, candidate.marginal_kwh / scales["max_marginal_kwh"])
    f_waste = candidate.defect_risk                           # already [0,1]
    f_time = min(1.0, candidate.processing_minutes / scales["max_minutes"])

    z = (weights["w1"] * f_fatigue
         + weights["w2"] * f_ergonomic
         + weights["w3"] * f_energy
         + weights["w4"] * f_waste
         + weights["w5"] * f_time)          # throughput: slower costs more

    return z + soft_penalty(candidate, workload_share, switching, soft)


def decide(candidates: list[Candidate], cfg: dict, scales: dict,
           workload_shares: dict, current_machine: dict,
           violations: Violations | None = None) -> Candidate | None:
    """One epoch's choice: filter on the hard constraints, then optimise.

    Returns None when nothing survives the filter — a deferral, which the
    design treats as a result worth reporting rather than a failure to hide.
    """
    feasible = filter_candidates(candidates, cfg["constraints"]["hard"],
                                 violations)
    if not feasible:
        return None

    weights = cfg["objective"]["weight_scenarios"][cfg["objective"]["active_weights"]]
    soft = cfg["constraints"]["soft"]

    return min(feasible, key=lambda c: score(
        c, weights, scales,
        workload_share=workload_shares.get(c.operator, 0.0),
        switching=(current_machine.get(c.operator) not in (None, c.machine)),
        soft=soft,
    ))
