"""Renderer contracts shared by optional presentation backends."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RenderQuality:
    name: str
    pixel_width: int
    pixel_height: int
    frame_rate: int


QUALITIES = {
    "draft": RenderQuality("draft", 854, 480, 15),
    "standard": RenderQuality("standard", 1280, 720, 30),
    "high": RenderQuality("high", 1920, 1080, 60),
    "production": RenderQuality("production", 3840, 2160, 60),
}


def get_quality(name: str) -> RenderQuality:
    try:
        return QUALITIES[name]
    except KeyError as exc:
        raise ValueError(f"unknown quality {name!r}; choose from {sorted(QUALITIES)}") from exc


class Renderer(Protocol):
    def render(self, simulation: object, output: Path, quality: RenderQuality) -> Path:
        """Render a simulation to an output artifact."""
