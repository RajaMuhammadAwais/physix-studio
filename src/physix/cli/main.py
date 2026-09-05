"""Command-line entry point for deterministic MVP workflows."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from physix.core.events import maximum_height_event
from physix.core.state import VerticalMotionConfig
from physix.physics.kinematics.vertical_motion import VerticalMotion
from physix.renderers.base import get_quality
from physix.simulation.engine import SimulationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="physix", description="PhysiX Studio scientific simulation tools")
    sub = parser.add_subparsers(dest="command", required=True)
    simulate = sub.add_parser("simulate", help="run a built-in simulation")
    simulate.add_argument("name", choices=["moon-ascent", "vertical-motion"])
    simulate.add_argument("--duration", type=float, default=10.0)
    simulate.add_argument("--samples", type=int, default=11)
    sub.add_parser("version", help="show version")
    sub.add_parser("list", help="list templates")
    render = sub.add_parser("render", help="render a cinematic scene with optional Manim")
    render.add_argument("name", choices=["moon-ascent"])
    render.add_argument("--quality", choices=["draft", "standard", "high", "production"], default="standard")
    render.add_argument("--output", type=Path, default=Path("media"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "version":
        print("physix-studio 0.1.0")
        return 0
    if args.command == "list":
        print("templates: moon-ascent, vertical-motion")
        return 0
    if args.command == "render":
        from physix.renderers.manim import ManimRenderer, ManimUnavailableError

        try:
            result = ManimRenderer().render(None, args.output, get_quality(args.quality))
        except ManimUnavailableError as exc:
            raise SystemExit(str(exc)) from exc
        print(result)
        return 0
    if args.samples < 2:
        raise SystemExit("--samples must be at least 2")
    config = VerticalMotionConfig(duration=args.duration)
    model = VerticalMotion(config)
    times = [i * args.duration / (args.samples - 1) for i in range(args.samples)]
    engine = SimulationEngine(model, args.duration, (maximum_height_event,))
    states = engine.run(times)
    payload = {
        "states": [
            {
                "time": s.time,
                "position": s.position,
                "velocity": s.velocity,
                "acceleration": s.acceleration,
                "metadata": dict(s.metadata),
            }
            for s in states
        ],
        "events": [e.name for e in engine.events],
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
