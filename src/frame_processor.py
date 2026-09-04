import cv2
import numpy as np


def adjust_rgb(frame_bgr: np.ndarray, brightness: float, contrast: float, saturation: float) -> np.ndarray:
    """Apply small, predictable colour adjustments and return RGB."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgb = np.clip((rgb.astype(np.float32) - 127.5) * contrast + 127.5, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * brightness, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def resize_to_grid(rgb: np.ndarray, columns: int, rows: int) -> np.ndarray:
    """Use area sampling so each digit represents its source region."""
    return cv2.resize(rgb, (columns, rows), interpolation=cv2.INTER_AREA)
