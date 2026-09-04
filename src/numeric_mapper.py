import numpy as np


def luminance(rgb: np.ndarray) -> np.ndarray:
    """Return perceptual brightness (0–255) for an RGB image."""
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]).astype(np.uint8)


def digits_for(rgb: np.ndarray, charset: str) -> np.ndarray:
    """Map each cell to a digit: dark cells use the first character."""
    levels = luminance(rgb).astype(np.float32) / 255.0
    indices = np.minimum((levels * len(charset)).astype(int), len(charset) - 1)
    return np.asarray(list(charset), dtype="<U1")[indices]
