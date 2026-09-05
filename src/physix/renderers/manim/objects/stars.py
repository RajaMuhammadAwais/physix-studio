"""Deterministic procedural space background components."""
from __future__ import annotations

import random


def star_field(count: int = 80, seed: int = 7, x_range: tuple[float, float] = (-7, 7),
               y_range: tuple[float, float] = (-4, 4)):
    try:
        from manim import WHITE, Dot, VGroup
    except ImportError as exc:
        raise RuntimeError("Manim is required for SpaceBackground; install physix-studio[manim]") from exc
    rng = random.Random(seed)
    return VGroup(*[Dot((rng.uniform(*x_range), rng.uniform(*y_range), 0), radius=0.012, color=WHITE)
                    for _ in range(count)])


def motion_trail(points: list[tuple[float, float, float]], max_length: int = 60):
    try:
        from manim import BLUE_A, VMobject
    except ImportError as exc:
        raise RuntimeError("Manim is required for MotionTrail; install physix-studio[manim]") from exc
    trail = VMobject(color=BLUE_A, stroke_opacity=0.55)
    bounded = points[-max_length:]
    if bounded:
        trail.set_points_as_corners(bounded)
    return trail
