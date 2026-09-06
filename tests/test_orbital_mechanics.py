from math import isclose

from examples.orbital_mechanics import build_circular_orbit


def test_circular_orbit_period_returns_to_initial_position():
    orbit = build_circular_orbit()
    initial = orbit.state_at(0)
    final = orbit.state_at(orbit.period)
    assert isclose(final.position[0], initial.position[0], abs_tol=1e-9)
    assert isclose(final.position[1], initial.position[1], abs_tol=1e-9)
    assert isclose(final.speed, initial.speed, abs_tol=1e-9)


def test_circular_orbit_speed_and_acceleration_are_constant():
    orbit = build_circular_orbit()
    states = [orbit.state_at(time) for time in (0, 1, 2, 4, 7)]
    assert all(isclose(state.speed, orbit.orbital_speed) for state in states)
    assert all(
        isclose(state.gravitational_acceleration, orbit.gravitational_parameter / orbit.radius**2)
        for state in states
    )
