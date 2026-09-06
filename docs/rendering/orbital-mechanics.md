# Orbital Mechanics Scene

`OrbitalMechanicsScene` is a deterministic Manim visualization of a normalized eccentric two-body orbit. The analytical model in `examples/orbital_mechanics.py` solves Kepler's equation and supplies the planet position, tangential velocity, radius, speed, gravitational acceleration, and swept area. Manim is only the projection layer.

The scene includes a central focus, elliptical orbit path, moving planet, bounded trail, radius vector, velocity vector, a live swept-area polygon, the equation `dA/dt = constant`, and synchronized telemetry. The highlighted swept area makes **Kepler's second law** visible: equal time intervals sweep equal areas.

Preview it interactively for a user-facing real-time animation:

```bash
pip install -e ".[manim]"
physix preview orbital-mechanics --quality draft
```

Export a saved video:

```bash
physix render orbital-mechanics --quality high --output ./media
```

The verified high-quality export is 1920×1080 at 60 fps. The repository includes the resulting MP4 at [`docs/assets/orbital-mechanics-1080p60.mp4`](../assets/orbital-mechanics-1080p60.mp4) and a representative frame below.

![Elliptical orbital mechanics scene](../assets/orbital-mechanics.png)

The model uses normalized units (`AU`, `AU/s`, and `AU/s²`) for educational clarity. It is a deterministic Keplerian ellipse rather than a full numerical N-body integrator; future work can add multiple bodies, perturbations, and conserved-energy diagnostics.
