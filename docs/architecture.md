# Technical Architecture

## Core contracts

`PhysicsState` is an immutable snapshot containing time, position, velocity, acceleration, optional conserved quantities, and extensible metadata. `TimelineController` is the sole playback clock. `SimulationEngine` evaluates a pure `PhysicsModel`, records deterministic history, and invokes event detectors. `LiveGraph` maps data coordinates to scene coordinates, while `ObjectGraphCursor` maps state values to that graph without knowing whether the visual object is a Moon, car, or electron.

## Data flow

```text
configuration → physics model → SimulationEngine → PhysicsState(t)
                                                  ├→ event detectors
                                                  ├→ graph curve/cursor
                                                  ├→ physical object adapters
                                                  └→ dashboard/equation adapters
```

The graph cursor is guaranteed to use the same state object as the physical scene. No component performs a second physics calculation.

## MVP milestones

1. **Core:** state, timeline, events, simulation history, tests.
2. **Vertical motion:** analytical model plus numerical reference implementation.
3. **Graph:** bounds, coordinate conversion, progressive curve, cursor.
4. **Synchronization:** Moon Ascent pipeline and synchronization tests.
5. **Visualization:** Manim adapters, cinematic scene, dashboard, equations.
6. **CLI and packaging:** configuration validation, render quality flags, docs, CI.

## Rendering boundary

The current MVP deliberately does not import Manim. This prevents an unavailable or changing renderer API from contaminating the physics contracts. The future adapter will implement `Scene`, `Mobject`, `Axes`, and updater behavior only at the boundary, with all values read from `PhysicsState(t)`.
