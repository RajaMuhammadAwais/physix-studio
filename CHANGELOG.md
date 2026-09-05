# Changelog

## 0.1.0 — Phase 2 renderer adapter

Added the optional Manim renderer architecture, renderer-neutral physics-to-scene coordinate mapping, procedural Earth/Moon/star/trail factories, progressive graph visualization, synchronized dashboard and equation adapters, render-quality profiles, `physix render moon-ascent`, renderer integration tests, and rendering documentation.

A real video render was not verified in the current environment because Manim installation requires the native `pangocairo >= 1.30.0` dependency, which is unavailable. The CLI detects this situation and reports the optional installation command rather than claiming success.
