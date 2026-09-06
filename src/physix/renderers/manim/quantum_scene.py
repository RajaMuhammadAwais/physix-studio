"""Quantum wave-packet superposition and measurement-collapse scene."""
from __future__ import annotations

from math import exp

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
    Axes,
    Create,
    Dot,
    MathTex,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    always_redraw,
)


class WavePacketCollapseScene(Scene):
    """Show two Gaussian amplitudes coherently superposed, then measured."""

    @staticmethod
    def _gaussian(x: float, center: float, width: float = 0.62) -> float:
        return exp(-((x - center) ** 2) / (2 * width**2))

    def construct(self) -> None:
        measurement = ValueTracker(0.0)
        stars = VGroup(*[
            Dot((x / 2, y / 2, 0), radius=0.009, color=WHITE)
            for x, y in ((-13, 7), (-9, 6), (-4, 8), (4, 7), (10, 6), (14, 8), (-15, -5), (13, -4))
        ])
        title = Text("PHYSIX STUDIO", font_size=30, color=WHITE).to_edge(UP)
        subtitle = Text("QUANTUM SUPERPOSITION · WAVE-PACKET COLLAPSE", font_size=15, color=WHITE).next_to(
            title, DOWN, buff=0.08
        )
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 1.35, 0.25],
            x_length=10.0, y_length=4.8, axis_config={"color": WHITE},
        ).shift(DOWN * 0.25)
        x_label = MathTex("x", color=WHITE).next_to(axes.x_axis, RIGHT)
        psi_label = MathTex("|\\psi(x)|^2", color=WHITE).next_to(axes.y_axis, UP)
        equation = MathTex(r"|\psi\rangle=\frac{1}{\sqrt{2}}(|L\rangle+|R\rangle)", color=WHITE).scale(0.7)
        equation.to_corner(UP + LEFT).shift(RIGHT * 0.25 + DOWN * 0.55)
        status = Text("SUPERPOSITION", font_size=20, color=YELLOW).to_corner(UP + RIGHT).shift(LEFT * 0.3 + DOWN * 0.55)

        left_center, right_center = -1.55, 1.55

        def collapse_factor() -> float:
            return measurement.get_value()

        left_curve = always_redraw(lambda: axes.plot(
            lambda x: (1 - collapse_factor()) * 0.5 * self._gaussian(x, left_center),
            x_range=[-4, 4], color=BLUE, stroke_width=4,
        ))
        right_curve = always_redraw(lambda: axes.plot(
            lambda x: (1 - collapse_factor()) * 0.5 * self._gaussian(x, right_center),
            x_range=[-4, 4], color=GREEN, stroke_width=4,
        ))
        total_curve = always_redraw(lambda: axes.plot(
            lambda x: (1 - collapse_factor()) * (
                0.5 * self._gaussian(x, left_center) + 0.5 * self._gaussian(x, right_center)
            ) + collapse_factor() * self._gaussian(x, right_center),
            x_range=[-4, 4], color=ORANGE, stroke_width=6,
        ))
        detector = always_redraw(lambda: Dot(
            axes.c2p(right_center, 0.0), radius=0.12, color=ORANGE if collapse_factor() > 0.5 else YELLOW
        ))

        def update_status(_mob=None) -> None:
            status.become(Text(
                "MEASURED → COLLAPSED |R⟩" if collapse_factor() > 0.5 else "SUPERPOSITION",
                font_size=20, color=ORANGE if collapse_factor() > 0.5 else YELLOW,
            ).to_corner(UP + RIGHT).shift(LEFT * 0.3 + DOWN * 0.55))

        status.add_updater(update_status)
        self.add(
            stars, title, subtitle, equation, axes, x_label, psi_label,
            left_curve, right_curve, total_curve, detector, status,
        )
        self.play(Create(axes), run_time=1)
        self.wait(1)
        self.play(measurement.animate.set_value(1.0), run_time=2)
        self.wait(2)
