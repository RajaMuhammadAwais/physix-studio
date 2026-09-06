import importlib.util
from pathlib import Path

import pytest

from physix.core.events import maximum_height_event
from physix.core.state import PhysicsState, VerticalMotionConfig
from physix.graphs.live_graph import GraphBounds, LiveGraph
from physix.physics.kinematics.vertical_motion import VerticalMotion
from physix.renderers.base import get_quality
from physix.renderers.manim import ManimRenderer, ManimUnavailableError
from physix.renderers.manim.adapters.dashboard_adapter import DashboardValues, EquationValues
from physix.renderers.manim.adapters.state_adapter import ManimStateAdapter, PhysicsCoordinateSystem


def test_physics_coordinate_mapping_and_graph_mapping():
    model = VerticalMotion(VerticalMotionConfig(duration=4, initial_velocity=4, acceleration=-1))
    state = model.state_at(2)
    graph = LiveGraph(GraphBounds(0, 4, 0, 8, width=4, height=4))
    adapter = ManimStateAdapter(graph, PhysicsCoordinateSystem(0, 8, -2, 2))
    visual = adapter.apply_state(state, [model.state_at(0), state])
    assert visual.graph_moon_point[:2] == graph.coords_to_point(state.time, state.position)
    assert visual.physical_moon_point[1] == 1


def test_dashboard_and_event_equation_use_same_state():
    state = PhysicsState(time=2, position=4, velocity=0, acceleration=-1)
    values = DashboardValues.from_state(state)
    assert values.time == "2.00 s"
    event = maximum_height_event(
        PhysicsState(time=1, position=3.5, velocity=0.5, acceleration=-1), state
    )
    assert EquationValues().for_state(state, [event]).event_highlight == "v = 0"


def test_quality_validation_and_unavailable_renderer(tmp_path: Path):
    assert get_quality("draft").frame_rate == 15
    with pytest.raises(ValueError):
        get_quality("unknown")
    if importlib.util.find_spec("manim") is None:
        with pytest.raises(ManimUnavailableError):
            ManimRenderer().render(None, tmp_path, get_quality("draft"))
