"""Procedural EarthVisual with no external image assets."""
from __future__ import annotations


def earth_visual(radius: float = 0.55, atmosphere: bool = True):
    try:
        from manim import BLUE_D, BLUE_E, GREEN_E, TEAL_A, Circle, VGroup
    except ImportError as exc:
        raise RuntimeError("Manim is required for EarthVisual; install physix-studio[manim]") from exc
    globe = Circle(radius=radius, color=BLUE_D, fill_color=BLUE_E, fill_opacity=1)
    continents = VGroup(
        Circle(radius=radius * 0.28, color=GREEN_E, fill_color=GREEN_E, fill_opacity=0.9, stroke_width=0),
        Circle(radius=radius * 0.18, color=GREEN_E, fill_color=GREEN_E, fill_opacity=0.9, stroke_width=0),
    ).move_to(globe.get_center() + (-radius * 0.18, radius * 0.12, 0))
    earth = VGroup(globe, continents)
    if atmosphere:
        earth.add(Circle(radius=radius * 1.08, color=TEAL_A, stroke_width=2, fill_opacity=0))
    return earth
