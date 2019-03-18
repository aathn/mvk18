from skysensestreamer.dataproc.coords import LocalCoord, GPSCoord
from skysensestreamer.dataproc import util
from time import time
from collections import deque
from typing import NewType, Tuple, Deque, Union
from math import pi


Angle = NewType("Angle", float)
"""Type definition mostly for simple documentation with type hints."""

Number = Union[int, float]


class Camera:
    """A class that handles the camera and its pan/tilt device."""

    def __init__(self):
        self.gps_position = None
        self.tracked_airplane = None
        self.direction = None
        """The compass angle (in radians) that the pan/tilt plattform has its right side facing."""
        self.airplanes = []

    def to_servo(self, lc: LocalCoord) -> (Angle, Angle):
        """Converts LocalCoords to angles for the servo controller

        :param lc: The local coord to be converted.
        :returns: A tuple containing a pan and a tilt angle.
        """
        pan = (self.direction - lc.azimuth) % (2 * pi)
        tilt = pi / 2 - lc.altitude_angle
        return (pan, tilt)


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

    def __init__(self, plane_id=None, init_time: Number = time()):
        self.id = plane_id
        self.init_time = init_time
        """Time of initialization for the Airplane object"""
        self.extrapolation = lambda x: GPSCoord(0.0, 0.0, 0.0)
        self.timestamped_positions: Deque[Tuple[Number, GPSCoord]] = deque(
            [], self.max_timestamped_positions
        )
        """A deque of tuples which consists of a timestamp and a GPSCoord."""

    def in_view(self, view: View) -> bool:
        pass

    @property
    def position(self) -> GPSCoord:
        """Return the current estimation of self's position"""
        return self.extrapolation(time())

    def append_position(self, new_time: Number, new_pos: GPSCoord):
        """Append a position to the timestamped positions and update the extrapolation"""
        self.timestamped_positions.append((new_time, new_pos))
        self._update_extrapolation()

    def _update_extrapolation(self):
        """Updates self.extrapolation by extrapolating with the current self.timestamped_positions as input.

        If the number of timestamped_positions is one we update it with that position as a constant.
        :code:`self.init_time` is subtracted from the times in order to avoid handling huge numbers, 
        which causes problems in the extrapolation function.
        """
        times = []
        positions = []
        for time_, coord in self.timestamped_positions:
            times.append(time_ - self.init_time)
            positions.append([coord.latitude, coord.longitude, coord.altitude])

        if len(times) == 1:
            self.extrapolation = lambda t: self.timestamped_positions[0][1]
        else:
            extrapolate_array = util.extrapolate(times, positions)
            self.extrapolation = lambda t: GPSCoord(
                *extrapolate_array(t - self.init_time)
            )
