"""PhysiX Studio: synchronized physics and scientific visualization primitives."""
from .core.state import PhysicsState, VerticalMotionConfig
from .core.timeline import TimelineController

__all__ = ["PhysicsState", "VerticalMotionConfig", "TimelineController"]
__version__ = "0.1.0"
