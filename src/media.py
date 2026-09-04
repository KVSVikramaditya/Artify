"""Shared media rendering service used by both the CLI and browser app."""

from collections.abc import Callable
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .config import RenderConfig
from .frame_processor import adjust_rgb, resize_to_grid
from .gif_exporter import GifExporter
from .renderer import NumericRenderer
from .video_reader import VideoReader

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

ProgressCallback = Callable[[int, int, str], None]


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def render_media(config: RenderConfig, progress: ProgressCallback | None = None) -> Path:
    """Render an image as PNG or a video as a looping GIF."""
    config.validate()
    if is_image(config.input_path):
        return _render_image(config, progress)
    return _render_video(config, progress)


def _render_image(config: RenderConfig, progress: ProgressCallback | None) -> Path:
    if progress:
        progress(0, 1, "Preparing image")
    with Image.open(config.input_path) as source:
        rgb = np.asarray(source.convert("RGB"))
    renderer = NumericRenderer(config.font_size, config.background)
    rows = renderer.rows_for(rgb.shape[1], rgb.shape[0], config.width)
    adjusted = _adjust_rgb_image(rgb, config)
    art = renderer.render(resize_to_grid(adjusted, config.width, rows), config.digits)
    output = config.output_path.with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    art.save(output, optimize=True)
    if progress:
        progress(1, 1, "Image art ready")
    return output


def _adjust_rgb_image(rgb: np.ndarray, config: RenderConfig) -> np.ndarray:
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return adjust_rgb(bgr, config.brightness, config.contrast, config.saturation)


def _render_video(config: RenderConfig, progress: ProgressCallback | None) -> Path:
    reader = VideoReader(config.input_path)
    try:
        info = reader.info
        end = min(info.duration, config.start + (config.duration or info.duration))
        if config.start >= end:
            raise ValueError("The selected start/duration contains no video frames")
        renderer = NumericRenderer(config.font_size, config.background)
        rows = renderer.rows_for(info.width, info.height, config.width)
        total = max(1, round((end - config.start) * config.fps))
        output = config.output_path.with_suffix(".gif")
        exporter = GifExporter(output, config.fps, config.palette_size)
        try:
            for number in range(total):
                frame = reader.frame_at(config.start + number / config.fps)
                if frame is None:
                    break
                rgb = adjust_rgb(frame, config.brightness, config.contrast, config.saturation)
                art = renderer.render(resize_to_grid(rgb, config.width, rows), config.digits)
                exporter.append(art)
                if progress:
                    progress(number + 1, total, f"Rendering frame {number + 1} of {total}")
        finally:
            exporter.close()
        return output
    finally:
        reader.close()
