from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RenderConfig:
    input_path: Path
    output_path: Path
    width: int = 140
    fps: float = 12.0
    # Ordered from visually light to visually dense.  The first characters keep
    # shadows quiet; later characters carry detail in bright regions.
    digits: str = " .·,:;i1tfLCG08@#%$&WM"
    font_size: int = 8
    start: float = 0.0
    duration: float | None = None
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    background: tuple[int, int, int] = (0, 0, 0)
    timecode: bool = False
    palette_size: int = 256

    def validate(self) -> None:
        if not self.input_path.is_file():
            raise ValueError(f"Input video was not found: {self.input_path}")
        if self.width < 20:
            raise ValueError("--width must be at least 20")
        if self.fps <= 0:
            raise ValueError("--fps must be greater than zero")
        if self.font_size < 4:
            raise ValueError("--font-size must be at least 4")
        if not self.digits:
            raise ValueError("--digits cannot be empty")
        if self.start < 0:
            raise ValueError("--start cannot be negative")
        if self.duration is not None and self.duration <= 0:
            raise ValueError("--duration must be greater than zero")
        if self.palette_size not in (2, 4, 8, 16, 32, 64, 128, 256):
            raise ValueError("--palette-size must be a power of two from 2 through 256")
        for name, value in (("brightness", self.brightness), ("contrast", self.contrast), ("saturation", self.saturation)):
            if value <= 0:
                raise ValueError(f"--{name} must be greater than zero")
