"""Manim dashboard and equation panel driven by adapter values."""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, WHITE, YELLOW, MathTex, Text, VGroup

from physix.renderers.manim.adapters.dashboard_adapter import DashboardValues, EquationValues


class ManimDashboard:
    def __init__(self) -> None:
        labels = ("TIME", "HEIGHT", "VELOCITY", "ACCELERATION")
        self.labels = VGroup(*[Text(label, font_size=18, color=WHITE) for label in labels])
        self.values = VGroup(*[Text("--", font_size=20, color=YELLOW) for _ in range(4)])
        cards = [VGroup(label, value).arrange(DOWN, buff=0.08)
                 for label, value in zip(self.labels, self.values)]
        self.group = VGroup(*cards)
        self.group.arrange(RIGHT, buff=0.65)

    def update(self, values: DashboardValues) -> None:
        for text, value in zip(self.values, (values.time, values.height, values.velocity, values.acceleration)):
            text.become(Text(value, font_size=20, color=YELLOW))


class ManimEquationPanel:
    def __init__(self) -> None:
        self.position = MathTex(r"h(t)=h_0+v_0t+\frac{1}{2}at^2", color=WHITE).scale(0.65)
        self.velocity = MathTex(r"v(t)=v_0+at", color=WHITE).scale(0.65)
        self.highlight = Text("", font_size=22, color=YELLOW)
        self.group = VGroup(self.position, self.velocity, self.highlight).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

    def update(self, values: EquationValues) -> None:
        self.highlight.become(Text(values.event_highlight or "", font_size=22, color=YELLOW))
