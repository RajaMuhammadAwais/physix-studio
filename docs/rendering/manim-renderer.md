# Manim Renderer

Install the optional renderer with:

```bash
pip install -e ".[manim]"
```

Render the flagship scene with:

```bash
physix render moon-ascent --quality draft --output ./media
```

Quality affects Manim output resolution and frame-rate configuration only. It never changes physics calculations. The scene samples `VerticalMotion` through the existing `SimulationEngine`, maps the current Manim `ValueTracker` value to `PhysicsState(t)`, and updates the physical Moon, graph curve, graph Moon, dashboard, equations, and event emphasis from that state.

The graph Moon is a procedural Moon object, not a dot or generic cursor. Its center is assigned from the existing `LiveGraph.coords_to_point(state.time, state.position)`, so it remains exactly on the visible curve. The curve is progressively revealed by filtering the existing recorded state history by the same simulation time.

If Manim is unavailable, the CLI returns an actionable installation message rather than pretending a render succeeded.
