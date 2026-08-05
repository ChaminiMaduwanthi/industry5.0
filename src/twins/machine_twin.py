"""
T5.4 — the machine digital twin (design §3).

Holds the four machine state variables and the equations that move them:

    H  health        H(t+dt) = max(0, H - dt * kappa_tau / L0)      §3.1
    E  energy        E(t)    = e_idle + 1[busy] * delta_e(tau)      §3.2
    Q  defect risk   Q = sigma(b0 + b1(1-H) + b2(1-S) + b3*F + b4*k) §3.3
    A  availability  A = 1[H > H_min] * 1[not under maintenance]    §3.4

Degradation is charged for the exact minutes a machine spent working rather
than once per epoch, so a task that straddles an epoch boundary is accounted
for correctly. Idle machines do not degrade at all (kappa = 0).

Q is where the two twins meet. Both couplings are in the equation already:
CP1 (skill) works now because skill is static, while CP2 (fatigue) needs the
human twin, so `fatigue_hat` is passed in and defaults to 0 until T5.7 wires
it up. That default is the ONLY thing missing here — the term itself is live.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from loader import MachineSpec


@dataclass
class MachineTwin:
    spec: MachineSpec
    cfg: dict

    health: float = 1.0
    under_maintenance: bool = False
    broken: bool = False                # hit by an S3 breakdown, not wear
    maintenance_events: int = 0
    breakdown_events: int = 0
    maintenance_minutes: float = 0.0
    degraded_minutes: float = 0.0
    health_trace: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.health = self.cfg["machines"]["health_init"]

    # --- §3.1 health ------------------------------------------------------
    def degrade(self, minutes: float, kappa: float) -> None:
        """Charge wear for `minutes` of work at task severity `kappa`."""
        self.health = max(0.0, self.health - minutes * kappa / self.spec.L0_minutes)
        self.degraded_minutes += minutes

    def restore(self) -> None:
        """A completed maintenance action returns the machine to nominal."""
        self.health = self.cfg["machines"]["health_after_maintenance"]
        self.under_maintenance = False
        self.broken = False

    def fail_now(self) -> None:
        """Force an immediate breakdown — used to inject the S3 disruption."""
        self.health = 0.0

    # --- §3.4 availability ------------------------------------------------
    @property
    def health_min(self) -> float:
        return self.cfg["machines"]["health_min_operational"]

    def needs_maintenance(self) -> bool:
        return self.health <= self.health_min and not self.under_maintenance

    def available(self) -> bool:
        return self.health > self.health_min and not self.under_maintenance

    # --- §3.2 energy ------------------------------------------------------
    def energy_rate(self, task_type: str | None) -> float:
        """kWh per hour: idle draw plus the task increment when working."""
        e = self.spec.e_idle_kwh_per_h
        if task_type is not None:
            e += self.spec.delta_e_kwh_per_h[task_type]
        return e

    # --- §3.3 quality — where the twins meet ------------------------------
    def defect_risk(self, skill: float, kappa: float,
                    fatigue_hat: float = 0.0) -> float:
        b = self.cfg["quality"]["fallback_coefficients"]
        z = (b["b0"]
             + b["b1"] * (1.0 - self.health)      # machine degradation
             + b["b2"] * (1.0 - skill)            # CP1  skill      -> quality
             + b["b3"] * fatigue_hat              # CP2  fatigue    -> quality
             + b["b4"] * kappa)                   # task severity
        return 1.0 / (1.0 + math.exp(-z))
