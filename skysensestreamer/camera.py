from dataproc.coords import LocalCoord, GPSCoord
from collections import deque
from typing import NewType, Tuple


Angle = NewType("Angle", float)
"""Type definition mostly for simple documentation with type hints."""


class Camera:
    """A class that handles the camera and its pan/tilt device."""

    def __init__(self):
        self.gps_position = None
        self.tracked_airplane = None
        self.direction = None
        self.airplanes = []


class View:
    """A class that represents the view for a camera. Used to filter out visible planes."""

    def __init__(
        self,
        upper_bound: Angle,
        lower_bound: Angle,
        left_bound: Angle,
        right_bound: Angle,
    ):
        self.upper_bound: Angle = upper_bound
        self.lower_bound: Angle = lower_bound
        self.left_bound: Angle = left_bound
        self.right_bound: Angle = right_bound

    def in_view(localcoord: LocalCoord) -> bool:
        pass


class Airplane:
    max_timestamped_positions = 3

    def __init__(self):
        self.id = None
        self.timestamped_positions: Deque[Tuple[int, GPSCoord]] = deque(
            [], self.max_timestamped_positions
        )
        """A deque of tuples which consists of a timestamp and a GPSCoord."""
