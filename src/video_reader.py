from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class VideoInfo:
    width: int
    height: int
    fps: float
    frame_count: int

    @property
    def duration(self) -> float:
        return self.frame_count / self.fps if self.fps else 0.0


class VideoReader:
    def __init__(self, path: Path) -> None:
        self.capture = cv2.VideoCapture(str(path))
        if not self.capture.isOpened():
            raise ValueError("The input could not be opened as a video")
        self.info = VideoInfo(
            int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            float(self.capture.get(cv2.CAP_PROP_FPS)),
            int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        )
        if not self.info.width or not self.info.height or not self.info.fps:
            self.close()
            raise ValueError("The video has invalid dimensions or frame rate")

    def frame_at(self, seconds: float) -> np.ndarray | None:
        self.capture.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)
        ok, frame = self.capture.read()
        return frame if ok else None

    def close(self) -> None:
        self.capture.release()
