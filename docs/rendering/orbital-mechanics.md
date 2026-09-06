# Orbital Mechanics Scene

`OrbitalMechanicsScene` is a deterministic Manim visualization of a normalized circular two-body orbit. The analytical model in `examples/orbital_mechanics.py` supplies the planet position, tangential velocity, constant orbital speed, and inward gravitational acceleration. Manim is only the projection layer.

The scene includes a central body, orbit path, moving planet, bounded trail, radius vector, velocity vector, the equation `v = sqrt(mu/r)`, and synchronized telemetry for time, radius, speed, and acceleration.

Render it locally with:

```bash
pip install -e ".[manim]"
physix render orbital-mechanics --quality draft --output ./media
```

The verified draft render is a 10-second, 480p15 MP4. A representative frame is included below.

![Orbital mechanics scene](../assets/orbital-mechanics.png)

The model uses normalized units (`AU`, `AU/s`, and `AU/s²`) for educational clarity. It is intentionally circular rather than a full numerical N-body integrator; the next orbital milestone can add eccentricity, multiple bodies, and conserved-energy diagnostics.
