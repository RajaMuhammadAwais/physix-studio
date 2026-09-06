"""Deterministic circular-orbit model used by the orbital mechanics scene."""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, tau


@dataclass(frozen=True, slots=True)
class OrbitalState:
    """Analytical two-body state for a circular orbit in normalized units."""

    time: float
    angle: float
    radius: float
    position: tuple[float, float]
    velocity: tuple[float, float]
    speed: float
    gravitational_acceleration: float


@dataclass(frozen=True, slots=True)
class CircularOrbit:
    """A stable circular orbit with an explicit gravitational parameter."""

    radius: float = 2.35
    gravitational_parameter: float = 5.0
    period: float = 8.0

    @property
    def angular_velocity(self) -> float:
        return tau / self.period

    @property
    def orbital_speed(self) -> float:
        return self.angular_velocity * self.radius

    def state_at(self, time: float) -> OrbitalState:
        angle = self.angular_velocity * time
        position = (self.radius * cos(angle), self.radius * sin(angle))
        velocity = (
            -self.orbital_speed * sin(angle),
            self.orbital_speed * cos(angle),
        )
        acceleration = self.gravitational_parameter / (self.radius**2)
        return OrbitalState(
            time=time,
            angle=angle,
            radius=self.radius,
            position=position,
            velocity=velocity,
            speed=self.orbital_speed,
            gravitational_acceleration=acceleration,
        )


def build_circular_orbit() -> CircularOrbit:
    """Build the flagship normalized circular-orbit example."""

    return CircularOrbit()


if __name__ == "__main__":
    orbit = build_circular_orbit()
    print(orbit.state_at(0.0))
    print(orbit.state_at(orbit.period / 4))
