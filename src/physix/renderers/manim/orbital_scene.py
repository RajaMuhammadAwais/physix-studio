"""Cinematic circular-orbit scene driven by the analytical orbit model."""
from __future__ import annotations

from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORANGE,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Circle,
    Create,
    Dot,
    MathTex,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    always_redraw,
)

from examples.orbital_mechanics import build_circular_orbit
from physix.renderers.manim.objects.stars import star_field


class OrbitalMechanicsScene(Scene):
    """A synchronized central-body, orbit-track, planet, and telemetry scene."""

    def construct(self) -> None:
        orbit = build_circular_orbit()
        tracker = ValueTracker(0.0)
        stars = star_field(seed=19, count=90)
        title = Text("PHYSIX STUDIO", font_size=30, color=WHITE).to_edge(UP)
        subtitle = Text("ORBITAL MECHANICS", font_size=16, color=WHITE).next_to(title, DOWN, buff=0.08)
        equation = MathTex(r"v=\sqrt{\frac{\mu}{r}}", color=WHITE).scale(0.8)
        equation.to_corner(UP + LEFT).shift(RIGHT * 0.25 + DOWN * 0.5)

        orbit_center = LEFT * 1.1 + UP * 0.15
        orbit_path = Circle(radius=orbit.radius, color=BLUE, stroke_opacity=0.7).move_to(orbit_center)
        central_body = Dot(orbit_center, radius=0.34, color=ORANGE)
        central_label = Text("CENTRAL BODY", font_size=16, color=ORANGE).next_to(central_body, DOWN, buff=0.12)
        planet = Dot(radius=0.18, color=GREEN)
        planet.add_updater(lambda mob: mob.move_to(self._point_at(orbit, tracker.get_value(), orbit_center)))
        trail = always_redraw(
            lambda: self._trail(orbit, tracker.get_value(), orbit_center)
        )
        velocity = always_redraw(
            lambda: self._velocity_arrow(orbit, tracker.get_value(), orbit_center)
        )
        radius_line = always_redraw(
            lambda: self._radius_line(orbit, tracker.get_value(), orbit_center)
        )

        telemetry = VGroup(
            Text("TIME", font_size=17, color=WHITE),
            Text("RADIUS", font_size=17, color=WHITE),
            Text("SPEED", font_size=17, color=WHITE),
            Text("ACCELERATION", font_size=17, color=WHITE),
        )
        telemetry_values = VGroup(*[Text("--", font_size=19, color=YELLOW) for _ in range(4)])
        cards = VGroup(*[
            VGroup(label, value).arrange(DOWN, buff=0.08)
            for label, value in zip(telemetry, telemetry_values)
        ])
        cards.arrange(RIGHT, buff=0.62).to_edge(DOWN)

        def update_telemetry(_mob=None) -> None:
            state = orbit.state_at(tracker.get_value())
            values = (
                f"{state.time:0.2f} s",
                f"{state.radius:0.2f} AU",
                f"{state.speed:0.2f} AU/s",
                f"{state.gravitational_acceleration:0.2f} AU/s²",
            )
            for card, text, value in zip(cards, telemetry_values, values):
                text.become(Text(value, font_size=19, color=YELLOW))
                card.arrange(DOWN, buff=0.08)
            cards.arrange(RIGHT, buff=0.62).to_edge(DOWN)

        cards.add_updater(update_telemetry)
        self.add(stars, title, subtitle, equation, orbit_path, trail, radius_line, velocity,
                 central_body, central_label, planet, cards)
        self.play(Create(orbit_path), run_time=1)
        self.play(tracker.animate.set_value(orbit.period), run_time=orbit.period, rate_func=lambda x: x)
        self.wait(1)

    @staticmethod
    def _point_at(orbit, time: float, center):
        state = orbit.state_at(time)
        return center + RIGHT * state.position[0] + UP * state.position[1]

    @classmethod
    def _trail(cls, orbit, time: float, center):
        from manim import VMobject

        path = VMobject(color=GREEN, stroke_opacity=0.45, stroke_width=3)
        points = [cls._point_at(orbit, i * time / 40, center) for i in range(41)]
        path.set_points_as_corners(points)
        return path

    @classmethod
    def _velocity_arrow(cls, orbit, time: float, center):
        state = orbit.state_at(time)
        start = cls._point_at(orbit, time, center)
        end = start + RIGHT * state.velocity[0] * 0.28 + UP * state.velocity[1] * 0.28
        return Arrow(start, end, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.18)

    @classmethod
    def _radius_line(cls, orbit, time: float, center):
        return Arrow(
            center,
            cls._point_at(orbit, time, center),
            buff=0.05,
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.08,
        )
