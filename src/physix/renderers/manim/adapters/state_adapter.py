"""Pure state-to-scene mapping; deliberately does not import Manim."""
from __future__ import annotations

from dataclasses import dataclass

from physix.core.state import PhysicsState
from physix.graphs.live_graph import LiveGraph


@dataclass(frozen=True, slots=True)
class PhysicsCoordinateSystem:
    """Maps a physical scalar range to a scene-space vertical range."""

    physics_min: float
    physics_max: float
    scene_min: float
    scene_max: float

    def __post_init__(self) -> None:
        if self.physics_max <= self.physics_min or self.scene_max <= self.scene_min:
            raise ValueError("coordinate ranges must be increasing")

    def map_height(self, height: float) -> float:
        ratio = (height - self.physics_min) / (self.physics_max - self.physics_min)
        return self.scene_min + ratio * (self.scene_max - self.scene_min)


@dataclass(frozen=True, slots=True)
class VisualState:
    time: float
    physical_moon_point: tuple[float, float, float]
    graph_moon_point: tuple[float, float, float]
    visible_curve: tuple[tuple[float, float], ...]


class ManimStateAdapter:
    """Converts one PhysicsState into all synchronized visual coordinates."""

    def __init__(self, graph: LiveGraph, physical_coordinates: PhysicsCoordinateSystem,
                 physical_x: float = -3.0, graph_z: float = 0.0) -> None:
        self.graph = graph
        self.physical_coordinates = physical_coordinates
        self.physical_x = physical_x
        self.graph_z = graph_z

    def apply_state(self, state: PhysicsState, history: list[PhysicsState]) -> VisualState:
        graph_xy = self.graph.coords_to_point(state.time, state.position)
        return VisualState(
            time=state.time,
            physical_moon_point=(self.physical_x, self.physical_coordinates.map_height(state.position), 0.0),
            graph_moon_point=(graph_xy[0], graph_xy[1], self.graph_z),
            visible_curve=tuple(self.graph.progressive_curve(history, state.time)),
        )
