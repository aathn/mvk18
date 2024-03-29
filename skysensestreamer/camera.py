from skysensestreamer.dataproc.coords import LocalCoord, GPSCoord
from skysensestreamer.dataproc import util
from skysensestreamer.pantiltcontrol import Controller
from time import time, sleep
from collections import deque
from typing import NewType, Union, List
from threading import Lock
from math import pi
import signal
import subprocess


Angle = NewType("Angle", float)
"""Type definition mostly for simple documentation with type hints."""

Number = Union[int, float]

SERVO_UPDATE_DELAY = 0.5
"""The delay between servo updates when tracking a plane"""
CAMERA_SEARCH_DELAY = 1
"""The delay between polls to the airplane list when waiting for a plane to track"""


class Camera:
    """A class that handles the camera and its pan/tilt device."""

    def __init__(
        self,
        gps_position: GPSCoord,
        direction: Angle,
        view_upper_bound: Angle,
        view_lower_bound: Angle,
        view_left_bound: Angle,
        view_right_bound: Angle,
        view_distance: int,
        serial_port: str = "/dev/ttyACM0",
        blacklisted_flights: List[str] = [],
        blacklisted_ids: List[str] = [],
    ):
        """
        :param gps_position: The position of the Skysense and camera
        :param direction: The compass angle (in radians) that the pan/tilt platform has its right side facing
        :param view_upper_bound: The angle in radians which is the highest the camera can point to and still see the
                                 sky (zero is straight up)
        :param view_lower_bound: The angle in radians which is the lowest the camera can point to and still see the
                                 sky (zero is straight up)
        :param view_left_bound: The compass angle in radians which is the leftmost point the camera can point to and
                                still see the sky (zero is north and increasing values represent clockwise rotation)
        :param view_right_bound: The compass angle in radians which is the rightmost point the camera can point to and
                                 still see the sky (zero is north and increasing values represent clockwise rotation)
        :param serial_port: The name of the serial port of the pan/tilt controller.
        :param view_distance: The camera's view distance in feet
        :param blacklisted_flights: Flight numbers containing any string in this list will be ignored when searching for planes to stream

        """
        self.gps_position = gps_position
        self.direction = direction
        """The compass angle (in radians) that the pan/tilt platform has its right side facing"""
        self.view = View(
            view_upper_bound,
            view_lower_bound,
            view_left_bound,
            view_right_bound,
            view_distance,
        )
        self.airplane_lock = Lock()
        """Used to provide exclusive access to the airplanes list"""
        self.controller = Controller(serial_port)
        """The object used to control the servos in the pan/tilt platform"""
        self.tracked_airplane = None
        self.airplanes = []
        """A list of airplanes in the vicinity of the Skysense that is updated by the parser thread started in 
        __main__.py"""
        self.blacklisted_flights = blacklisted_flights
        self.blacklisted_ids = blacklisted_ids

    @property
    def airplanes(self) -> List["Airplane"]:
        with self.airplane_lock:
            return self.__airplanes

    @airplanes.setter
    def airplanes(self, planes: List["Airplane"]):
        with self.airplane_lock:
            self.__airplanes = planes

    def _to_servo(self, lc: LocalCoord) -> (Angle, Angle):
        """Converts LocalCoords to angles for the servo controller.

        :param lc: The local coord to be converted.
        :returns: A tuple containing a pan and a tilt angle.

        """
        pan = (self.direction - lc.azimuth) % (2 * pi)
        tilt = pi / 2 - lc.altitude_angle
        return pan, tilt

    def start(self, input_device, format, resolution, bitrate, base_url):
        """Start tracking, filming and streaming airplanes.

        :param input_device: The USB-camera from which to stream. Default '0'
        :param format: The input format, may differ on different operating systems. Default avfoundation.
        :param resolution: The resolution of the streamed video. Default '640x480'
        :param bitrate: The bitrate of the streamed video. Default '1000k'
        :param base_url: The url to output the streams to.

        """
        stream_handler = FFmpegHandler(input_device, format, resolution, bitrate)
        while True:
            self._search_for_airplane()
            stream_handler.start_stream(
                "{}/{}".format(base_url, self.tracked_airplane.id)
            )
            self._follow_tracked_plane()
            stream_handler.stop_stream()

    def _follow_tracked_plane(self):
        while self.can_see(self.tracked_airplane):
            print("Following plane: ", self.tracked_airplane.id)
            print("Tracked pos: ", self.tracked_airplane.position)
            localcoord = self.gps_position.to_local(self.tracked_airplane.position)
            print(
                "Localcoord: ",
                localcoord.azimuth,
                localcoord.altitude_angle,
                localcoord.distance,
            )
            pan_angle, tilt_angle = self._to_servo(localcoord)
            print("Pan: ", pan_angle, "Tilt: ", tilt_angle)
            self.controller.set_position(pan_angle, tilt_angle)
            sleep(SERVO_UPDATE_DELAY)

    def _search_for_airplane(self):
        while True:
            visible = self._get_visible()
            print("Searching for planes. Visible: ", [plane.id for plane in visible])
            # print("Show all dists: ", [self.gps_position.to_local(plane.position).distance for plane in self.airplanes])
            if len(visible) > 0:
                self._select_plane(visible)
                break
            sleep(CAMERA_SEARCH_DELAY)

    def _select_plane(self, planes: List["Airplane"]):
        planes.sort(key=lambda x: self.gps_position.to_local(x.position).distance)
        self.tracked_airplane = planes[0]

    def _get_visible(self):
        return [plane for plane in self.airplanes if self.can_see(plane)]

    def can_see(self, plane: "Airplane") -> bool:
        """Check if the camera can see a plane

        :param plane: The plane to check
        :returns: True if plane is in view of the camera

        """
        # Check if flight is blacklisted
        for flight_nr in self.blacklisted_flights:
            if flight_nr in plane.flight_nr:
                return False

        # Check if plane is blacklisted
        for id_num in self.blacklisted_ids:
            if id_num == plane.id:
                return False

        plane_local = self.gps_position.to_local(plane.position)
        return self.view.contains(plane_local)


class FFmpegHandler:
    """A class that handles ffmpeg streaming from a USB web cam.

    The FFmpegHandler object can start and stop a stream to a certain url.
    Always make sure to stop the previous stream before starting a new one.

    """

    def __init__(self, input_device, format, resolution, bitrate):
        self.process = None
        self.streaming = False
        self.input_device = input_device
        self.format = format
        self.resolution = resolution
        self.bitrate = bitrate

    def start_stream(self, url: str):
        """Start a process that streams video from USB web cam to url specified.

        :param url: The url or output where streaming data is sent to.

        """

        if self.streaming:
            return  # Return if stream is already running

        cmd = (
            "ffmpeg -f "
            + self.format
            + " -framerate 30 -video_size "
            + self.resolution
            + " -pix_fmt uyvy422"
            + " -i "
            + self.input_device
            + " -f mpegts -codec:v mpeg1video -s "
            + self.resolution
            + " -b:v "
            + self.bitrate
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
        distance: int,
    ):
        self.upper_bound = upper_bound  # TODO: Should be less than lower_bound
        self.lower_bound = lower_bound
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.distance = distance

    def contains(self, position: LocalCoord) -> bool:
        """Returns True if the position is within the view.

        :param position: The position to check
        :returns: Whether position is in view

        """
        position_in_view = False
        if (
            position.distance < self.distance
            and self.upper_bound <= position.altitude_angle <= self.lower_bound
        ):
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

    def __init__(self, plane_id=None, init_time: Number = time(), flight_nr: str = ""):
        self.id = plane_id
        self.flight_nr = flight_nr
        self.init_time = init_time
        """Time of initialization for the Airplane object"""
        self.extrapolation = lambda x: GPSCoord(0.0, 0.0, 0.0)
        self.timestamped_positions = deque([], self.max_timestamped_positions)
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
