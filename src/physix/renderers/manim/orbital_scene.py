"""Cinematic elliptical-orbit scene with Kepler's second-law visualization."""
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
    Create,
    Dot,
    Ellipse,
    MathTex,
    Polygon,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    always_redraw,
)

from examples.orbital_mechanics import build_elliptical_orbit
from physix.renderers.manim.objects.stars import star_field


class OrbitalMechanicsScene(Scene):
    """An eccentric orbit, equal-area sweep, velocity vector, and telemetry."""

    def construct(self) -> None:
        orbit = build_elliptical_orbit()
        tracker = ValueTracker(0.0)
        stars = star_field(seed=19, count=90)
        title = Text("PHYSIX STUDIO", font_size=30, color=WHITE).to_edge(UP)
        subtitle = Text("ELLIPTICAL ORBITS · KEPLER II", font_size=16, color=WHITE).next_to(
            title, DOWN, buff=0.08
        )
        equation = MathTex(r"\frac{dA}{dt}=\frac{1}{2}r^2\dot{\theta}=\mathrm{constant}", color=WHITE).scale(0.62)
        equation.to_corner(UP + LEFT).shift(RIGHT * 0.25 + DOWN * 0.5)
        area_label = Text("EQUAL AREAS IN EQUAL TIMES", font_size=15, color=YELLOW)
        area_label.to_corner(UP + RIGHT).shift(LEFT * 0.25 + DOWN * 0.65)

        focus = LEFT * 1.15 + UP * 0.1
        ellipse_center = focus + RIGHT * orbit.focal_distance
        orbit_path = Ellipse(
            width=2 * orbit.semi_major_axis,
            height=2 * orbit.semi_major_axis * (1 - orbit.eccentricity**2) ** 0.5,
            color=BLUE,
            stroke_opacity=0.75,
        ).move_to(ellipse_center)
        central_body = Dot(focus, radius=0.34, color=ORANGE)
        central_label = Text("FOCUS", font_size=16, color=ORANGE).next_to(central_body, DOWN, buff=0.12)
        planet = Dot(radius=0.18, color=GREEN)
        planet.add_updater(lambda mob: mob.move_to(self._point_at(orbit, tracker.get_value(), focus)))
        trail = always_redraw(lambda: self._trail(orbit, tracker.get_value(), focus))
        velocity = always_redraw(lambda: self._velocity_arrow(orbit, tracker.get_value(), focus))
        radius_line = always_redraw(lambda: self._radius_line(orbit, tracker.get_value(), focus))
        swept_area = always_redraw(lambda: self._swept_area(orbit, tracker.get_value(), focus))

        telemetry = VGroup(
            Text("TIME", font_size=17, color=WHITE),
            Text("RADIUS", font_size=17, color=WHITE),
            Text("SPEED", font_size=17, color=WHITE),
            Text("SWEPT AREA", font_size=17, color=WHITE),
        )
        telemetry_values = VGroup(*[Text("--", font_size=19, color=YELLOW) for _ in range(4)])
        cards = VGroup(*[
            VGroup(label, value).arrange(DOWN, buff=0.08)
            for label, value in zip(telemetry, telemetry_values)
        ])
        cards.arrange(RIGHT, buff=0.56).to_edge(DOWN)

        def update_telemetry(_mob=None) -> None:
            state = orbit.state_at(tracker.get_value())
            values = (
                f"{state.time:0.2f} s",
                f"{state.radius:0.2f} AU",
                f"{state.speed:0.2f} AU/s",
                f"{state.swept_area:0.2f} AU²",
            )
            for card, text, value in zip(cards, telemetry_values, values):
                text.become(Text(value, font_size=19, color=YELLOW))
                card.arrange(DOWN, buff=0.08)
            cards.arrange(RIGHT, buff=0.56).to_edge(DOWN)

        cards.add_updater(update_telemetry)
        self.add(
            stars, title, subtitle, equation, area_label, orbit_path, swept_area,
            trail, radius_line, velocity, central_body, central_label, planet, cards,
        )
        self.play(Create(orbit_path), run_time=1)
        self.play(tracker.animate.set_value(orbit.period), run_time=orbit.period, rate_func=lambda x: x)
        self.wait(1)

    @staticmethod
    def _point_at(orbit, time: float, focus):
        state = orbit.state_at(time)
        return focus + RIGHT * state.position[0] + UP * state.position[1]

    @classmethod
    def _trail(cls, orbit, time: float, focus):
        from manim import VMobject

        path = VMobject(color=GREEN, stroke_opacity=0.45, stroke_width=3)
        points = [cls._point_at(orbit, i * time / 45, focus) for i in range(46)]
        path.set_points_as_corners(points)
        return path

    @classmethod
    def _swept_area(cls, orbit, time: float, focus):
        points = [focus]
        points.extend(cls._point_at(orbit, i * time / 30, focus) for i in range(31))
        return Polygon(*points, color=YELLOW, fill_color=YELLOW, fill_opacity=0.18, stroke_opacity=0.35)

    @classmethod
    def _velocity_arrow(cls, orbit, time: float, focus):
        state = orbit.state_at(time)
        start = cls._point_at(orbit, time, focus)
        end = start + RIGHT * state.velocity[0] * 0.22 + UP * state.velocity[1] * 0.22
        return Arrow(start, end, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.18)

    @classmethod
    def _radius_line(cls, orbit, time: float, focus):
        return Arrow(
            focus,
            cls._point_at(orbit, time, focus),
            buff=0.05,
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.08,
        )
