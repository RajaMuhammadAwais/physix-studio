"""Procedural MoonVisual; imports Manim only when the factory is called."""
from __future__ import annotations


def moon_visual(radius: float = 0.28, glow: bool = True):
    try:
        from manim import GREY_B, GREY_D, WHITE, Circle, Dot, VGroup
    except ImportError as exc:
        raise RuntimeError("Manim is required for MoonVisual; install physix-studio[manim]") from exc
    body = Circle(radius=radius, color=GREY_B, fill_color=GREY_B, fill_opacity=1.0, stroke_width=1)
    craters = VGroup(
        Dot(body.get_center() + (-radius * 0.35, radius * 0.2, 0), radius=radius * 0.12, color=GREY_D),
        Dot(body.get_center() + (radius * 0.25, -radius * 0.18, 0), radius=radius * 0.09, color=GREY_D),
        Dot(body.get_center() + (radius * 0.05, radius * 0.35, 0), radius=radius * 0.06, color=WHITE),
    )
    moon = VGroup(body, craters)
    if glow:
        moon.set_stroke(width=2)
    return moon
