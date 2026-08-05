"""
T5.8 — ergonomic risk (design §4.7).

    R = clip( RULA_base(tau) + psi1 * F_hat + psi2 * v_hat , 1, 7 )
                    |                |               |
       McAtamney &  |         fatigue worsens        |  CP5
       Corlett 1993 |            posture             |

RULA is a 1-7 observational score. The base value per task type comes from the
design; the two additions model what a static observational score cannot see —
that a tired operator holds a worse posture, and that a faster machine forces a
faster, less controlled movement.

    psi1 = 2.0   a fully fatigued operator adds two RULA points
    psi2 = 1.0   a machine at full pace adds one

HC3 rejects any pairing scoring above 5, which is the RULA action level at
which investigation and change are required.
"""

from __future__ import annotations

RULA_MIN, RULA_MAX = 1, 7


def rula(base: int, fatigue_hat: float, machine_speed_hat: float,
         psi1: float, psi2: float) -> float:
    """Design §4.7. Inputs are normalised to [0,1]; the result is 1-7."""
    score = base + psi1 * fatigue_hat + psi2 * machine_speed_hat
    return max(RULA_MIN, min(RULA_MAX, score))


def machine_speed_hat(energy_rate: float, idle_rate: float,
                      max_rate: float) -> float:
    """CP5 input — how hard the machine is being driven, on [0,1].

    The design leaves 'normalised machine speed' abstract because the machine
    twin carries no explicit speed variable. Power draw is used as the stand-in:
    a machine pulling close to its maximum is running its heaviest duty, which
    is exactly the condition that paces the operator. It is a modelling choice,
    recorded here rather than buried, and it only ever scales the psi2 term.
    """
    span = max_rate - idle_rate
    if span <= 0:
        return 0.0
    return max(0.0, min(1.0, (energy_rate - idle_rate) / span))
