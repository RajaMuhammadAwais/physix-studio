"""Physics event primitives and deterministic event detection."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

from .state import PhysicsState


@dataclass(frozen=True, slots=True)
class PhysicsEvent:
    name: str
    time: float
    state: PhysicsState
    metadata: dict[str, float | str] = field(default_factory=dict)


EventDetector = Callable[[PhysicsState, PhysicsState], PhysicsEvent | None]


def maximum_height_event(previous: PhysicsState, current: PhysicsState) -> PhysicsEvent | None:
    """Detect the first velocity sign change from positive to non-positive."""
    if previous.velocity > 0 >= current.velocity:
        return PhysicsEvent("maximum_height", current.time, current, {"height": current.position})
    return None


def detect_events(states: Iterable[PhysicsState], detectors: Iterable[EventDetector]) -> list[PhysicsEvent]:
    snapshots = list(states)
    events: list[PhysicsEvent] = []
    for previous, current in zip(snapshots, snapshots[1:]):
        for detector in detectors:
            event = detector(previous, current)
            if event is not None:
                events.append(event)
    return events
