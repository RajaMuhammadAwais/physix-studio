# Research Report

## Scope

The initial research compared official documentation and established practices across Manim Community Edition, NumPy/SciPy, SymPy, Matplotlib, VPython, and PyVista. The selection criterion was relevance to a deterministic simulation whose state can drive both cinematic objects and live graphs.

## Findings

| Approach | Strength | Limitation for PhysiX Studio | Decision |
|---|---|---|---|
| Manim Community Edition | Scene graph, updaters, axes, camera, and high-quality offline rendering | Rendering concerns can leak into domain logic if used as the simulation engine | Use as the presentation adapter, not the physics source of truth |
| NumPy/SciPy | Efficient arrays and mature numerical methods | Array-first APIs are not sufficient as a domain model for typed event-rich snapshots | Optional numerical backend behind model protocols |
| SymPy | Exact symbolic expressions and differentiation | Symbolic expressions should not be required at runtime for every frame | Use for validation and equation generation where valuable |
| Matplotlib | Familiar axes and animation primitives | Less suitable for cinematic scene composition and object reuse | Useful export/debug backend, not flagship renderer |
| VPython | Fast interactive 3D educational prototyping | Different rendering/runtime model from offline cinematic production | Reference for educational ergonomics, not core dependency |
| PyVista | Strong 3D scientific mesh and volume visualization | Overkill for the 2D/2.5D Moon Ascent MVP | Future specialized backend for 3D scientific scenes |

## Architectural conclusion

A small, dependency-free core is the safest first step: typed states, an explicit timeline, pure physics models, deterministic history, event detectors, and renderer-neutral graph mapping. Manim should consume these contracts through adapters. This makes unit tests fast and permits future Matplotlib, web, or PyVista backends without duplicating physics.

## Sources

The research was cross-checked against the official project documentation for [Manim](https://docs.manim.community/), [NumPy](https://numpy.org/doc/), [SciPy](https://docs.scipy.org/doc/scipy/), [SymPy](https://docs.sympy.org/latest/), [Matplotlib](https://matplotlib.org/stable/), [VPython](https://www.vpython.org/), and [PyVista](https://docs.pyvista.org/). Exact API details should be verified against the installed version when the rendering adapter is added.
