# ADR-001: Separate simulation core from renderer

**Status:** Accepted

**Decision:** Keep physics, state, events, and graph coordinate mapping independent of Manim.

**Rationale:** Rendering frameworks change and are expensive to import in tests. A pure core enables deterministic replay, multiple renderers, and mathematical validation.
