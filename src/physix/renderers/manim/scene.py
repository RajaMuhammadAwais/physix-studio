"""Flagship cinematic scene; Manim is only a projection layer."""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, WHITE, Create, Scene, Text, ValueTracker

from examples.moon_ascent import build_moon_ascent
from physix.renderers.manim.adapters.dashboard_adapter import DashboardValues, EquationValues
from physix.renderers.manim.adapters.state_adapter import ManimStateAdapter, PhysicsCoordinateSystem
from physix.renderers.manim.components.dashboard import ManimDashboard, ManimEquationPanel
from physix.renderers.manim.components.live_graph import ManimLiveGraph
from physix.renderers.manim.objects.earth import earth_visual
from physix.renderers.manim.objects.moon import moon_visual
from physix.renderers.manim.objects.stars import star_field


class MoonAscentScene(Scene):
    """Two synchronized Moons, a progressive graph, and a live dashboard."""

    def construct(self) -> None:
        engine, graph, _ = build_moon_ascent()
        history = engine.history.states
        max_height = max(s.position for s in history) * 1.1
        coordinates = PhysicsCoordinateSystem(0, max_height, -2.6, 2.8)
        adapter = ManimStateAdapter(graph, coordinates, -3.2)
        tracker = ValueTracker(0.0)
        stars = star_field()
        title = Text("PHYSIX STUDIO", font_size=30, color=WHITE).to_edge(UP)
        subtitle = Text("MOON ASCENT SIMULATION", font_size=16, color=WHITE).next_to(title, DOWN, buff=0.08)
        earth = earth_visual().move_to((-3.2, -2.6, 0))
        physical_moon = moon_visual(radius=0.25).move_to((-3.2, -2.0, 0))
        graph_view = ManimLiveGraph(graph, origin=(2.5, 0.1, 0))
        dashboard = ManimDashboard()
        dashboard.group.to_edge(DOWN)
        equations = ManimEquationPanel()
        equations.group.to_corner(UP + LEFT).shift(RIGHT * 0.25 + DOWN * 0.5)

        def current_state():
            return engine.state_at(min(tracker.get_value(), engine.duration))

        def update_visuals(_mob=None):
            visual = adapter.apply_state(current_state(), history)
            physical_moon.move_to(visual.physical_moon_point)
            graph_view.apply(current_state(), history)
            dashboard.update(DashboardValues.from_state(current_state()))
            equations.update(EquationValues().for_state(current_state(), engine.events))
            return physical_moon

        physical_moon.add_updater(update_visuals)
        self.add(stars, title, subtitle, earth, graph_view.mobjects(), physical_moon, dashboard.group, equations.group)
        self.play(Create(earth), run_time=1)
        self.play(tracker.animate.set_value(engine.duration), run_time=engine.duration, rate_func=lambda x: x)
        self.wait(1)
