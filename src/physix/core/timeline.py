"""Deterministic master timeline independent of wall-clock rendering."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimelineController:
    """Controls simulation time; renderers consume, but never own, this clock."""

    duration: float
    current_time: float = 0.0
    speed: float = 1.0
    playing: bool = False

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("duration must be positive")
        self.seek(self.current_time)
        self.set_speed(self.speed)

    def play(self) -> None:
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def resume(self) -> None:
        self.play()

    def stop(self) -> None:
        self.playing = False
        self.seek(0.0)

    def seek(self, time: float) -> None:
        if not 0.0 <= time <= self.duration:
            raise ValueError(f"time must be between 0 and {self.duration}")
        self.current_time = float(time)

    def set_speed(self, multiplier: float) -> None:
        if multiplier <= 0:
            raise ValueError("speed multiplier must be positive")
        self.speed = float(multiplier)

    def advance(self, frame_seconds: float) -> float:
        if frame_seconds < 0:
            raise ValueError("frame_seconds cannot be negative")
        if self.playing:
            self.current_time = min(self.duration, self.current_time + frame_seconds * self.speed)
            if self.current_time >= self.duration:
                self.playing = False
        return self.current_time
