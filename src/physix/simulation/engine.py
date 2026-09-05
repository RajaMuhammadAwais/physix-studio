"""Simulation orchestration and replayable state history."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from physix.core.events import EventDetector, PhysicsEvent, detect_events
from physix.core.state import PhysicsState


class PhysicsModel(Protocol):
    def state_at(self, time: float) -> PhysicsState: ...


@dataclass
class StateHistory:
    states: list[PhysicsState] = field(default_factory=list)

    def append(self, state: PhysicsState) -> None:
        if self.states and state.time < self.states[-1].time:
            raise ValueError("state history must be chronological")
        self.states.append(state)

    def at(self, time: float) -> PhysicsState:
        for state in self.states:
            if state.time == time:
                return state
        raise KeyError(f"no state recorded at time {time}")


@dataclass
class SimulationEngine:
    model: PhysicsModel
    duration: float
    detectors: tuple[EventDetector, ...] = ()
    history: StateHistory = field(default_factory=StateHistory)
    events: list[PhysicsEvent] = field(default_factory=list)

    def state_at(self, time: float) -> PhysicsState:
        return self.model.state_at(time)

    def run(self, times: list[float]) -> list[PhysicsState]:
        self.history = StateHistory()
        for time in times:
            if not 0 <= time <= self.duration:
                raise ValueError("sample time is outside simulation duration")
            self.history.append(self.state_at(time))
        self.events = detect_events(self.history.states, self.detectors)
        return list(self.history.states)

    def replay(self) -> list[PhysicsState]:
        return list(self.history.states)
