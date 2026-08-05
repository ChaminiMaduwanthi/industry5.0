"""
T5.8 — cognitive load (design §4.8), a NASA-TLX style proxy.

    C = clip( c_tau + gamma1*(1 - H_m) + gamma2*Q_m + gamma3*(n-1)/(|M|-1), 0, 1)
                |            |               |                  |
          task baseline   CP3: a failing   defect risk    machines watched
                          machine needs                    at once
                          more attention

    gamma1 = 0.30   gamma2 = 0.20   gamma3 = 0.15      (Hart & Staveland, 1988)

CP3 is the one that matters for the argument: a degrading machine does not only
cost availability, it costs the operator attention. A framework that models the
machine alone cannot see that.
"""

from __future__ import annotations


def cognitive_load(task_base: float, machine_health: float, defect_risk: float,
                   machines_watched: int, machines_total: int,
                   gamma1: float, gamma2: float, gamma3: float) -> float:
    """Design §4.8. Returns a value on [0,1]."""
    spread = 0.0
    if machines_total > 1:
        spread = (machines_watched - 1) / (machines_total - 1)

    load = (task_base
            + gamma1 * (1.0 - machine_health)     # CP3
            + gamma2 * defect_risk
            + gamma3 * spread)
    return max(0.0, min(1.0, load))
