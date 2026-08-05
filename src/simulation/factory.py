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
from decision.constraints import Candidate, Violations, update_rest_state  # noqa: E402
from decision.weighted import decide                       # noqa: E402
from models.human.ergonomics import machine_speed_hat      # noqa: E402
from models.sustainability import account, marginal_energy_kwh  # noqa: E402
from twins.human_twin import HumanTwin                     # noqa: E402
from twins.machine_twin import MachineTwin                 # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Offset for the disruption stream. Breakdown times and victims must be drawn
# from a generator the allocator never touches, otherwise B1, B2 and B3 would
# each face a different disruption on the same seed and S3 would compare
# nothing. With this, one seed means one identical set of failures for every
# baseline.
_FAILURE_SEED_OFFSET = 10_000


# =============================================================================
@dataclass
class ShiftState:
    setup: Setup
    machines: dict[str, MachineState]
    operators: dict[str, OperatorState]
    twins: dict[str, MachineTwin]
    humans: dict[str, HumanTwin]
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
    scrap_units: int = 0
    ideal_minutes: float = 0.0     # nominal time of completed work, for OEE
    violations: Violations = field(default_factory=Violations)

    # --- availability, in one place ---------------------------------------
    # Every allocator must go through these. Availability is not just "is it
    # idle": design §3.4 makes it A = 1[H > H_min] AND 1[not maintenance], and
    # the health half of that lives on the twin. An allocator that filtered on
    # the entity alone would happily start work on a machine that had just worn
    # through its floor, because `env.process` only queues the maintenance
    # routine — it does not run it before the next synchronous dispatch.
    def free_machines(self) -> list[str]:
        return [m for m, s in self.machines.items()
                if s.available() and self.twins[m].available()]

    def free_operators(self) -> list[str]:
        """Idle, not on a scheduled break, and not on a mandatory HC1 rest."""
        return [o for o, s in self.operators.items()
                if s.available() and not self.humans[o].resting]

    def enforces(self, constraint: str) -> bool:
        """Whether the ACTIVE POLICY enforces a constraint.

        Constraints belong to the baseline, not to the factory. A mandatory
        rest is something a human-aware scheduler decides to grant; a
        throughput-only scheduler does not, and if the simulation granted it
        anyway the comparison would measure nothing. Each allocator declares
        what it enforces.
        """
        return constraint in getattr(self.allocator, "enforces", frozenset())

    def pending_tasks(self) -> list[Task]:
        return [t for t in self.queue if t.assigned_operator is None]


# =============================================================================
# Allocators — the seam the decision layer plugs into
# =============================================================================
def build_candidates(state: ShiftState, task: Task, operators: list[str],
                     machines: list[str], ablate: frozenset = frozenset()
                     ) -> list[Candidate]:
    """Cost every way this task could be run, for the decision layer to weigh.

    `ablate` hides a coupling from the SCHEDULER. The factory is unchanged: a
    tired operator still makes more mistakes with CP2 ablated, the decision
    simply cannot take that into account. Removing a coupling from the physics
    as well would score each ablation in a different world.
    """
    setup = state.setup
    spec = setup.tasks[task.task_type]
    lo, hi = setup.pace_range()
    out = []

    for op_id in operators:
        human = state.humans[op_id]
        skill = setup.operators[op_id].skill[task.task_type]
        minutes = setup.processing_time(task.task_type, op_id)

        for mac_id in machines:
            twin = state.twins[mac_id]
            speed = machine_speed_hat(twin.spec.efficiency_factor, lo, hi)
            # What the scheduler is allowed to notice.
            seen_speed = 0.0 if "CP5" in ablate else speed
            seen_skill = 1.0 if "CP1" in ablate else skill
            seen_fatigue = 0.0 if "CP2" in ablate else human.fatigue_hat
            out.append(Candidate(
                task=task, operator=op_id, machine=mac_id,
                processing_minutes=minutes,
                skill=skill,
                fatigue_hat=human.fatigue_hat,
                fatigue_after=human.predict_fatigue_hat(
                    minutes, spec.energy_demand_kcal_min),
                rula=human.rula(spec.rula_base, seen_speed),
                defect_risk=twin.defect_risk(
                    skill=seen_skill, kappa=spec.severity_kappa,
                    fatigue_hat=seen_fatigue),
                marginal_kwh=marginal_energy_kwh(
                    twin.spec.delta_e_kwh_per_h[task.task_type], minutes),
            ))
    return out


def weighted_allocator(state: ShiftState, rng: random.Random
                       ) -> list[tuple[Task, str, str]]:
    """B3a — hard constraints filter, then the weighted sum picks (design §9).

    Greedy across the pending queue: each task takes the best assignment still
    available, then the pair it used is withdrawn. A task with no feasible
    option is left in the queue, which is the deferral the design asks to be
    reported rather than hidden.
    """
    setup = state.setup
    free_ops = state.free_operators()
    free_macs = state.free_machines()

    scales = {
        "max_minutes": max(setup.processing_time(t, o)
                           for t in setup.tasks for o in setup.operators),
        "max_marginal_kwh": max(
            marginal_energy_kwh(m.delta_e_kwh_per_h[t],
                                setup.processing_time(t, o))
            for m in setup.machines.values()
            for t in setup.tasks for o in setup.operators),
    }
    shares = {o: s.busy_minutes / setup.shift_minutes
              for o, s in state.operators.items()}
    current = {o: s.current_machine for o, s in state.operators.items()}

    ablate = getattr(state.allocator, "ablate", frozenset())
    assignments = []
    for task in state.pending_tasks():
        if not free_ops or not free_macs:
            break
        chosen = decide(
            build_candidates(state, task, free_ops, free_macs, ablate),
            setup.cfg, scales, shares, current, state.violations)
        if chosen is None:
            continue                       # deferred: no feasible pairing
        assignments.append((task, chosen.operator, chosen.machine))
        free_ops.remove(chosen.operator)
        free_macs.remove(chosen.machine)
    return assignments


def industry40_allocator(state: ShiftState, rng: random.Random
                         ) -> list[tuple[Task, str, str]]:
    """B2 — the Industry 4.0 baseline (design §11).

    Deliberately the SAME framework under restrictions, not separate code, so
    the comparison cannot be accused of pitting two different simulators
    against each other. What it keeps and what it drops:

        machine twin   full strength. HC4 still removes a machine that has
                       worn past its floor, so B2 protects its equipment as
                       well as B3 does.
        human twin     still running. Fatigue, ergonomic risk and cognitive
                       load are all computed and reported — otherwise there
                       would be no B2 figures to compare against. They simply
                       do not enter the decision.
        objective      throughput alone: take the fastest pairing available.
        constraints    HC4 only. No fatigue limit, no skill floor, no
                       ergonomic ceiling, no mandatory rest.

    ⚠️ The physical couplings are NOT switched off under B2. A tired operator
    still makes more mistakes here, because that happens in the factory whether
    or not the scheduler models it. Disabling CP2 for B2 would simulate a
    different, kinder world for it and flatter its quality figures. Design §11
    says the human twin is invisible to the OPTIMISER; it does not say the
    physics changes. This reading is what keeps the comparison honest, and it
    is the one to state in the methodology.
    """
    setup = state.setup
    free_ops = state.free_operators()
    free_macs = state.free_machines()

    assignments = []
    for task in state.pending_tasks():
        if not free_ops or not free_macs:
            break
        # Fastest operator for this task. Machine choice does not change the
        # rate, so it is made on service timing: run down whatever is closest
        # to its floor and keep fresh capacity in reserve. Taking the
        # HEALTHIEST instead equalises wear across the fleet, which sounds
        # tidy and is worse — the machines then reach the floor together and
        # go out of service together. Measured, that cost B2 enough throughput
        # to fall behind random assignment, which would have made it a straw
        # opponent. Staggering service is also exactly what a machine twin is
        # for, so this is the Industry 4.0 strategy rather than a patch.
        op = min(free_ops, key=lambda o: setup.processing_time(task.task_type, o))
        mac = min(free_macs, key=lambda m: state.twins[m].health)
        assignments.append((task, op, mac))
        free_ops.remove(op)
        free_macs.remove(mac)
    return assignments


def random_allocator(state: ShiftState, rng: random.Random
                     ) -> list[tuple[Task, str, str]]:
    """Baseline B1: pair pending tasks with whoever and whatever is free.

    No twin state is consulted and no constraint is applied. T5.11 replaces
    this with the constrained weighted-sum decision, keeping the signature.
    """
    free_ops = state.free_operators()
    free_machines = state.free_machines()
    pending = state.pending_tasks()

    rng.shuffle(free_ops)
    rng.shuffle(free_machines)

    assignments = []
    for task in pending:
        if not free_ops or not free_machines:
            break
        assignments.append((task, free_ops.pop(), free_machines.pop()))
    return assignments


# What each policy enforces. HC4 is not listed because it is not a scheduling
# preference — a machine below its floor is under maintenance and physically
# unavailable to every policy alike. The human constraints are the ones that
# separate a human-aware scheduler from a throughput-only one, so they belong
# to the policy and are declared here.
random_allocator.enforces = frozenset()                       # B1
industry40_allocator.enforces = frozenset()                   # B2 — HC4 only
weighted_allocator.enforces = frozenset({"HC1", "HC2", "HC3"})  # B3a


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

    twin, human = state.twins[mac_id], state.humans[op_id]
    spec = setup.tasks[task.task_type]
    task.machine_health_at_start = twin.health
    task.fatigue_at_start = human.fatigue_hat

    # --- exposure while this task runs (CP3, CP5) -------------------------
    lo, hi = setup.pace_range()
    speed_hat = machine_speed_hat(twin.spec.efficiency_factor, lo, hi)  # CP5
    rula = human.rula(spec.rula_base, speed_hat)           # §4.7
    load = human.cognition(                                # §4.8, CP3
        task_base=spec.cognitive_base,
        machine_health=twin.health,
        defect_risk=twin.defect_risk(
            skill=setup.operators[op_id].skill[task.task_type],
            kappa=spec.severity_kappa,
            fatigue_hat=human.fatigue_hat),
        machines_watched=1,
        machines_total=len(state.machines),
    )
    human.observe(rula, load)
    task.rula_score = rula
    human.begin_task(env.now, spec.energy_demand_kcal_min)     # CP4

    minutes = setup.processing_time(task.task_type, op_id)
    yield env.timeout(minutes)
    human.end_task(env.now)

    task.finished_min = env.now
    op.record(task.task_type, minutes)
    mac.busy_minutes += minutes
    mac.tasks_done += 1
    mac.variable_energy_kwh += (
        setup.machines[mac_id].delta_e_kwh_per_h[task.task_type] * minutes / 60
    )

    # --- quality (design §3.3) — both couplings live ---------------------
    # Evaluated against the conditions the task actually ran under: the machine
    # health and the operator fatigue at the moment work started, hence wear is
    # charged afterwards. CP1 (skill) and CP2 (fatigue) both feed this.
    risk = twin.defect_risk(
        skill=setup.operators[op_id].skill[task.task_type],
        kappa=spec.severity_kappa,
        fatigue_hat=task.fatigue_at_start,                 # CP2
    )
    task.defect_risk = risk
    task.defective = state.rng.random() < risk
    if task.defective:
        state.scrap_units += 1

    # --- wear and effort (design §3.1, §4.1) ------------------------------
    twin.degrade(minutes, spec.severity_kappa)
    state.ideal_minutes += spec.nominal_time_minutes

    op.busy = mac.busy = False
    op.current_task_type = mac.current_task_type = None
    op.current_machine = None
    state.queue.remove(task)
    state.completed.append(task)

    # A machine that has just worn past its floor must not be handed the next
    # task, so this is checked before dispatching rather than waiting for the
    # epoch tick.
    if twin.needs_maintenance():
        _start_maintenance(env, state, mac_id)

    # An operator who finishes mid-epoch must not stand idle until the next
    # epoch boundary: the decision epoch sets how often the plan is recomputed,
    # not how often a free pair may start work. Without this, the mean task
    # length (~15 min) and the epoch length (15 min) interact to waste roughly
    # a third of the available capacity, purely as an artefact of the clock.
    _dispatch(env, state)


def _start_maintenance(env: simpy.Environment, state: ShiftState, mac_id: str,
                       breakdown: bool = False) -> None:
    """Mark the machine out of service NOW, then run the repair as a process.

    The flag must be set synchronously. `env.process` only schedules the
    generator; its first line does not execute until the calling process
    yields, and a dispatch can happen in between.
    """
    twin, mac = state.twins[mac_id], state.machines[mac_id]
    if twin.under_maintenance:
        return
    twin.under_maintenance = mac.under_maintenance = True
    env.process(_maintain(env, state, mac_id, breakdown))


def _maintain(env: simpy.Environment, state: ShiftState, mac_id: str,
              breakdown: bool = False):
    """Hold the machine for the repair time, then return it to nominal."""
    twin, mac = state.twins[mac_id], state.machines[mac_id]
    key = "breakdown_repair_minutes" if breakdown else "maintenance_minutes"
    duration = state.setup.cfg["simulation"][key]

    twin.maintenance_events += 1
    if breakdown:
        twin.breakdown_events += 1

    yield env.timeout(duration)

    twin.maintenance_minutes += duration
    twin.restore()
    mac.under_maintenance = False
    _dispatch(env, state)


def _inject_failures(env: simpy.Environment, state: ShiftState):
    """Scenario S3: knock machines out partway through the shift.

    A machine that is mid-task keeps running until that task finishes; the
    breakdown is picked up the moment it frees up. Interrupting work in flight
    would be harsher, and is left out because nothing in the design calls for
    it — noted in the limitations rather than assumed away.
    """
    n = state.setup.scenario_cfg.get("machine_failures", 0)
    if not n:
        return

    rng = random.Random(state.rng_seed + _FAILURE_SEED_OFFSET)
    shift = state.setup.shift_minutes
    victims = rng.sample(sorted(state.machines), min(n, len(state.machines)))
    times = sorted(rng.uniform(0.25 * shift, 0.75 * shift) for _ in victims)

    previous = 0.0
    for when, mac_id in zip(times, victims):
        yield env.timeout(when - previous)
        previous = when
        state.twins[mac_id].broken = True
        state.twins[mac_id].fail_now()
        if not state.machines[mac_id].busy:
            _start_maintenance(env, state, mac_id, breakdown=True)


def _refresh_rest_state(state: ShiftState, charge_minutes: float = 0.0) -> None:
    """Apply the HC1 hysteresis band (design §8), if the policy enforces it.

    Crossing the limit starts a mandatory rest that runs until fatigue has
    fallen to the lower band. A single threshold would make an operator flip
    between working and resting every epoch either side of it.

    `charge_minutes` is only added on the epoch tick, so calling this before a
    mid-epoch dispatch keeps the rest accounting honest.
    """
    if not state.enforces("HC1"):
        return
    hys = state.setup.cfg["constraints"]["hc1_hysteresis"]
    for human in state.humans.values():
        was = human.resting
        human.resting = update_rest_state(
            human.fatigue_hat, was,
            hys["enter_rest_at"], hys["leave_rest_at"])
        if human.resting:
            human.rest_minutes += charge_minutes
            if not was:
                human.rest_episodes += 1


def _dispatch(env: simpy.Environment, state: ShiftState) -> int:
    """Run the current allocator and start work on whatever it returns.

    Fatigue is brought up to the current instant first. Dispatch happens the
    moment a pair frees up, which is usually mid-epoch, and deciding against
    the fatigue value left over from the last epoch boundary lets work through
    that HC1 should have stopped.
    """
    for human in state.humans.values():
        human.sync(env.now)
    _refresh_rest_state(state)

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

        # --- twin updates (design §9, step 1) ---------------------------
        # Fatigue advances for every operator, whether they worked this epoch
        # or rested. Only the first epoch is skipped, since no time has passed.
        if state.epoch_log:
            for human in state.humans.values():
                human.advance(env.now, setup.epoch_minutes)

        # HC1 hysteresis (design §8). Evaluated after the fatigue update and
        # before the decision, so a mandatory rest takes effect in the same
        # epoch the limit is reached rather than one epoch late.
        _refresh_rest_state(state, charge_minutes=setup.epoch_minutes)

        # Anything that wore past its floor while idle, or was knocked out by
        # the S3 disruption while busy, goes into maintenance now.
        for mac_id, twin in state.twins.items():
            if twin.needs_maintenance() and not state.machines[mac_id].busy:
                _start_maintenance(env, state, mac_id,
                                   breakdown=twin.broken)
            twin.health_trace.append(twin.health)

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
    rng = random.Random(seed)
    env = simpy.Environment()

    state = ShiftState(
        setup=setup,
        machines={m: MachineState(m) for m in setup.machines},
        operators={o: OperatorState(o) for o in setup.operators},
        twins={m: MachineTwin(spec=s, cfg=setup.cfg)
               for m, s in setup.machines.items()},
        humans={o: HumanTwin(spec=s, cfg=setup.cfg)
                for o, s in setup.operators.items()},
        rng=rng,
        rng_seed=seed,
        allocator=allocator,
        on_epoch=on_epoch,
    )
    state.queue = build_task_queue(setup, rng)
    total_demand = len(state.queue)

    env.process(_epoch_loop(env, state))
    env.process(_inject_failures(env, state))
    env.run(until=setup.shift_minutes)

    # Work still in flight when the clock stops was really performed, so its
    # elapsed minutes count towards utilisation and energy even though the unit
    # never came off the line. Only counters are credited — the task stays
    # unfinished, and no output is claimed for it.
    for task in state.queue:
        if task.started_min is None or task.finished_min is not None:
            continue
        elapsed = setup.shift_minutes - task.started_min
        if elapsed <= 0:
            continue
        state.operators[task.assigned_operator].busy_minutes += elapsed
        mac = state.machines[task.assigned_machine]
        mac.busy_minutes += elapsed
        mac.variable_energy_kwh += (
            setup.machines[task.assigned_machine]
            .delta_e_kwh_per_h[task.task_type] * elapsed / 60)

    # The epoch loop advances fatigue for the window that has just closed, so
    # the final epoch of the shift is still outstanding when the clock stops.
    # Without this the last fifteen minutes of every shift are never charged.
    for human in state.humans.values():
        human.end_task(setup.shift_minutes)
        human.advance(setup.shift_minutes, setup.epoch_minutes)

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
    good = units - state.scrap_units
    busy = [o.busy_minutes for o in state.operators.values()]

    maint_min = sum(t.maintenance_minutes for t in state.twins.values())
    maint_events = sum(t.maintenance_events for t in state.twins.values())
    machine_time = len(state.machines) * setup.shift_minutes

    result = {
        "seed": seed,
        "scenario": setup.scenario,
        "demand": total_demand,
        "throughput": units,
        "good_units": good,
        "scrap_units": state.scrap_units,
        "scrap_rate": round(state.scrap_units / units, 4) if units else None,
        "unfinished": total_demand - units,
        "maintenance_events": maint_events,
        "downtime_hrs": round(maint_min / 60, 3),
        "downtime_share": round(maint_min / machine_time, 4),
        "mean_health_end": round(
            sum(t.health for t in state.twins.values()) / len(state.twins), 4),

        # --- human-centric KPIs (design §4) ------------------------------
        "mean_fatigue": round(
            sum(sum(h.fatigue_trace) / len(h.fatigue_trace)
                for h in state.humans.values() if h.fatigue_trace)
            / len(state.humans), 4),
        "max_fatigue": round(
            max(h.peak_fatigue_hat for h in state.humans.values()), 4),
        "hc1_breaches": sum(
            1 for h in state.humans.values()
            for f in h.fatigue_trace
            if f >= setup.cfg["constraints"]["hard"]["HC1_fatigue_max"]),
        "mean_rula": round(
            sum(h.mean_rula for h in state.humans.values())
            / len(state.humans), 4),
        "hc3_breaches": sum(
            1 for h in state.humans.values() for r in h.rula_samples
            if r > setup.cfg["constraints"]["hard"]["HC3_rula_max"]),
        "mean_cognitive_load": round(
            sum(h.mean_cognitive for h in state.humans.values())
            / len(state.humans), 4),
        # OEE, the classic equipment measure, in this model's terms:
        #   availability  uptime after maintenance, over planned machine time
        #   performance   nominal cycle time over the time actually taken, so
        #                 it measures how well work was matched to skill
        #   quality       good units over units started
        # Reported for completeness (experiment-plan §6); the pillars the
        # argument rests on are the human and sustainability columns.
        "availability": round(1 - maint_min / machine_time, 4),
        "performance": round(
            state.ideal_minutes
            / sum(m.busy_minutes for m in state.machines.values()), 4)
        if sum(m.busy_minutes for m in state.machines.values()) else 0.0,
        "quality_rate": round(good / units, 4) if units else 0.0,
        "oee": round(
            (1 - maint_min / machine_time)
            * (state.ideal_minutes
               / max(sum(m.busy_minutes for m in state.machines.values()), 1e-9))
            * (good / units if units else 0.0), 4),

        # Hard-constraint breaches actually observed. HC2 and HC4 cannot appear
        # here: they filter availability, so a breach is impossible by
        # construction rather than by policy.
        "constraint_violations": sum(
            1 for h in state.humans.values() for f in h.fatigue_trace
            if f >= setup.cfg["constraints"]["hard"]["HC1_fatigue_max"]) + sum(
            1 for h in state.humans.values() for r in h.rula_samples
            if r > setup.cfg["constraints"]["hard"]["HC3_rula_max"]),

        "rest_episodes": sum(h.rest_episodes for h in state.humans.values()),
        "rest_minutes": sum(h.rest_minutes for h in state.humans.values()),
        **state.violations.as_dict(),
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
    print(f"  good / scrap          {r['good_units']} / {r['scrap_units']}  "
          f"({r['scrap_rate']:.2%} scrap)")
    print(f"  maintenance           {r['maintenance_events']} events, "
          f"{r['downtime_hrs']} h  ({r['downtime_share']:.1%} of machine time)")
    print(f"  mean health at end    {r['mean_health_end']}")
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
        t = state.twins[m.machine_id]
        print(f"    {m.machine_id}  {m.busy_minutes:6.1f} min  "
              f"({share:5.1%})  {m.tasks_done:3d} tasks  "
              f"{m.variable_energy_kwh:6.2f} kWh   "
              f"health {t.health:4.2f}  {t.maintenance_events} stops")


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
    print("=== the three scenarios ===")
    for sc in setup.cfg["experiment"]["scenarios"]:
        s = load_setup(scenario=sc)
        r = run_shift(s, seed=0)
        print(f"  {sc}: demand {r['demand']:3d}  done {r['throughput']:3d}  "
              f"unfinished {r['unfinished']:3d}  "
              f"op util {r['operator_utilisation']:.0%}  "
              f"downtime {r['downtime_share']:.1%}  "
              f"scrap {r['scrap_rate']:.1%}")
    print()
    print("  S3 currently shows up as downtime, not lost throughput: a normal")
    print("  shift has slack, so breakdowns get absorbed. Its real signal is")
    print("  what each baseline does to the OPERATORS to catch up, which needs")
    print("  the human twin (T5.7). Revisit S3's demand if it stays flat then.")
