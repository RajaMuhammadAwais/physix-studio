"""Renderer-neutral live graph primitives."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from physix.core.state import PhysicsState


@dataclass(frozen=True, slots=True)
class GraphBounds:
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    width: float = 8.0
    height: float = 4.5


class LiveGraph:
    def __init__(self, bounds: GraphBounds) -> None:
        if bounds.x_max <= bounds.x_min or bounds.y_max <= bounds.y_min:
            raise ValueError("graph bounds must have positive ranges")
        self.bounds = bounds

    def coords_to_point(self, x: float, y: float) -> tuple[float, float]:
        b = self.bounds
        if not b.x_min <= x <= b.x_max or not b.y_min <= y <= b.y_max:
            raise ValueError("point is outside graph bounds")
        return ((x - b.x_min) / (b.x_max - b.x_min) * b.width,
                (y - b.y_min) / (b.y_max - b.y_min) * b.height)

    def progressive_curve(self, states: list[PhysicsState], current_time: float) -> list[tuple[float, float]]:
        return [(s.time, s.position) for s in states if s.time <= current_time]

T = TypeVar("T")

@dataclass
class ObjectGraphCursor(Generic[T]):
    graph: LiveGraph
    visual_object: T
    x_value: Callable[[PhysicsState], float]
    y_value: Callable[[PhysicsState], float]
    position: tuple[float, float] = (0.0, 0.0)

    def update(self, state: PhysicsState) -> tuple[float, float]:
        self.position = self.graph.coords_to_point(self.x_value(state), self.y_value(state))
        return self.position
