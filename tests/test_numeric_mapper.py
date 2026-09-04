import numpy as np

from src.numeric_mapper import digits_for


def test_luminance_uses_full_charset_range():
    rgb = np.array([[[0, 0, 0], [255, 255, 255]]], dtype=np.uint8)
    assert digits_for(rgb, "0123456789").tolist() == [["0", "9"]]
