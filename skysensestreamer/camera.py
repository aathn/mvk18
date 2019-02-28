from dataproc.coords import LocalCoord, GPSCoord
import dataproc.util as util
from time import time
from collections import deque
from typing import NewType, Tuple, Deque


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


class Airplane:
    max_timestamped_positions = 3

    def __init__(self):
        self.id = None
        self.extrapolation = lambda x: GPSCoord(0.0, 0.0, 0.0)
        self.timestamped_positions: Deque[Tuple[int, GPSCoord]] = deque(
            [], self.max_timestamped_positions
        )
        """A deque of tuples which consists of a timestamp and a GPSCoord."""

    def in_view(self, view: View) -> bool:
        pass

    @property
    def position(self) -> GPSCoord:
        """Return the current estimation of self's position"""
        return self.extrapolation(time())

    def append_position(self, new_time: int, new_pos: GPSCoord):
        """Append a position to the timestamped positions and update the extrapolation"""
        self.timestamped_positions.append((new_time, new_pos))
        self._update_extrapolation()

    def _update_extrapolation(self):
        time_pos_array = [
            [time_, coord.latitude, coord.longitude, coord.altitude]
            for time_, coord in self.timestamped_positions
        ]

        extrapolate_array = util.extrapolate(
            time_pos_array[:][0], time_pos_array[:][1:]
        )
        self.extrapolation = lambda t: GPSCoord(*extrapolate_array(t))
