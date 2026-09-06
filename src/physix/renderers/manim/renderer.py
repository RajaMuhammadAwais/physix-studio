"""Optional Manim process runner; physics remains in the core process model."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

from physix.renderers.base import RenderQuality


class ManimUnavailableError(RuntimeError):
    pass


class ManimRenderer:
    QUALITY_FLAGS = {"draft": "l", "standard": "m", "high": "h", "production": "p"}

    def render(self, simulation: object, output: Path, quality: RenderQuality,
               scene_name: str = "moon-ascent") -> Path:
        del simulation  # The scene constructs the deterministic example pipeline itself.
        if importlib.util.find_spec("manim") is None:
            raise ManimUnavailableError(
                "Manim is not installed. Install it with: pip install 'physix-studio[manim]'"
            )
        output.mkdir(parents=True, exist_ok=True)
        scenes = {
            "moon-ascent": ("src/physix/renderers/manim/scene.py", "MoonAscentScene"),
            "orbital-mechanics": (
                "src/physix/renderers/manim/orbital_scene.py", "OrbitalMechanicsScene"
            ),
        }
        try:
            scene_file, scene_class = scenes[scene_name]
        except KeyError as exc:
            raise ValueError(f"Unknown Manim scene: {scene_name}") from exc
        command = ["python", "-m", "manim", f"-q{self.QUALITY_FLAGS[quality.name]}",
                   "--media_dir", str(output), scene_file, scene_class]
        subprocess.run(command, check=True)
        videos = sorted(output.rglob(f"{scene_class}.mp4"))
        if not videos:
            raise RuntimeError(f"Manim completed but no {scene_class}.mp4 found in {output}")
        return videos[-1]
