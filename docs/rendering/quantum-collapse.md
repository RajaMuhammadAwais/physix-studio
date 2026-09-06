# Quantum Wave-Packet Collapse Scene

`WavePacketCollapseScene` visualizes a two-state superposition as two Gaussian wave packets. During the measurement animation, the left and right components fade while the total probability density collapses onto the right-hand packet. The detector marker and status label update from `SUPERPOSITION` to `MEASURED → COLLAPSED |R⟩`.

Preview locally with:

```bash
physix preview quantum-collapse --quality draft
```

Or save an MP4:

```bash
physix render quantum-collapse --quality draft --output ./media
```

The scene is intentionally educational rather than a full quantum solver. It provides a deterministic visualization contract suitable for later extensions such as phase interference, time-dependent Schrödinger evolution, or a measurement basis selector.
