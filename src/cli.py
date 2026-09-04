import argparse
from pathlib import Path

from .config import RenderConfig
from .media import render_media


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Convert a video clip into coloured numeric-art GIF frames.")
    p.add_argument("input", type=Path, help="Input MP4/video path")
    p.add_argument("--output", type=Path, required=True, help="Output GIF path")
    p.add_argument("--width", type=int, default=140, help="Numeric characters across (default: 140)")
    p.add_argument("--fps", type=float, default=12, help="Output FPS (default: 12)")
    p.add_argument("--digits", default=" .·,:;i1tfLCG08@#%$&WM", help="Characters used from dark to bright")
    p.add_argument("--font-size", type=int, default=8)
    p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--duration", type=float)
    p.add_argument("--brightness", type=float, default=1.0)
    p.add_argument("--contrast", type=float, default=1.0)
    p.add_argument("--saturation", type=float, default=1.0)
    p.add_argument("--timecode", action="store_true", help="Show the source timestamp in the top-right corner")
    p.add_argument("--palette-size", type=int, default=256, help="GIF palette size: 2–256 (default: 256)")
    return p


def main() -> None:
    args = parser().parse_args()
    config = RenderConfig(
        input_path=args.input,
        output_path=args.output,
        width=args.width,
        fps=args.fps,
        digits=args.digits,
        font_size=args.font_size,
        start=args.start,
        duration=args.duration,
        brightness=args.brightness,
        contrast=args.contrast,
        saturation=args.saturation,
        background=(0, 0, 0),
        timecode=args.timecode,
        palette_size=args.palette_size,
    )
    try:
        config.validate()
        def report(done: int, total: int, message: str) -> None:
            print(f"{message} ({done}/{total})")

        output = render_media(config, report)
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"Done: {output} ({size_mb:.1f} MB)")
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Error: {exc}")
