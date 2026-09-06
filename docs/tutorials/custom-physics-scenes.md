# Creating Custom Physics Scenes with the Physix CLI

**Author:** Manus AI

## Overview

PhysiX Studio separates a physics model from its visual projection. A model produces deterministic state at a requested time. A renderer consumes that state and turns it into animated geometry, text, graphs, and diagnostic overlays. This separation is the central design rule for custom scenes because it keeps equations testable, rendering optional, and animation timing reproducible.

This tutorial explains how to create a custom physics scene, register it with the `physix` command-line interface, preview it interactively, export it to MP4, add tests, and document the result. The examples use the repository's existing Manim adapter, but the model design does not depend on Manim.

## 1. Install the project

Create an editable environment from the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Install the optional renderer when the scene uses Manim:

```bash
pip install -e ".[manim]"
```

A working local Manim installation also requires native Cairo and Pango libraries, FFmpeg, a C compiler for packages such as `pycairo`, and a LaTeX installation for `MathTex`. On Ubuntu, the following packages cover the normal local workflow:

```bash
sudo apt-get install -y build-essential libcairo2-dev libpango1.0-dev ffmpeg \
  python3-dev texlive-latex-base texlive-latex-extra \
  texlive-fonts-recommended dvisvgm
```

The core simulation and unit tests do not require Manim. The renderer is optional by design.

## 2. Choose a state contract

Begin with a state object that contains every quantity a renderer may need. State should be immutable, typed, and expressed in explicit units or normalized units. A useful state contract contains time, primary physical variables, derived quantities, and event or diagnostic values.

For example, a gravitational-lensing state can be represented as follows:

```python
@dataclass(frozen=True, slots=True)
class LensingState:
    source_angle: float
    einstein_radius: float
    primary_image: float
    secondary_image: float
    magnification: float
```

The state should describe what is physically true at one instant. It should not contain Manim objects, colors, positions in camera coordinates, or updater callbacks. Those concerns belong to the renderer layer.

| State field | Meaning | Renderer use |
|---|---|---|
| `source_angle` | Angular source offset, in normalized radians | Source marker and telemetry |
| `einstein_radius` | Characteristic lensing angular scale | Ring and equation annotation |
| `primary_image` | Positive image solution | Image marker and ray path |
| `secondary_image` | Negative image solution | Second image marker and ray path |
| `magnification` | Relative brightness factor | Dashboard and explanatory label |

## 3. Implement the analytical model

Place a reusable model in `examples/` or in a dedicated physics package. The model should expose a deterministic `state_at(time_or_parameter)` method. If a closed-form solution is available, prefer it because it makes replay and testing straightforward. If numerical integration is required, isolate the integrator and make its step size explicit.

The lens equation used by the included gravitational-lensing scene is:

```text
θ± = 1/2 (β ± √(β² + 4θE²))
```

Here, `β` is the source angle and `θE` is the Einstein radius. The model computes two apparent image positions. The renderer then maps those normalized values into scene coordinates.

For orbital scenes, the equivalent separation is between the orbital model and the Manim scene. The orbital model solves Kepler's equation and returns position, velocity, radius, and swept area. The scene knows only how to display those values.

A model should satisfy the following properties:

1. The same input produces the same output.
2. The output remains valid outside a renderer process.
3. Units and normalization are documented.
4. Derived quantities are computed from the same primary state.
5. Boundary conditions are explicit.

## 4. Write model tests before animation work

Tests should validate physical relationships rather than pixels. For the lens equation, the two image solutions satisfy:

```text
θ+ θ− = −θE²
```

A focused test looks like this:

```python
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
```

Run the fast checks from the repository root:

```bash
pytest -q
ruff check .
```

The test suite should pass before the scene is registered with the CLI. This keeps failures attributable to the model rather than to Manim installation or scene composition.

## 5. Build the Manim projection layer

Create a scene module under `src/physix/renderers/manim/`. The scene should construct visual objects once and update them from a single timeline value. `ValueTracker` is suitable for a scalar animation parameter. A simulation with several coordinates can use one tracker and derive all values from it.

The essential pattern is:

```python
tracker = ValueTracker(0.0)

physical_object = Dot()
physical_object.add_updater(
    lambda mob: mob.move_to(point_from_state(model.state_at(tracker.get_value())))
)

telemetry.add_updater(
    lambda mob: update_text_from_state(model.state_at(tracker.get_value()))
)
```

All objects must read the same state. Do not create one updater for the object, another timer for the graph, and a third timer for the dashboard. Independent clocks create visible drift and make a scene difficult to reproduce.

Use `always_redraw` for geometry whose shape changes continuously, such as a lensing ray, swept-area polygon, motion trail, or probability-density curve. Keep the calculation inside a small helper method so that the scene's `construct()` method remains readable.

## 6. Keep coordinate mapping explicit

Physics coordinates and scene coordinates are different spaces. A scene may place a focus at `(-1, 0.1, 0)` even though the physical model uses `(0, 0)` as its origin. Write a dedicated mapping function:

```python
def point_at(model, time: float, center):
    state = model.state_at(time)
    return center + RIGHT * state.position[0] + UP * state.position[1]
```

For a graph, use one mapping contract such as `coords_to_point(time, value)`. For a 2D orbit, keep the physical origin and visual center separate. Explicit mapping prevents accidental coupling between model units and camera layout.

## 7. Register the scene with the renderer

The renderer maps a stable public scene name to a Python file and Manim class. In `src/physix/renderers/manim/renderer.py`, add one entry to the `SCENES` dictionary:

```python
SCENES = {
    "gravitational-lensing": (
        "src/physix/renderers/manim/lensing_scene.py",
        "GravitationalLensingScene",
    ),
}
```

The renderer uses the same mapping for saved exports and interactive previews. This prevents a scene from being available in one workflow but missing from the other.

Quality profiles are passed to Manim through both resolution flags and explicit frame rate. The project currently defines these profiles:

| Profile | Resolution | Frame rate | Intended use |
|---|---:|---:|---|
| `draft` | 854×480 | 15 fps | Rapid development |
| `standard` | 1280×720 | 30 fps | Review renders |
| `high` | 1920×1080 | 60 fps | Demonstration exports |
| `production` | 3840×2160 | 60 fps | Final mastering |

## 8. Add CLI commands

Add the public scene name to both `render` and `preview` choices in `src/physix/cli/main.py`. Then the user can run:

```bash
physix render gravitational-lensing --quality draft --output ./media
physix preview gravitational-lensing --quality draft
```

The `render` command saves an MP4 and prints its path. The `preview` command asks Manim to render and open the result in the local video player. The preview workflow is intended for users who want to run the project and immediately see the animation in real time.

A saved high-quality export uses the same public name:

```bash
physix render gravitational-lensing --quality high --output ./media
```

Inspect an export with FFprobe:

```bash
ffprobe -v error \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  ./media/videos/lensing_scene/1080p60/GravitationalLensingScene.mp4
```

## 9. Add documentation and screenshots

Every scene should have a short guide under `docs/rendering/`. Explain the model, the visual encoding, the units, the preview command, and the export command. Add at least one representative frame under `docs/assets/` and link it from both the scene guide and the README.

A useful scene guide answers these questions:

- What physical model is being shown?
- Which quantities are authoritative?
- Which visual objects depend on each quantity?
- What is normalized or simplified?
- What command previews the scene?
- What command exports the scene?
- What limitations remain?

Do not describe a scene as a full physical solver if it is an educational analytical model. State the approximation directly.

## 10. Verify the complete workflow

The minimum acceptance sequence is:

```bash
pytest -q
ruff check .
physix list
physix render gravitational-lensing --quality draft --output /tmp/physix-lensing
physix preview gravitational-lensing --quality draft
```

The preview command opens a player and may remain active until the player is closed. For automated checks, use the render command and inspect the resulting MP4 with FFprobe. Extract a representative frame with FFmpeg when visual inspection is needed:

```bash
ffmpeg -y -loglevel error \
  -i /tmp/physix-lensing/videos/lensing_scene/480p15/GravitationalLensingScene.mp4 \
  -vf 'select=eq(n\,30)' -frames:v 1 /tmp/lensing-frame.png
```

Visual review should check that labels do not overlap, values update, motion is smooth, objects remain within the frame, and the scene communicates the intended physical relationship. Unit tests alone cannot detect a misplaced label or an updater that resets a group position.

## 11. Common failure modes

| Failure | Cause | Correction |
|---|---|---|
| `ManimUnavailableError` | Optional dependency is missing | Install `.[manim]` and native rendering dependencies |
| `FileNotFoundError: latex` | LaTeX is missing for `MathTex` | Install a LaTeX distribution |
| Empty or overlapping telemetry | Text replacement resets object position | Re-arrange and re-anchor the parent group after updates |
| Render succeeds at the wrong frame rate | Quality profile is not passed to Manim | Pass `--fps` explicitly from `RenderQuality.frame_rate` |
| Scene works with `render` but not `preview` | Scene was registered in only one path | Use one shared scene registry |
| Physics and visual object drift apart | Multiple independent timers | Derive every object from one tracker and one state function |
| Tests fail after Manim installation | Test assumes the optional dependency is absent | Branch availability tests on `importlib.util.find_spec("manim")` |

## 12. Recommended extension path

A custom scene is complete when its model is independently testable, its scene is driven by one authoritative state, its CLI name is registered for both preview and export, its documentation explains the approximation, and a real local render has been inspected. After that baseline is stable, add richer physics incrementally.

For orbital mechanics, the next extensions could include perturbations, multiple bodies, conserved energy, or numerical integration. For gravitational lensing, the next extensions could include a moving observer, extended sources, an Einstein ring transition, and brightness conservation diagnostics. Each extension should begin with a state contract and a model test before adding new visual objects.

## References

[1]: https://docs.manim.community/en/stable/ "Manim Community Documentation"

[2]: https://docs.python.org/3/library/dataclasses.html "Python dataclasses documentation"

[3]: https://ffmpeg.org/ffprobe.html "FFprobe documentation"
