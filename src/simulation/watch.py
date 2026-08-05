"""
Live view of the shift clock — watch the simulation walk, epoch by epoch.

    python src/simulation/watch.py                 S1, seed 0, 0.35 s per epoch
    python src/simulation/watch.py S2              the high-demand shift
    python src/simulation/watch.py S2 3 0.1        scenario, seed, speed

The simulation itself finishes in milliseconds. This attaches an observer to
the epoch hook and pauses between epochs so a human can follow what the clock
is doing. It changes nothing about the run: the same seed produces the same
result whether it is watched or not.

Nothing here belongs to the model. It reads state and draws it.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loader import load_setup                              # noqa: E402
from simulation.factory import ShiftState, run_shift       # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.system("")          # enables ANSI escape handling on the Windows console

CLEAR = "\033[2J\033[H"
DIM, BOLD, OFF = "\033[2m", "\033[1m", "\033[0m"
GREEN, YELLOW, RED, BLUE, GREY = (
    "\033[32m", "\033[33m", "\033[31m", "\033[36m", "\033[90m")

# Task types coloured by how hard they are on the operator.
TASK_COLOUR = {"L": GREEN, "M": YELLOW, "H": RED}

SHIFT_START_HOUR = 8


def _clock(minutes: float) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{SHIFT_START_HOUR + h:02d}:{m:02d}"


def _bar(done: int, total: int, width: int = 34) -> str:
    filled = round(width * done / total) if total else 0
    return "█" * filled + "·" * (width - filled)


def draw(state: ShiftState) -> None:
    setup = state.setup
    e = state.epoch_log[-1]
    now = e["clock_min"]
    total_epochs = setup.epochs_per_shift

    demand = len(state.queue) + len(state.completed)
    done = len(state.completed)

    # energy so far: every machine draws idle power the whole time it is on
    idle = sum(setup.machines[m].e_idle_kwh_per_h for m in state.machines) * now / 60
    var = sum(m.variable_energy_kwh for m in state.machines.values())
    kwh = idle + var
    ef = setup.cfg["sustainability"]["emission_factor_kg_co2_per_kwh"]

    out = [CLEAR]
    out.append(f"{BOLD}  Industry 5.0 — shift clock{OFF}"
               f"{GREY}    scenario {setup.scenario} · seed {state.rng_seed}"
               f" · allocator: random (B1){OFF}")
    out.append("")
    out.append(f"  {BOLD}{_clock(now)}{OFF}   epoch {e['epoch'] + 1:2d}/{total_epochs}"
               f"   {_bar(e['epoch'] + 1, total_epochs)}"
               + (f"   {BLUE}{BOLD}BREAK{OFF}" if e["on_break"] else ""))
    out.append("")

    # --- machines --------------------------------------------------------
    h_min = setup.cfg["machines"]["health_min_operational"]
    out.append(f"  {DIM}MACHINES{OFF}"
               f"{GREY}                                    health "
               f"(floor {h_min:.2f} = maintenance){OFF}")
    for m in state.machines.values():
        twin = state.twins[m.machine_id]
        if m.under_maintenance:
            kind = "repair" if twin.broken else "tool change"
            mark, label = f"{RED}▓▓▓{OFF}", f"{RED}{kind}{OFF}"
        elif m.busy:
            c = TASK_COLOUR[m.current_task_type]
            mark, label = f"{c}███{OFF}", f"{c}task {m.current_task_type}{OFF}"
        else:
            mark, label = f"{GREY}···{OFF}", f"{GREY}idle{OFF}"

        hc = GREEN if twin.health > 0.6 else YELLOW if twin.health > h_min else RED
        out.append(f"    {m.machine_id}  {mark}  {label:22s}"
                   f"{hc}{_bar(round(twin.health * 100), 100, 14)}"
                   f" {twin.health:4.2f}{OFF}  "
                   f"{GREY}{m.tasks_done:3d} done{OFF}")

    out.append("")

    # --- operators -------------------------------------------------------
    hc1 = setup.cfg["constraints"]["hard"]["HC1_fatigue_max"]
    out.append(f"  {DIM}OPERATORS{OFF}"
               f"{GREY}                                   fatigue "
               f"(HC1 = {hc1:.2f} of personal AWL){OFF}")
    for o in state.operators.values():
        human = state.humans[o.operator_id]
        f = human.fatigue_hat

        if o.on_break:
            mark, label = f"{BLUE}▒▒▒{OFF}", f"{BLUE}on break{OFF}"
        elif o.busy:
            c = TASK_COLOUR[o.current_task_type]
            mark = f"{c}███{OFF}"
            label = f"{c}task {o.current_task_type}{OFF} on {o.current_machine}"
        else:
            mark, label = f"{GREY}···{OFF}", f"{GREY}waiting{OFF}"

        fc = RED if f >= hc1 else YELLOW if f >= 0.6 else GREEN
        flag = f" {RED}OVER HC1{OFF}" if f >= hc1 else ""
        out.append(f"    {o.operator_id}  {mark}  {label:26s}"
                   f"{fc}{_bar(round(f * 100), 100, 14)} {f:4.2f}{OFF}"
                   f"{GREY}  AWL {human.spec.awl_kcal_min:4.2f}{OFF}{flag}")

    # --- totals ----------------------------------------------------------
    out.append("")
    out.append(f"  {DIM}QUEUE{OFF}      {_bar(done, demand)}  "
               f"{done}/{demand} done, {e['queue_pending']} waiting")
    scrap = state.scrap_units
    out.append(f"  {DIM}ENERGY{OFF}     {kwh:6.1f} kWh    "
               f"{DIM}CO2e{OFF} {kwh * ef:5.1f} kg    "
               f"{DIM}SCRAP{OFF} {scrap} "
               f"({scrap / done:.0%})" if done else "")
    down = sum(t.maintenance_events for t in state.twins.values())
    if down:
        out.append(f"  {DIM}DOWNTIME{OFF}   {down} maintenance events")
    if state.deferral_epochs:
        out.append(f"  {YELLOW}DEFERRALS  {state.deferral_epochs} "
                   f"epochs blocked by constraints{OFF}")
    out.append("")
    breaches = sum(1 for h in state.humans.values() if h.fatigue_hat >= hc1)
    if breaches:
        out.append(f"  {RED}{breaches} operator(s) past HC1 and still working — "
                   f"nothing stops them until the decision layer exists "
                   f"(T5.11){OFF}")
    else:
        out.append(f"  {GREY}fatigue is modelled but not yet acted on "
                   f"(T5.11 adds the constraints){OFF}")

    print("\n".join(out), flush=True)


# =============================================================================
def main() -> None:
    scenario = sys.argv[1] if len(sys.argv) > 1 else "S1"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35

    setup = load_setup(scenario=scenario)

    def observer(state: ShiftState) -> None:
        draw(state)
        time.sleep(delay)

    result = run_shift(setup, seed=seed, on_epoch=observer)

    print(f"  {BOLD}shift over{OFF}   "
          f"{result['throughput']}/{result['demand']} tasks · "
          f"{result['energy_kwh']} kWh · {result['co2e_kg']} kg CO2e · "
          f"Gini {result['workload_gini']}")
    if result["unfinished"]:
        print(f"  {YELLOW}{result['unfinished']} tasks did not fit in the "
              f"shift{OFF}")
    print()


if __name__ == "__main__":
    main()
