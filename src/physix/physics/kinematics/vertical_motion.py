"""Constant-acceleration vertical motion, independent from visualization."""
from __future__ import annotations

from collections.abc import Iterable

from physix.core.state import PhysicsState, VerticalMotionConfig


class VerticalMotion:
    def __init__(self, config: VerticalMotionConfig) -> None:
        self.config = config

    def state_at(self, time: float) -> PhysicsState:
        if not 0 <= time <= self.config.duration:
            raise ValueError("time must be within the configured duration")
        c = self.config
        height = c.initial_height + c.initial_velocity * time + 0.5 * c.acceleration * time**2
        velocity = c.initial_velocity + c.acceleration * time
        return PhysicsState(
            time=time,
            position=height,
            velocity=velocity,
            acceleration=c.acceleration,
            metadata={"model": "constant_acceleration", "quantity": "height"},
        )

    def sample(self, times: Iterable[float]) -> list[PhysicsState]:
        return [self.state_at(time) for time in times]

    def numerical_state_at(self, time: float, step: float = 0.001) -> PhysicsState:
        """Forward-Euler reference implementation for future numerical models."""
        if step <= 0:
            raise ValueError("step must be positive")
        c = self.config
        steps = int(time / step)
        remainder = time - steps * step
        height = c.initial_height
        velocity = c.initial_velocity
        for _ in range(steps):
            height += velocity * step
            velocity += c.acceleration * step
        height += velocity * remainder
        velocity += c.acceleration * remainder
        return PhysicsState(time=time, position=height, velocity=velocity, acceleration=c.acceleration)
