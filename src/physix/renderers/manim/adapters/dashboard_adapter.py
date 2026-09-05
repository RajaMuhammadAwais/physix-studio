"""Renderer-neutral dashboard and equation values."""
from __future__ import annotations

from dataclasses import dataclass

from physix.core.events import PhysicsEvent
from physix.core.state import PhysicsState


@dataclass(frozen=True, slots=True)
class DashboardValues:
    time: str
    height: str
    velocity: str
    acceleration: str

    @classmethod
    def from_state(cls, state: PhysicsState, precision: int = 2) -> DashboardValues:
        return cls(
            time=f"{state.time:.{precision}f} s",
            height=f"{state.position:.{precision}f} km",
            velocity=f"{state.velocity:.{precision}f} km/s",
            acceleration=f"{state.acceleration:.{precision}f} m/s²",
        )


@dataclass(frozen=True, slots=True)
class EquationValues:
    position_equation: str = "h(t) = h₀ + v₀t + ½at²"
    velocity_equation: str = "v(t) = v₀ + at"
    event_highlight: str | None = None

    def for_state(self, state: PhysicsState, events: list[PhysicsEvent]) -> EquationValues:
        active = next((event for event in events if event.time <= state.time), None)
        return EquationValues(event_highlight="v = 0" if active else None)
