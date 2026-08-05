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
    out.append(f"  {DIM}MACHINES{OFF}")
    for m in state.machines.values():
        if m.under_maintenance:
            mark, label = f"{RED}▓▓▓{OFF}", f"{RED}maintenance{OFF}"
        elif m.busy:
            c = TASK_COLOUR[m.current_task_type]
            mark, label = f"{c}███{OFF}", f"{c}task {m.current_task_type}{OFF}"
        else:
            mark, label = f"{GREY}···{OFF}", f"{GREY}idle{OFF}"
        util = m.busy_minutes / now if now else 0
        out.append(f"    {m.machine_id}  {mark}  {label:22s}"
                   f"{GREY}{m.tasks_done:3d} done · {util:4.0%} busy{OFF}")

    out.append("")

    # --- operators -------------------------------------------------------
    out.append(f"  {DIM}OPERATORS{OFF}")
    for o in state.operators.values():
        if o.on_break:
            mark, label = f"{BLUE}▒▒▒{OFF}", f"{BLUE}on break{OFF}"
        elif o.busy:
            c = TASK_COLOUR[o.current_task_type]
            mark = f"{c}███{OFF}"
            label = f"{c}task {o.current_task_type}{OFF} on {o.current_machine}"
        else:
            mark, label = f"{GREY}···{OFF}", f"{GREY}waiting{OFF}"
        share = o.busy_minutes / now if now else 0
        out.append(f"    {o.operator_id}  {mark}  {label:26s}"
                   f"{GREY}{o.tasks_done:3d} done · {share:4.0%} busy{OFF}")

    # --- totals ----------------------------------------------------------
    out.append("")
    out.append(f"  {DIM}QUEUE{OFF}      {_bar(done, demand)}  "
               f"{done}/{demand} done, {e['queue_pending']} waiting")
    out.append(f"  {DIM}ENERGY{OFF}     {kwh:6.1f} kWh    "
               f"{DIM}CO2e{OFF} {kwh * ef:5.1f} kg")
    if state.deferral_epochs:
        out.append(f"  {YELLOW}DEFERRALS  {state.deferral_epochs} "
                   f"epochs blocked by constraints{OFF}")
    out.append("")
    out.append(f"  {GREY}fatigue and machine health are not modelled yet "
               f"(T5.4, T5.7){OFF}")

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
