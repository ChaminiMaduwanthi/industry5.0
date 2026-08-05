"""
T5.3 — the discrete-event shift clock.

This is the walking skeleton. It runs one full shift end to end with a random
allocator, which is baseline B1. What it deliberately does NOT do yet:

    no machine health decay      -> T5.4  MachineTwin
    no fatigue or ergonomics     -> T5.7  HumanTwin
    no coupling CP1-CP5          -> T5.9
    no hard constraints          -> T5.11 (they filter before the optimiser)
    no optimiser                 -> T5.11 / T5.12

Those slot in at exactly one place each: `allocate` is the seam for the
decision layer, and the epoch loop is where twin updates will be called. Every
number comes from loader.py, so nothing here needs editing when a parameter
changes.

Run:  python src/simulation/factory.py
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

import simpy

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loader import Setup, load_setup                       # noqa: E402
from simulation.entities import (                          # noqa: E402
    MachineState, OperatorState, Task, workload_gini,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Flip to True in T5.4, once machine health can drive a breakdown.
_FAILURES_SUPPORTED = False
_warned: set[str] = set()


# =============================================================================
@dataclass
class ShiftState:
    setup: Setup
    machines: dict[str, MachineState]
    operators: dict[str, OperatorState]
    rng: random.Random
    rng_seed: int
    allocator: object                   # (state, rng) -> [(task, op, machine)]
    queue: list[Task] = field(default_factory=list)
    completed: list[Task] = field(default_factory=list)
    epoch_log: list[dict] = field(default_factory=list)
    on_epoch: object = None             # optional observer, called each epoch

    # Epochs where work waited even though a free operator and a free machine
    # both existed. Design §8 calls this the direct answer to "how much
    # throughput was given up to protect the operator". No constraint exists
    # yet, so this must read 0 until T5.11 — if it ever does not, the
    # allocator is dropping work it could have done.
    deferral_epochs: int = 0


# =============================================================================
# Allocators — the seam the decision layer plugs into
# =============================================================================
def random_allocator(state: ShiftState, rng: random.Random
                     ) -> list[tuple[Task, str, str]]:
    """Baseline B1: pair pending tasks with whoever and whatever is free.

    No twin state is consulted and no constraint is applied. T5.11 replaces
    this with the constrained weighted-sum decision, keeping the signature.
    """
    free_ops = [o for o, s in state.operators.items() if s.available()]
    free_machines = [m for m, s in state.machines.items() if s.available()]
    pending = [t for t in state.queue if t.assigned_operator is None]

    rng.shuffle(free_ops)
    rng.shuffle(free_machines)

    assignments = []
    for task in pending:
        if not free_ops or not free_machines:
            break
        assignments.append((task, free_ops.pop(), free_machines.pop()))
    return assignments


# =============================================================================
# Processes
# =============================================================================
def _work(env: simpy.Environment, state: ShiftState,
          task: Task, op_id: str, mac_id: str):
    """Occupy one operator and one machine for the processing time."""
    setup = state.setup
    op, mac = state.operators[op_id], state.machines[mac_id]

    op.busy = mac.busy = True
    op.current_task_type = mac.current_task_type = task.task_type
    op.current_machine = mac_id
    task.assigned_operator, task.assigned_machine = op_id, mac_id
    task.started_min = env.now

    minutes = setup.processing_time(task.task_type, op_id)
    yield env.timeout(minutes)

    task.finished_min = env.now
    op.record(task.task_type, minutes)
    mac.busy_minutes += minutes
    mac.tasks_done += 1
    mac.variable_energy_kwh += (
        setup.machines[mac_id].delta_e_kwh_per_h[task.task_type] * minutes / 60
    )

    op.busy = mac.busy = False
    op.current_task_type = mac.current_task_type = None
    op.current_machine = None
    state.queue.remove(task)
    state.completed.append(task)

    # An operator who finishes mid-epoch must not stand idle until the next
    # epoch boundary: the decision epoch sets how often the plan is recomputed,
    # not how often a free pair may start work. Without this, the mean task
    # length (~15 min) and the epoch length (15 min) interact to waste roughly
    # a third of the available capacity, purely as an artefact of the clock.
    _dispatch(env, state)


def _dispatch(env: simpy.Environment, state: ShiftState) -> int:
    """Run the current allocator and start work on whatever it returns."""
    assignments = state.allocator(state, state.rng)
    for task, op_id, mac_id in assignments:
        env.process(_work(env, state, task, op_id, mac_id))
    return len(assignments)


def _epoch_loop(env: simpy.Environment, state: ShiftState):
    """Once per decision epoch: update twins, then decide (design §9)."""
    setup = state.setup
    sim = setup.cfg["simulation"]
    break_start = sim["break_after_minutes"]
    break_end = break_start + sim["break_duration_minutes"]

    while True:
        # --- scheduled break --------------------------------------------
        on_break = break_start <= env.now < break_end
        for o in state.operators.values():
            o.on_break = on_break

        # --- twin updates go here (T5.4, T5.7, T5.9) --------------------

        # --- decide ------------------------------------------------------
        n_assigned = _dispatch(env, state)

        # Let the work just started actually begin before the state is
        # sampled, otherwise every log line reports the previous epoch's
        # occupancy and every downstream utilisation figure is wrong.
        yield env.timeout(0)

        # A deferral is work waiting while a free operator AND a free machine
        # both exist and the allocator still refused to pair them — that only
        # happens when a constraint forbids every remaining combination
        # (design §8). Counting "nothing was assigned" instead would count
        # every epoch where the team simply happened to be busy, which is not
        # a deferral at all and would inflate the figure roughly tenfold.
        pending = sum(1 for t in state.queue if t.assigned_operator is None)
        free_op = any(o.available() for o in state.operators.values())
        free_mac = any(m.available() for m in state.machines.values())
        if pending and free_op and free_mac and not n_assigned:
            state.deferral_epochs += 1

        state.epoch_log.append({
            "epoch": len(state.epoch_log),
            "clock_min": env.now,
            "busy_machines": sum(m.busy for m in state.machines.values()),
            "busy_operators": sum(o.busy for o in state.operators.values()),
            "on_break": on_break,
            "queue_pending": pending,
            "completed": len(state.completed),
        })

        # Observation hook. watch.py draws the live view through this, and the
        # Streamlit dashboard (T5.14) will use the same one. Nothing inside the
        # simulation depends on it.
        if state.on_epoch is not None:
            state.on_epoch(state)

        yield env.timeout(setup.epoch_minutes)


# =============================================================================
def build_task_queue(setup: Setup, rng: random.Random) -> list[Task]:
    """All of the shift's work is released at the start.

    Demand arrives as a fixed order book rather than a stochastic stream: every
    baseline then faces exactly the same work for a given seed, so differences
    between B1, B2 and B3 come from the decisions and not from luck in arrivals.
    """
    sim = setup.cfg["simulation"]
    n = round(sim["tasks_per_shift"] * setup.scenario_cfg["demand_multiplier"])
    mix = sim["task_type_mix"]
    types, weights = list(mix.keys()), list(mix.values())
    return [Task(task_id=i, task_type=rng.choices(types, weights)[0],
                 released_min=0.0)
            for i in range(n)]


def run_shift(setup: Setup, seed: int = 0, allocator=random_allocator,
              verbose: bool = False, on_epoch=None) -> dict:
    # S3 injects mid-shift breakdowns, which need machine health to exist.
    # Until T5.4 lands, S3 is silently identical to S1 — say so out loud rather
    # than let a whole result table be produced from a scenario that never ran.
    if (setup.scenario_cfg.get("machine_failures", 0)
            and not _FAILURES_SUPPORTED and setup.scenario not in _warned):
        _warned.add(setup.scenario)
        print(f"  ! scenario {setup.scenario} asks for "
              f"{setup.scenario_cfg['machine_failures']} machine failures, "
              f"which need MachineTwin (T5.4). Running without them "
              f"— {setup.scenario} currently equals S1.")

    rng = random.Random(seed)
    env = simpy.Environment()

    state = ShiftState(
        setup=setup,
        machines={m: MachineState(m) for m in setup.machines},
        operators={o: OperatorState(o) for o in setup.operators},
        rng=rng,
        rng_seed=seed,
        allocator=allocator,
        on_epoch=on_epoch,
    )
    state.queue = build_task_queue(setup, rng)
    total_demand = len(state.queue)

    env.process(_epoch_loop(env, state))
    env.run(until=setup.shift_minutes)

    return summarise(state, total_demand, seed, verbose)


# =============================================================================
def summarise(state: ShiftState, total_demand: int, seed: int,
              verbose: bool) -> dict:
    setup = state.setup
    hours = setup.shift_minutes / 60
    ef = setup.cfg["sustainability"]["emission_factor_kg_co2_per_kwh"]

    idle_kwh = sum(setup.machines[m].e_idle_kwh_per_h for m in state.machines) * hours
    var_kwh = sum(m.variable_energy_kwh for m in state.machines.values())
    energy = idle_kwh + var_kwh

    units = len(state.completed)
    busy = [o.busy_minutes for o in state.operators.values()]

    result = {
        "seed": seed,
        "scenario": setup.scenario,
        "demand": total_demand,
        "throughput": units,
        "unfinished": total_demand - units,
        "energy_kwh": round(energy, 3),
        "energy_per_unit": round(energy / units, 4) if units else None,
        "co2e_kg": round(energy * ef, 3),
        "machine_utilisation": round(
            sum(m.busy_minutes for m in state.machines.values())
            / (len(state.machines) * setup.shift_minutes), 4),
        "operator_utilisation": round(
            sum(busy) / (len(busy) * setup.shift_minutes), 4),
        "workload_gini": round(workload_gini(busy), 4),
        "deferral_epochs": state.deferral_epochs,
    }

    if verbose:
        _print_report(state, result)
    return result


def _print_report(state: ShiftState, r: dict) -> None:
    setup = state.setup
    print(f"=== shift trace · scenario {r['scenario']} · seed {r['seed']} "
          f"· allocator: random (B1) ===")
    print()
    print("epoch  clock   machines  operators  queue  done  note")
    for e in state.epoch_log:
        h, m = divmod(int(e["clock_min"]), 60)
        note = "break" if e["on_break"] else ""
        print(f"  {e['epoch']:3d}  {8 + h:02d}:{m:02d}   "
              f"{e['busy_machines']}/{len(state.machines)}       "
              f"{e['busy_operators']}/{len(state.operators)}       "
              f"{e['queue_pending']:4d}  {e['completed']:4d}  {note}")

    print()
    print("=== shift summary ===")
    print(f"  demand                {r['demand']} tasks")
    print(f"  completed             {r['throughput']}  "
          f"(unfinished {r['unfinished']})")
    print(f"  energy                {r['energy_kwh']} kWh  "
          f"-> {r['co2e_kg']} kg CO2e")
    print(f"  energy per unit       {r['energy_per_unit']} kWh")
    print(f"  machine utilisation   {r['machine_utilisation']:.1%}")
    print(f"  operator utilisation  {r['operator_utilisation']:.1%}")
    print(f"  workload Gini         {r['workload_gini']}  (0 = perfectly even)")
    print()
    print("  per operator:")
    for o in state.operators.values():
        share = o.busy_minutes / setup.shift_minutes
        by = " ".join(f"{t}:{n}" for t, n in sorted(o.tasks_by_type.items()))
        print(f"    {o.operator_id}  {o.busy_minutes:6.1f} min  "
              f"({share:5.1%})  {o.tasks_done:3d} tasks   {by}")
    print()
    print("  per machine:")
    for m in state.machines.values():
        share = m.busy_minutes / setup.shift_minutes
        print(f"    {m.machine_id}  {m.busy_minutes:6.1f} min  "
              f"({share:5.1%})  {m.tasks_done:3d} tasks  "
              f"{m.variable_energy_kwh:6.2f} kWh variable")


# =============================================================================
if __name__ == "__main__":
    setup = load_setup(scenario="S1")
    run_shift(setup, seed=0, verbose=True)

    print()
    print("=== determinism check ===")
    a = run_shift(setup, seed=0)
    b = run_shift(setup, seed=0)
    c = run_shift(setup, seed=1)
    print(f"  same seed  -> identical: {a == b}")
    print(f"  other seed -> different: {a != c}")

    print()
    print("=== demand pressure across scenarios (S2 is the stress case) ===")
    for sc in setup.cfg["experiment"]["scenarios"]:
        s = load_setup(scenario=sc)
        r = run_shift(s, seed=0)
        print(f"  {sc}: demand {r['demand']:3d}  completed {r['throughput']:3d}  "
              f"unfinished {r['unfinished']:3d}  "
              f"operator util {r['operator_utilisation']:.1%}")
