"""Deterministic two-body orbital models used by the Manim scenes."""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, hypot, pi, sin, sqrt, tau


@dataclass(frozen=True, slots=True)
class OrbitalState:
    """Analytical orbital state in normalized astronomical units."""

    time: float
    angle: float
    radius: float
    position: tuple[float, float]
    velocity: tuple[float, float]
    speed: float
    gravitational_acceleration: float
    swept_area: float


@dataclass(frozen=True, slots=True)
class EllipticalOrbit:
    """Keplerian two-body orbit solved from Kepler's equation."""

    semi_major_axis: float = 2.45
    eccentricity: float = 0.55
    gravitational_parameter: float = 5.0
    period: float = 10.0

    @property
    def angular_velocity(self) -> float:
        return tau / self.period

    @property
    def radius(self) -> float:
        """Compatibility alias for the circular model's old radius field."""

        return self.semi_major_axis

    @property
    def mean_motion(self) -> float:
        return self.angular_velocity

    @property
    def areal_velocity(self) -> float:
        return 0.5 * sqrt(
            self.gravitational_parameter
            * self.semi_major_axis
            * (1 - self.eccentricity**2)
        )

    @property
    def focal_distance(self) -> float:
        return self.semi_major_axis * self.eccentricity

    @property
    def orbital_speed(self) -> float:
        return self.state_at(0).speed

    def _eccentric_anomaly(self, time: float) -> float:
        mean_anomaly = self.mean_motion * time
        eccentric_anomaly = mean_anomaly
        for _ in range(12):
            eccentric_anomaly -= (
                eccentric_anomaly
                - self.eccentricity * sin(eccentric_anomaly)
                - mean_anomaly
            ) / (1 - self.eccentricity * cos(eccentric_anomaly))
        return eccentric_anomaly

    def state_at(self, time: float) -> OrbitalState:
        eccentric_anomaly = self._eccentric_anomaly(time)
        a = self.semi_major_axis
        e = self.eccentricity
        beta = sqrt(1 - e**2)
        x = a * (cos(eccentric_anomaly) - e)
        y = a * beta * sin(eccentric_anomaly)
        denominator = 1 - e * cos(eccentric_anomaly)
        velocity_scale = self.mean_motion * a / denominator
        velocity = (-velocity_scale * sin(eccentric_anomaly), velocity_scale * beta * cos(eccentric_anomaly))
        position = (x, y)
        radius = hypot(x, y)
        speed = hypot(*velocity)
        acceleration = self.gravitational_parameter / radius**2
        true_anomaly = 2 * pi * ((time / self.period) % 1)
        swept_area = self.areal_velocity * time
        return OrbitalState(
            time=time,
            angle=true_anomaly,
            radius=radius,
            position=position,
            velocity=velocity,
            speed=speed,
            gravitational_acceleration=acceleration,
            swept_area=swept_area,
        )


@dataclass(frozen=True, slots=True)
class CircularOrbit(EllipticalOrbit):
    """Backward-compatible circular orbit specialization."""

    semi_major_axis: float = 2.35
    eccentricity: float = 0.0
    period: float = 8.0


def build_elliptical_orbit() -> EllipticalOrbit:
    """Build the flagship eccentric orbit used by the Kepler scene."""

    return EllipticalOrbit()


def build_circular_orbit() -> CircularOrbit:
    """Build the original circular-orbit example."""

    return CircularOrbit()


if __name__ == "__main__":
    orbit = build_elliptical_orbit()
    print(orbit.state_at(0.0))
    print(orbit.state_at(orbit.period / 4))
