"""Optional Manim process runner; physics remains in the core process model."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

from physix.renderers.base import RenderQuality


class ManimUnavailableError(RuntimeError):
    pass


SCENES = {
    "moon-ascent": ("src/physix/renderers/manim/scene.py", "MoonAscentScene"),
    "orbital-mechanics": (
        "src/physix/renderers/manim/orbital_scene.py", "OrbitalMechanicsScene"
    ),
    "quantum-collapse": (
        "src/physix/renderers/manim/quantum_scene.py", "WavePacketCollapseScene"
    ),
    "gravitational-lensing": (
        "src/physix/renderers/manim/lensing_scene.py", "GravitationalLensingScene"
    ),
}


class ManimRenderer:
    QUALITY_FLAGS = {"draft": "l", "standard": "m", "high": "h", "production": "p"}

    @staticmethod
    def _require_manim() -> None:
        if importlib.util.find_spec("manim") is None:
            raise ManimUnavailableError(
                "Manim is not installed. Install it with: pip install 'physix-studio[manim]'"
            )

    @staticmethod
    def _scene(scene_name: str) -> tuple[str, str]:
        try:
            return SCENES[scene_name]
        except KeyError as exc:
            raise ValueError(f"Unknown Manim scene: {scene_name}") from exc

    def render(self, simulation: object, output: Path, quality: RenderQuality,
               scene_name: str = "moon-ascent") -> Path:
        del simulation
        self._require_manim()
        output.mkdir(parents=True, exist_ok=True)
        scene_file, scene_class = self._scene(scene_name)
        command = [
            "python", "-m", "manim", f"-q{self.QUALITY_FLAGS[quality.name]}",
            "--fps", str(quality.frame_rate), "--media_dir", str(output), scene_file, scene_class,
        ]
        subprocess.run(command, check=True)
        videos = sorted(output.rglob(f"{scene_class}.mp4"))
        if not videos:
            raise RuntimeError(f"Manim completed but no {scene_class}.mp4 found in {output}")
        return videos[-1]

    def preview(self, quality: RenderQuality, scene_name: str = "moon-ascent") -> None:
        """Render a scene and open it in Manim's local video player."""

        self._require_manim()
        scene_file, scene_class = self._scene(scene_name)
        command = [
            "python", "-m", "manim", "-p", f"-q{self.QUALITY_FLAGS[quality.name]}",
            "--fps", str(quality.frame_rate), scene_file, scene_class,
        ]
        subprocess.run(command, check=True)
