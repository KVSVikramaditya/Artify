from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .numeric_mapper import digits_for


def load_monospace_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Menlo.ttc",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


class NumericRenderer:
    def __init__(self, font_size: int, background: tuple[int, int, int]) -> None:
        self.font = load_monospace_font(font_size)
        box = self.font.getbbox("0")
        self.cell_width = max(1, box[2] - box[0])
        self.cell_height = max(1, box[3] - box[1] + 2)
        self.background = background

    def rows_for(self, source_width: int, source_height: int, columns: int) -> int:
        aspect = source_width / source_height
        return max(1, round(columns * self.cell_width / (aspect * self.cell_height)))

    def render(self, grid_rgb: np.ndarray, charset: str) -> Image.Image:
        rows, columns, _ = grid_rgb.shape
        image = Image.new("RGB", (columns * self.cell_width, rows * self.cell_height), self.background)
        draw = ImageDraw.Draw(image)
        symbols = digits_for(grid_rgb, charset)
        for y in range(rows):
            for x in range(columns):
                draw.text((x * self.cell_width, y * self.cell_height), symbols[y, x],
                          font=self.font, fill=tuple(map(int, grid_rgb[y, x])))
        return image

    def add_timecode(self, image: Image.Image, seconds: float) -> Image.Image:
        """Add a small, legible source-time marker outside the character field."""
        minutes, remainder = divmod(max(0, seconds), 60)
        label = f"◉ {int(minutes):02d}:{remainder:04.1f}"
        draw = ImageDraw.Draw(image)
        box = draw.textbbox((0, 0), label, font=self.font)
        padding = 8
        x = image.width - (box[2] - box[0]) - padding
        y = padding
        draw.rounded_rectangle((x - 5, y - 3, image.width - 3, y + (box[3] - box[1]) + 4), radius=4, fill=(4, 20, 28))
        draw.text((x, y), label, font=self.font, fill=(70, 235, 255))
        return image
