"""Immutable, typed state shared by simulation and presentation layers."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class PhysicsState:
    """A snapshot of a simulation at one authoritative time."""

    time: float
    position: float
    velocity: float
    acceleration: float
    force: float | None = None
    energy: float | None = None
    metadata: Mapping[str, float | str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("simulation time cannot be negative")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class VerticalMotionConfig:
    """Configuration for constant-acceleration vertical motion."""

    initial_height: float = 0.0
    initial_velocity: float = 100.0
    acceleration: float = -9.81
    duration: float = 10.0

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("duration must be positive")


class PhysicsStateLike:
    """Protocol-like documentation type for future specialized state models."""

    time: float
