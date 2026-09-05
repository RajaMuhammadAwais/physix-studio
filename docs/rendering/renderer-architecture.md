# Renderer Architecture

PhysiX Studio has one authoritative timeline and one source of truth: `PhysicsState(t)`. A renderer receives deterministic snapshots and projects them into visual objects. It does not integrate equations, own simulation time, or maintain independent clocks.

The Manim adapter is organized into pure state adapters, procedural object factories, reusable components, and a thin `MoonAscentScene`. `ManimStateAdapter.apply_state()` maps one state to the physical Moon point, graph Moon point, and progressively visible curve. The dashboard and equation adapters consume that same state and the existing physics events.

Manim remains optional. Core users install `physix-studio`; cinematic rendering users install `physix-studio[manim]`. This keeps simulation, tests, and future renderer backends lightweight.
