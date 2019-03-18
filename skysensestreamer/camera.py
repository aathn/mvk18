from __future__ import annotations
from skysensestreamer.dataproc.coords import LocalCoord, GPSCoord
from skysensestreamer.dataproc import util
from time import time
from collections import deque
from typing import NewType, Tuple, Deque, Union
from threading import Lock
from math import pi
import signal
import subprocess


Angle = NewType("Angle", float)
"""Type definition mostly for simple documentation with type hints."""

Number = Union[int, float]


class Camera:
    """A class that handles the camera and its pan/tilt device."""

    def __init__(self, lock: Lock):
        self.gps_position = None
        self.tracked_airplane = None
        self.view = None
        self.direction = None
        """The compass angle (in radians) that the pan/tilt plattform has its right side facing."""
        self.airplanes = []
        self.lock = lock

    def _to_servo(self, lc: LocalCoord) -> (Angle, Angle):
        """Converts LocalCoords to angles for the servo controller.

        :param lc: The local coord to be converted.
        :returns: A tuple containing a pan and a tilt angle.
        """
        pan = (self.direction - lc.azimuth) % (2 * pi)
        tilt = pi / 2 - lc.altitude_angle
        return (pan, tilt)

    def start(self):
        """"""
        stream_handler = FFmpegHandler()
        while True:
            self._search_for_airplane()
            stream_handler.start_stream()
            self._follow_airplane()
            stream_handler.stop_stream()

    def _follow_airplane(self):
        

    def _search_for_airplane(self):
        while True:
            visible = self._get_visible()
            if len(visible) > 0:
                self.tracked_airplane = visible[0]
                break
            
    def _get_visible(self):
        return filter(airplanes, lambda x: x.in_view(self.view))

    def can_see(self, plane: Airplane) -> bool:
        """Check if the camera can see a plane

        :param plane: The plane to check
        :returns: True if plane is in view of the camera
        """
        plane_local = self.gps_position.to_local(plane.position)
        return self.view.contains(plane_local)


class FFmpegHandler:
    """A class that handles ffmpeg streaming from a USB web cam.

	The FFmpegHandler object can start and stop a stream to a certain url.
	Always make sure to stop the previous stream before starting a new one.
	"""

    def __init__(self):
        self.process = None
        self.streaming = False

    def start_stream(
        self,
        url: str,
        input_device: str = '"0"',
        format: str = "avfoundation",
        resolution: str = "640x480",
        bitrate: str = "1000k",
    ):
        """
        Start a process that streams video from USB web cam to url specified.

		:param url: The url or output where streaming data is sent to.
		:param input_device: The USB-camera from which to stream. Default "0"
        :param format: The input format, may differ on different operating systems. Default avfoundation.
		:param resolution: The resolution of the streamed video. Default "640x480"
		:param bitrate: The bitrate of the streamed video. Default "1000k"
		"""

        if self.streaming:
            return  # Return if stream is already running

        cmd = (
            "ffmpeg -f "
            + format
            + " -framerate 30 -video_size "
            + resolution
            + " -pix_fmt uyvy422"
            + " -i "
            + input_device
            + " -f mpegts -codec:v mpeg1video -s "
            + resolution
            + " -b:v "
            + bitrate
            + " -bf 0 "
            + url
        )
        self.process = subprocess.Popen(
            "exec " + cmd, stdout=subprocess.PIPE, shell=True
        )
        self.streaming = True

    def stop_stream(self):
        """Stop streaming process."""
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        self.streaming = False


class View:
    """A class that represents the view for a camera. Used to filter out visible planes."""

    def __init__(
        self,
        upper_bound: Angle,
        lower_bound: Angle,
        left_bound: Angle,
        right_bound: Angle,
    ):
        self.upper_bound: Angle = upper_bound  # Should be less than lower_bound
        self.lower_bound: Angle = lower_bound
        self.left_bound: Angle = left_bound
        self.right_bound: Angle = right_bound

    def contains(self, position: LocalCoord) -> bool:
        """Returns True if the position is within the view.

        :param position: The position to check
        :returns: Whether position is in view
        """
        position_in_view = False
        if self.upper_bound <= position.altitude_angle <= self.lower_bound:
            if self.left_bound <= position.azimuth <= self.right_bound:
                position_in_view = True
            elif self.left_bound >= self.right_bound and (
                self.left_bound <= position.azimuth
                or position.azimuth <= self.right_bound
            ):
                position_in_view = True
        return position_in_view


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
