"""
T5.10 — the Planet pillar (design §3.2, §3.3).

Energy, emissions and waste were already being counted in scattered places.
This gathers them into one accounting so the objective function and the results
table draw on the same numbers.

Two decisions worth stating, because both change what the KPI means:

Energy per unit is charged against GOOD units, not units started. Scrap
consumed electricity and produced nothing, so counting it as output would make
a shift look more efficient the more it wasted. Both figures are returned so
the difference stays visible.

Idle draw is included in the total but excluded from the marginal cost of an
assignment. A powered machine draws its idle load whether or not it is given
work, so that part cannot be attributed to a decision — only delta_e can.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SustainabilityReport:
    energy_kwh: float
    idle_kwh: float
    variable_kwh: float
    co2e_kg: float
    units_started: int
    good_units: int
    scrap_units: int

    @property
    def scrap_rate(self) -> float:
        return self.scrap_units / self.units_started if self.units_started else 0.0

    @property
    def energy_per_unit(self) -> float | None:
        """Against good units — waste is not output."""
        return self.energy_kwh / self.good_units if self.good_units else None

    @property
    def energy_per_started_unit(self) -> float | None:
        return (self.energy_kwh / self.units_started
                if self.units_started else None)

    @property
    def co2e_per_unit(self) -> float | None:
        return self.co2e_kg / self.good_units if self.good_units else None

    def as_dict(self) -> dict:
        return {
            "energy_kwh": round(self.energy_kwh, 3),
            "idle_kwh": round(self.idle_kwh, 3),
            "variable_kwh": round(self.variable_kwh, 3),
            "co2e_kg": round(self.co2e_kg, 3),
            "energy_per_unit": (round(self.energy_per_unit, 4)
                                if self.energy_per_unit else None),
            "energy_per_started_unit": (round(self.energy_per_started_unit, 4)
                                        if self.energy_per_started_unit else None),
            "co2e_per_unit": (round(self.co2e_per_unit, 4)
                              if self.co2e_per_unit else None),
            "good_units": self.good_units,
            "scrap_units": self.scrap_units,
            "scrap_rate": round(self.scrap_rate, 4),
        }


def account(machine_specs: dict, machine_states: dict, shift_minutes: float,
            emission_factor: float, units_started: int,
            scrap_units: int) -> SustainabilityReport:
    """Design §3.2:  E = e_idle + 1[busy] * delta_e(tau),  CO2e = kWh * EF."""
    hours = shift_minutes / 60
    idle = sum(s.e_idle_kwh_per_h for s in machine_specs.values()) * hours
    variable = sum(m.variable_energy_kwh for m in machine_states.values())
    total = idle + variable

    return SustainabilityReport(
        energy_kwh=total,
        idle_kwh=idle,
        variable_kwh=variable,
        co2e_kg=total * emission_factor,
        units_started=units_started,
        good_units=units_started - scrap_units,
        scrap_units=scrap_units,
    )


def marginal_energy_kwh(delta_e_kwh_per_h: float, minutes: float) -> float:
    """What one assignment actually adds to consumption.

    Only the variable term: the idle draw is paid whether the machine is given
    this task or not, so attributing it to the decision would penalise every
    option equally and change nothing except the scale.
    """
    return delta_e_kwh_per_h * minutes / 60
