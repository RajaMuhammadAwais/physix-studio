# Changelog

## 0.1.0 — Phase 2 renderer adapter

Added the optional Manim renderer architecture, renderer-neutral physics-to-scene coordinate mapping, procedural Earth/Moon/star/trail factories, progressive graph visualization, synchronized dashboard and equation adapters, render-quality profiles, `physix render moon-ascent`, renderer integration tests, and rendering documentation.

A real draft video render was verified locally after installing the optional Manim, Cairo/Pango, compiler, FFmpeg, and LaTeX dependencies. The resulting 12-second 480p15 `MoonAscentScene.mp4` was inspected for layout and synchronization; dashboard and equation anchoring were corrected before the final render.

## 0.2.0 — Orbital and quantum scenes

Extended orbital mechanics from circular motion to a deterministic eccentric Keplerian ellipse with a live swept-area visualization for Kepler's second law. Added `physix preview` for local user-facing playback, added the quantum wave-packet superposition and collapse scene, and verified a 12-second 1920×1080 60 fps orbital MP4 export.

## 0.3.0 — Relativistic lensing and scene authoring tutorial

Added a normalized gravitational-lensing scene with Einstein-radius geometry, image splitting, bent light paths, and magnification telemetry. Added a comprehensive tutorial for creating custom physics models and Manim scenes with the Physix CLI, including testing, preview, export, screenshots, and troubleshooting.
