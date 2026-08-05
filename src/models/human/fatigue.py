"""
T5.8 — the fatigue model (design §4.1, §4.4).

Kept as pure functions so the equations can be tested on their own, without a
simulation around them.

The published form (Calzavara et al. 2019, confirmed against Sgarbossa &
Vijayakumar 2020 Eq. 3, 4, 9) is an exponential approach towards whatever
energy expenditure the current activity demands:

    F(t + dt) = E* + (F(t) - E*) * exp(-rho * dt)

        E*   = E_w(tau)  while working, the task's metabolic demand
             = E_rest    while resting or idle
        rho  = lambda    when E* >= F, i.e. fatigue is building
             = mu        when E* <  F, i.e. the operator is recovering

Fatigue therefore rises only as far as the task actually demands. Light work
never exhausts anyone, which is the whole reason for using energy expenditure
rather than an abstract 0-1 counter.

*** lambda and mu are CALIBRATED, not measured, and appear in no publication.
    Never attribute them to Calzavara et al. — only the FORM comes from there.
    docs/04-framework-design.md §4.5 has the wording to use. ***
"""

from __future__ import annotations

import math


def relax(current: float, target: float, rate: float, minutes: float) -> float:
    """One exponential step towards `target`. This is the equation above."""
    if minutes <= 0:
        return current
    return target + (current - target) * math.exp(-rate * minutes)


def step(current: float, e_star: float, minutes: float,
         lam: float, mu: float) -> float:
    """Advance fatigue by `minutes` spent at an activity demanding `e_star`.

    The rate switches on direction: building fatigue uses lambda, shedding it
    uses mu. mu > lambda, so recovery is faster than accumulation.
    """
    rate = lam if e_star >= current else mu
    return relax(current, e_star, rate, minutes)


def normalise(fatigue: float, e_rest: float, awl: float) -> float:
    """Design §4.4 — fatigue as a fraction of this operator's own headroom.

        F_hat = clip((F - E_rest) / (AWL - E_rest), 0, 1)

    This is where personalisation enters. The same absolute effort lands at a
    different F_hat for each operator, because AWL is computed from their age,
    sex and weight. A single threshold of 0.80 then protects three people
    differently without a single rule being written per person.
    """
    band = awl - e_rest
    if band <= 0:
        raise ValueError("AWL must exceed the resting rate")
    return max(0.0, min(1.0, (fatigue - e_rest) / band))


def half_life_minutes(rate: float) -> float:
    """Convenience for reporting: ln(2)/rate."""
    return math.log(2) / rate
