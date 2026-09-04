from pathlib import Path

import imageio.v2 as imageio
from PIL import Image


class GifExporter:
    """Streams frames into the encoder instead of retaining the clip in RAM."""
    def __init__(self, output: Path, fps: float, palette_size: int = 256) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        self.writer = imageio.get_writer(str(output), mode="I", duration=1 / fps, loop=0, palettesize=palette_size, subrectangles=True)

    def append(self, image: Image.Image) -> None:
        self.writer.append_data(image)

    def close(self) -> None:
        self.writer.close()
