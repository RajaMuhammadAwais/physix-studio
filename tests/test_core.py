from math import isclose

from examples.moon_ascent import build_moon_ascent
from physix.core.events import maximum_height_event
from physix.core.state import VerticalMotionConfig
from physix.core.timeline import TimelineController
from physix.physics.kinematics.vertical_motion import VerticalMotion
from physix.simulation.engine import SimulationEngine


def test_analytical_vertical_motion():
    model = VerticalMotion(VerticalMotionConfig(initial_velocity=10, acceleration=-2, duration=5))
    state = model.state_at(3)
    assert isclose(state.position, 21)
    assert isclose(state.velocity, 4)


def test_timeline_is_authoritative_and_clamped():
    timeline = TimelineController(10)
    timeline.play()
    timeline.advance(3)
    assert timeline.current_time == 3
    timeline.set_speed(2)
    timeline.advance(4)
    assert timeline.current_time == 10
    assert not timeline.playing


def test_maximum_height_event():
    model = VerticalMotion(VerticalMotionConfig(initial_velocity=10, acceleration=-2, duration=10))
    engine = SimulationEngine(model, 10, (maximum_height_event,))
    engine.run([0, 4, 6, 10])
    assert [event.name for event in engine.events] == ["maximum_height"]


def test_cursor_is_exactly_on_same_state_curve():
    engine, graph, cursor = build_moon_ascent()
    state = engine.history.states[40]
    point = cursor.update(state)
    assert point == graph.coords_to_point(state.time, state.position)
    assert graph.progressive_curve(engine.history.states, state.time)[-1] == (state.time, state.position)
