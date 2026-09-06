"""Deterministic gravitational-lensing model for the relativistic scene."""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, slots=True)
class LensingState:
    source_angle: float
    einstein_radius: float
    primary_image: float
    secondary_image: float
    magnification: float


@dataclass(frozen=True, slots=True)
class PointMassLens:
    """Thin-lens approximation in normalized angular units."""

    einstein_radius: float = 0.95

    def state_at(self, source_angle: float) -> LensingState:
        discriminant = sqrt(source_angle**2 + 4 * self.einstein_radius**2)
        primary = 0.5 * (source_angle + discriminant)
        secondary = 0.5 * (source_angle - discriminant)
        magnification = (
            (source_angle**2 + 2 * self.einstein_radius**2)
            / (abs(source_angle) * discriminant)
            if abs(source_angle) > 1e-9
            else float("inf")
        )
        return LensingState(source_angle, self.einstein_radius, primary, secondary, magnification)


def build_point_mass_lens() -> PointMassLens:
    """Build the normalized lens used by the Manim scene."""

    return PointMassLens()
