"""
T5.7 — the human digital twin (design §4).  ★ the novelty of this work ★

Holds the six operator state variables and advances them on the same clock as
the machine twin:

    F      fatigue, kcal/min          exponential work-recovery      §4.1
    F_hat  normalised fatigue [0,1]   against THIS operator's AWL    §4.4
    S      skill                      static within a shift          §4.6
    R      ergonomic risk [1,7]       RULA + fatigue + CP5           §4.7
    C      cognitive load [0,1]       task + CP3 + defect risk       §4.8
    W      workload share [0,1]       busy minutes / total           §4.9

What makes this a twin rather than a rule: nothing here is a policy. F evolves
from the operator's own physiology — resting expenditure from Mifflin-St Jeor
and acceptable work level from Price — so OP2, who is smaller and older than
OP1, reaches the same F_hat sooner on the same task. The scheduler never has to
be told that. It falls out of the equations.

Fatigue advances once per decision epoch, in two segments: the minutes actually
worked, then the minutes idle. The exponential composes, so applying the two in
sequence is exact for the piecewise-constant demand within an epoch.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from loader import OperatorSpec
from models.human import cognitive, ergonomics, fatigue as fat


@dataclass
class HumanTwin:
    spec: OperatorSpec
    cfg: dict

    fatigue: float = 0.0
    ergonomic_risk: float = 1.0
    cognitive_load: float = 0.0

    # accumulated within the current epoch, cleared by `advance`
    epoch_busy_minutes: float = 0.0
    epoch_energy_minutes: float = 0.0     # sum of E_w * minutes

    fatigue_trace: list[float] = field(default_factory=list)
    peak_fatigue_hat: float = 0.0
    rula_samples: list[float] = field(default_factory=list)
    cognitive_samples: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        # A shift starts rested: expenditure sits at the operator's own
        # resting rate, which is F_hat = 0 by construction.
        self.fatigue = self.spec.e_rest_kcal_min

    # --- §4.4 normalised fatigue -----------------------------------------
    @property
    def fatigue_hat(self) -> float:
        return fat.normalise(self.fatigue, self.spec.e_rest_kcal_min,
                             self.spec.awl_kcal_min)

    # --- bookkeeping fed by the simulation --------------------------------
    def record_work(self, minutes: float, energy_demand: float) -> None:
        """Called when the operator finishes a task within this epoch."""
        self.epoch_busy_minutes += minutes
        self.epoch_energy_minutes += energy_demand * minutes

    # --- §4.1 the fatigue step -------------------------------------------
    def advance(self, epoch_minutes: float) -> None:
        """Move fatigue on by one decision epoch."""
        lam = self.cfg["fatigue"]["lambda_per_min"]
        mu = self.cfg["fatigue"]["mu_per_min"]

        worked = min(self.epoch_busy_minutes, epoch_minutes)
        rested = max(0.0, epoch_minutes - worked)

        if worked > 0:
            # CP4 — the task's own metabolic demand is the asymptote. Where
            # several tasks fell in one epoch, their time-weighted demand is
            # the equivalent constant.
            e_star = self.epoch_energy_minutes / self.epoch_busy_minutes
            self.fatigue = fat.step(self.fatigue, e_star, worked, lam, mu)

        if rested > 0:
            self.fatigue = fat.step(self.fatigue, self.spec.e_rest_kcal_min,
                                    rested, lam, mu)

        self.epoch_busy_minutes = 0.0
        self.epoch_energy_minutes = 0.0

        f_hat = self.fatigue_hat
        self.fatigue_trace.append(f_hat)
        self.peak_fatigue_hat = max(self.peak_fatigue_hat, f_hat)

    # --- §4.7 ergonomic risk ---------------------------------------------
    def rula(self, task_rula_base: int, machine_speed_hat: float) -> float:
        erg = self.cfg["ergonomics"]
        return ergonomics.rula(
            base=task_rula_base,
            fatigue_hat=self.fatigue_hat,
            machine_speed_hat=machine_speed_hat,
            psi1=erg["psi1_fatigue"],
            psi2=erg["psi2_machine_speed"],
        )

    # --- §4.8 cognitive load ---------------------------------------------
    def cognition(self, task_base: float, machine_health: float,
                  defect_risk: float, machines_watched: int,
                  machines_total: int) -> float:
        cog = self.cfg["cognitive"]
        return cognitive.cognitive_load(
            task_base=task_base,
            machine_health=machine_health,
            defect_risk=defect_risk,
            machines_watched=machines_watched,
            machines_total=machines_total,
            gamma1=cog["gamma1_machine_health"],
            gamma2=cog["gamma2_defect_risk"],
            gamma3=cog["gamma3_multi_machine"],
        )

    def observe(self, rula_score: float, cognitive: float) -> None:
        """Store what the operator was exposed to, for the shift KPIs."""
        self.ergonomic_risk = rula_score
        self.cognitive_load = cognitive
        self.rula_samples.append(rula_score)
        self.cognitive_samples.append(cognitive)

    # --- reporting --------------------------------------------------------
    @property
    def mean_rula(self) -> float:
        return (sum(self.rula_samples) / len(self.rula_samples)
                if self.rula_samples else float(self.ergonomic_risk))

    @property
    def mean_cognitive(self) -> float:
        return (sum(self.cognitive_samples) / len(self.cognitive_samples)
                if self.cognitive_samples else 0.0)
