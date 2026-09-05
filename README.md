# PhysiX Studio

**Physics Simulation → Scientific Visualization → Animated Graphs → Cinematic Educational Content**

PhysiX Studio is an open-source Python foundation for deterministic physics simulations whose physical state drives every visual component through one authoritative timeline. Its defining abstraction is an **object graph cursor**: a physical visual object, such as a Moon, can move along a graph at the point `(simulation_time, measured_value)` without drifting from the curve.

## Current MVP

This first implementation provides a typed immutable `PhysicsState`, a deterministic `TimelineController`, analytical and numerical constant-acceleration motion, event detection, replayable state history, coordinate-safe `LiveGraph`, generic `ObjectGraphCursor`, centralized themes, a CLI, and a tested Moon Ascent data pipeline. The physics layer has no visualization dependency. Manim adapters are intentionally deferred until the core contracts are stable.

## Quickstart

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
physix simulate moon-ascent --duration 10 --samples 11
python examples/moon_ascent.py
```

## Cinematic Rendering

The unique rendering feature is that **physical objects can become live graph cursors**. The physical Moon and a smaller graph Moon are both driven by the same `PhysicsState(t)`: one is mapped into physical scene coordinates and the other into `LiveGraph.coords_to_point(time, height)`. The Height vs Time curve is progressively revealed from the same recorded history.

Manim is an optional renderer adapter, never the physics clock:

```bash
pip install -e ".[manim]"
physix render moon-ascent --quality draft --output ./media
```

The supported quality profiles are `draft`, `standard`, `high`, and `production`. Users who only need the simulation core do not install Manim. See [`docs/rendering/`](docs/rendering/) for the rendering architecture and known limitations.

## Architecture

```text
TimelineController → SimulationEngine → PhysicsState(t)
                                      ├→ Physical object adapter
                                      ├→ LiveGraph + ObjectGraphCursor
                                      └→ Dashboard / equation adapters
```

There are no independent object, graph, or dashboard timers. A renderer samples the same state at the same time. See [`docs/architecture.md`](docs/architecture.md) and [`docs/adr/`](docs/adr/).

## Roadmap

The next milestone is a Manim Community Edition adapter for Earth, Moon, stars, trail, dashboard, and progressive graph reveal. Future physics modules include projectile motion, mechanics, waves, electromagnetism, and orbital systems.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Please keep physics independent from presentation, add tests for new models, and document architectural changes as ADRs.
