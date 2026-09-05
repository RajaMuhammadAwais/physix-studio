"""Deterministic Moon Ascent data pipeline used by renderers and tutorials."""
from __future__ import annotations

from physix.core.events import maximum_height_event
from physix.core.state import VerticalMotionConfig
from physix.graphs.live_graph import GraphBounds, LiveGraph, ObjectGraphCursor
from physix.physics.kinematics.vertical_motion import VerticalMotion
from physix.simulation.engine import SimulationEngine


def build_moon_ascent(duration: float = 10.0, sample_count: int = 101):
    model = VerticalMotion(VerticalMotionConfig(initial_velocity=100.0, duration=duration))
    times = [duration * i / (sample_count - 1) for i in range(sample_count)]
    engine = SimulationEngine(model, duration, (maximum_height_event,))
    states = engine.run(times)
    graph = LiveGraph(GraphBounds(0, duration, 0, max(s.position for s in states) * 1.1))
    cursor = ObjectGraphCursor(graph, visual_object="moon", x_value=lambda s: s.time, y_value=lambda s: s.position)
    return engine, graph, cursor


if __name__ == "__main__":
    engine, graph, cursor = build_moon_ascent()
    point = cursor.update(engine.history.states[-1])
    print(f"Moon graph cursor at {point}; events={[e.name for e in engine.events]}")
