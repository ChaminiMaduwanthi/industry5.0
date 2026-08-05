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


def machine_speed_hat(efficiency_factor: float, slowest: float,
                      fastest: float) -> float:
    """CP5 input — how fast THIS machine paces its operator, on [0,1].

    The design leaves 'normalised machine speed' abstract because the machine
    twin carries no explicit speed variable, so a stand-in is needed. It has to
    be a property of the machine.

    Power draw was tried first and is wrong: draw is dominated by the task
    class, so every heavy task scored 1.0. Task intensity is already in the
    equation twice over — as RULA_base(tau) here and as kappa in the wear
    model — so feeding it in a third time through CP5 double counts it. The
    effect was not subtle. RULA_base(H) is 4 and psi2 is 1.0, so heavy work
    started at 5 before any fatigue and HC3 (R <= 5) rejected it for anyone not
    perfectly fresh. Heavy tasks became almost unassignable, and the whole team
    sat blocked in a quarter of all epochs.

    The per-machine efficiency spread is used instead. It varies by machine and
    not by task, which is what a pace term should do.
    """
    span = fastest - slowest
    if span <= 0:
        return 0.0
    return max(0.0, min(1.0, (efficiency_factor - slowest) / span))
