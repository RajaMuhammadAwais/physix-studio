"""Manim graph components backed by PhysiX LiveGraph data."""
from __future__ import annotations

from manim import BLUE_A, WHITE, Axes, Create, VGroup, VMobject

from physix.core.state import PhysicsState
from physix.graphs.live_graph import LiveGraph
from physix.renderers.manim.objects.moon import moon_visual


class ManimLiveGraph:
    def __init__(self, graph: LiveGraph, origin: tuple[float, float, float] = (0, 0, 0)) -> None:
        self.graph = graph
        b = graph.bounds
        self.axes = Axes(x_range=[b.x_min, b.x_max, max(1, (b.x_max - b.x_min) / 5)],
                         y_range=[b.y_min, b.y_max, max(1, (b.y_max - b.y_min) / 5)],
                         x_length=b.width, y_length=b.height,
                         axis_config={"color": WHITE, "stroke_width": 1.5}).move_to(origin)
        self.curve = VMobject(color=BLUE_A, stroke_width=3)
        self.cursor = moon_visual(radius=0.12, glow=True)
        self.labels = VGroup(self.axes.get_x_axis_label("Time"), self.axes.get_y_axis_label("Height"))

    def mobjects(self) -> VGroup:
        return VGroup(self.axes, self.labels, self.curve, self.cursor)

    def apply(self, state: PhysicsState, history: list[PhysicsState]) -> None:
        points = [self.axes.c2p(x, y) for x, y in self.graph.progressive_curve(history, state.time)]
        if points:
            self.curve.set_points_as_corners(points)
        self.cursor.move_to(self.axes.c2p(state.time, state.position))

    def reveal_animation(self):
        return Create(self.curve)
