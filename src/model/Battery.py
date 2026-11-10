from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Battery:
    """
    BESS Model
    Attributes:
        model_id: Unique model identifier (e.g., 1 to 8).
        name: Commercial or catalog name of the battery model.
        capacity: Nominal energy storage capacity in kWh.
        max_charge: Maximum charging power in kW.
        max_discharge: Maximum discharging power in kW.
        efficiency: Round-trip charging/discharging efficiency (0.0 to 1.0).
        current_charge: Current energy stored in the battery in kWh.
        initial_charge: Starting charge at period 1 in kWh.
        final_charge: Target required charge at period 96 in kWh.
    """

    model_id: int
    name: str
    capacity: float
    max_charge: float
    max_discharge: float
    efficiency: float
    current_charge: float = 0.0
    initial_charge: float = 0.0
    final_charge: float = 0.0

    def __post_init__(self) -> None:
        if self.current_charge == 0.0 and self.initial_charge > 0.0:
            self.current_charge = self.initial_charge

    @property
    def soc(self) -> float:
        if self.capacity <= 0:
            return 0.0
        return self.current_charge / self.capacity

    @property
    def available_capacity(self) -> float:
        """Remaining capacity that can be stored (in kWh)."""
        return max(0.0, self.capacity - self.current_charge)

    @property
    def available_energy(self) -> float:
        """Energy currently available to discharge (in kWh)."""
        return max(0.0, self.current_charge)

    def charge(self, power_kw: float, duration_hours: float = 0.25) -> float:
        """Charge the battery with the given power for a time interval."""
        if power_kw <= 0 or self.available_capacity <= 0:
            return 0.0

        # Cap the charging power to its maximum
        actual_power = min(power_kw, self.max_charge)

        added_energy = actual_power * duration_hours * self.efficiency

        # Cap by available capacity
        if added_energy > self.available_capacity:
            added_energy = self.available_capacity
            actual_power = added_energy / (duration_hours * self.efficiency)

        self.current_charge += added_energy
        return actual_power

    def discharge(self, power_kw: float, duration_hours: float = 0.25) -> float:
        """Discharge the battery with the given power for a time interval."""
        if power_kw <= 0 or self.available_energy <= 0:
            return 0.0

        # Cap the discharging power to the battery specific minimum
        requested_power = min(power_kw, self.max_discharge)

        energy_drawn = (requested_power * duration_hours) / self.efficiency

        # Cap by available energy
        if energy_drawn > self.available_energy:
            energy_drawn = self.available_energy
            actual_power = (energy_drawn * self.efficiency) / duration_hours
        else:
            actual_power = requested_power

        self.current_charge -= energy_drawn
        return actual_power

    def reset(self) -> None:
        """Reset the battery charge back to its initial charge state."""
        self.current_charge = self.initial_charge

    @classmethod
    def from_dict(cls, model_id: int, data: dict[str, Any]) -> Battery:
        """Factory method to instantiate a Battery from a specification dict."""
        cap = float(data.get("capacity_kwh", data.get("capacity", 0.0)))
        init_charge = float(data.get("initial_charge_kwh", data.get("initial_charge", cap / 2.0)))
        final_charge = float(data.get("final_charge_kwh", data.get("final_charge", cap / 2.0)))

        return cls(
            model_id=int(model_id),
            name=str(data.get("name", f"Model {model_id}")),
            capacity=cap,
            max_charge=float(data.get("max_charge_kw", data.get("max_charge", 0.0))),
            max_discharge=float(data.get("max_discharge_kw", data.get("max_discharge", 0.0))),
            efficiency=float(data.get("efficiency", 1.0)),
            current_charge=init_charge,
            initial_charge=init_charge,
            final_charge=final_charge,
        )
