from math import isclose

from examples.gravitational_lensing import build_point_mass_lens


def test_lens_equation_produces_images_on_opposite_sides():
    lens = build_point_mass_lens()
    state = lens.state_at(0.5)
    assert state.primary_image > 0
    assert state.secondary_image < 0
    assert isclose(
        state.primary_image * state.secondary_image,
        -lens.einstein_radius**2,
        rel_tol=1e-9,
    )


def test_alignment_increases_magnification():
    lens = build_point_mass_lens()
    aligned = lens.state_at(0.01)
    offset = lens.state_at(0.8)
    assert aligned.magnification > offset.magnification
