"""Centralized visual design tokens; optional Manim adapters can consume these."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Theme:
    name: str
    background: str
    foreground: str
    accent: str
    panel: str
    grid: str


THEMES = {
    "cinematic": Theme("cinematic", "#07111f", "#e6f1ff", "#7dd3fc", "#0d2036", "#24415b"),
    "scientific": Theme("scientific", "#101820", "#f0f4f8", "#57c7ff", "#1b2b3a", "#38546b"),
    "dark_lab": Theme("dark_lab", "#050505", "#f5f5f5", "#fbbf24", "#171717", "#404040"),
    "minimal": Theme("minimal", "#ffffff", "#111827", "#2563eb", "#f3f4f6", "#d1d5db"),
    "presentation": Theme("presentation", "#0b1020", "#ffffff", "#a78bfa", "#151b35", "#374151"),
}


def get_theme(name: str = "cinematic") -> Theme:
    try:
        return THEMES[name]
    except KeyError as exc:
        raise ValueError(f"unknown theme {name!r}; choose from {sorted(THEMES)}") from exc
