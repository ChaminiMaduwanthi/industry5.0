"""
T5.3 — runtime state for the three things that move during a shift.

These are deliberately thin. They hold what a task, a machine and an operator
*are doing right now*, and nothing about how they degrade or tire: machine
health belongs to MachineTwin (T5.4) and fatigue to HumanTwin (T5.7). Keeping
that split means the walking skeleton can be trusted before any twin equation
exists, and a twin can later be swapped in without touching the clock.

The static properties (L0, AWL, skill, energy demand) stay in loader.py — the
records here only carry the identifier and point back to the spec.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: int
    task_type: str                      # L / M / H
    released_min: float                 # when it entered the queue

    assigned_operator: str | None = None
    assigned_machine: str | None = None
    started_min: float | None = None
    finished_min: float | None = None

    @property
    def is_done(self) -> bool:
        return self.finished_min is not None

    @property
    def waiting_time(self) -> float | None:
        if self.started_min is None:
            return None
        return self.started_min - self.released_min


@dataclass
class MachineState:
    machine_id: str
    busy: bool = False
    under_maintenance: bool = False
    busy_minutes: float = 0.0
    tasks_done: int = 0

    # Energy is accumulated here because it is pure bookkeeping over the
    # equation E = e_idle + 1[busy] * delta_e(tau) (design §3.2). The idle
    # term is added once at the end of the shift for every machine.
    variable_energy_kwh: float = 0.0

    def available(self) -> bool:
        return not self.busy and not self.under_maintenance


@dataclass
class OperatorState:
    operator_id: str
    busy: bool = False
    on_break: bool = False
    busy_minutes: float = 0.0
    tasks_done: int = 0
    tasks_by_type: dict[str, int] = field(default_factory=dict)

    def available(self) -> bool:
        return not self.busy and not self.on_break

    def record(self, task_type: str, minutes: float) -> None:
        self.busy_minutes += minutes
        self.tasks_done += 1
        self.tasks_by_type[task_type] = self.tasks_by_type.get(task_type, 0) + 1


def workload_gini(busy_minutes: list[float]) -> float:
    """Gini coefficient of the workload share (design §4.9).

    0 means the shift was shared perfectly evenly, 1 means one operator did
    everything. This is soft constraint SC1 and a reported KPI, so it is worth
    having from the very first run.
    """
    n = len(busy_minutes)
    total = sum(busy_minutes)
    if n == 0 or total == 0:
        return 0.0
    mean = total / n
    diffs = sum(abs(a - b) for a in busy_minutes for b in busy_minutes)
    return diffs / (2 * n * n * mean)
