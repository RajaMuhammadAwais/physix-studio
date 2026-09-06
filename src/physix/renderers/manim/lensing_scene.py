"""Relativistic gravitational-lensing visualization in the thin-lens approximation."""
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
    Arc,
    ArcBetweenPoints,
    Create,
    Dot,
    MathTex,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    always_redraw,
)

from examples.gravitational_lensing import build_point_mass_lens
from physix.renderers.manim.objects.stars import star_field


class GravitationalLensingScene(Scene):
    """Show a massive lens bending rays into two apparent source images."""

    def construct(self) -> None:
        lens = build_point_mass_lens()
        source_tracker = ValueTracker(0.55)
        stars = star_field(seed=31, count=90)
        title = Text("PHYSIX STUDIO", font_size=30, color=WHITE).to_edge(UP)
        subtitle = Text("GENERAL RELATIVITY · GRAVITATIONAL LENSING", font_size=15, color=WHITE).next_to(
            title, DOWN, buff=0.08
        )
        equation = MathTex(r"\theta_{\pm}=\frac{1}{2}(\beta\pm\sqrt{\beta^2+4\theta_E^2})", color=WHITE).scale(0.58)
        equation.to_corner(UP + LEFT).shift(RIGHT * 0.22 + DOWN * 0.5)
        caption = Text("LIGHT FOLLOWS CURVED SPACETIME", font_size=16, color=YELLOW)
        caption.to_corner(UP + RIGHT).shift(LEFT * 0.2 + DOWN * 0.55)

        center = LEFT * 1.0 + DOWN * 0.1
        lens_body = Dot(center, radius=0.4, color=ORANGE)
        lens_label = Text("MASSIVE LENS", font_size=15, color=ORANGE).next_to(lens_body, DOWN, buff=0.12)
        einstein_ring = always_redraw(
            lambda: Arc(radius=1.15, angle=6.28, color=YELLOW, stroke_opacity=0.35).move_to(center)
        )
        source = always_redraw(lambda: Dot(
            center + RIGHT * 4.1 + UP * source_tracker.get_value() * 0.55,
            radius=0.16,
            color=BLUE,
        ))
        source_label = Text("DISTANT SOURCE", font_size=15, color=BLUE).next_to(source, UP, buff=0.12)
        primary = always_redraw(lambda: self._image_dot(lens, source_tracker.get_value(), center, True))
        secondary = always_redraw(lambda: self._image_dot(lens, source_tracker.get_value(), center, False))
        rays = always_redraw(lambda: self._rays(lens, source_tracker.get_value(), center))
        telemetry = VGroup(
            Text("SOURCE ANGLE", font_size=16, color=WHITE),
            Text("EINSTEIN RADIUS", font_size=16, color=WHITE),
            Text("MAGNIFICATION", font_size=16, color=WHITE),
        )
        values = VGroup(*[Text("--", font_size=18, color=YELLOW) for _ in range(3)])
        cards = VGroup(*[
            VGroup(label, value).arrange(DOWN, buff=0.08)
            for label, value in zip(telemetry, values)
        ])
        cards.arrange(RIGHT, buff=0.65).to_edge(DOWN)

        def update_cards(_mob=None) -> None:
            state = lens.state_at(source_tracker.get_value())
            text_values = (
                f"{state.source_angle:0.2f} rad",
                f"{state.einstein_radius:0.2f} rad",
                f"{state.magnification:0.2f}×",
            )
            for card, value_mob, text in zip(cards, values, text_values):
                value_mob.become(Text(text, font_size=18, color=YELLOW))
                card.arrange(DOWN, buff=0.08)
            cards.arrange(RIGHT, buff=0.65).to_edge(DOWN)

        cards.add_updater(update_cards)
        self.add(stars, title, subtitle, equation, caption, einstein_ring, rays, lens_body, lens_label,
                 source, source_label, primary, secondary, cards)
        self.play(Create(lens_body), run_time=1)
        self.play(source_tracker.animate.set_value(-0.55), run_time=5, rate_func=lambda x: x)
        self.play(source_tracker.animate.set_value(0.55), run_time=5, rate_func=lambda x: x)
        self.wait(1)

    @staticmethod
    def _image_dot(lens, source_angle: float, center, primary: bool):
        state = lens.state_at(source_angle)
        image_angle = state.primary_image if primary else state.secondary_image
        return Dot(center + RIGHT * 1.55 + UP * image_angle * 0.85, radius=0.14,
                   color=GREEN if primary else BLUE)

    @classmethod
    def _rays(cls, lens, source_angle: float, center):
        state = lens.state_at(source_angle)
        source_point = center + RIGHT * 4.1 + UP * source_angle * 0.55
        primary_point = center + RIGHT * 1.55 + UP * state.primary_image * 0.85
        secondary_point = center + RIGHT * 1.55 + UP * state.secondary_image * 0.85
        ray_one = ArcBetweenPoints(source_point, primary_point, angle=0.7, color=GREEN, stroke_opacity=0.8)
        ray_two = ArcBetweenPoints(source_point, secondary_point, angle=-0.7, color=BLUE, stroke_opacity=0.8)
        return VGroup(ray_one, ray_two)
