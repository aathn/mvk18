"""This main file is responsible for starting the camera and also the flight data parsing in an additional thread.

The module does the following:
1.

"""

from skysensestreamer.camera import Camera
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.parser import keep_planes_updated
from threading import Thread, Event
from configparser import ConfigParser

CONFIG_FILE_PATH = "conf.ini"
FLIGHT_DATA_FILE_PATH = "/tmp/flights.js"

config_parser = ConfigParser()
config_parser.read(CONFIG_FILE_PATH)
camera_settings = config_parser["camera_settings"]

camera = Camera(
    gps_position=GPSCoord(
        0, 0, 0
    ),  # TODO: This GPS position is temporary until GPS position parsing is in place
    direction=camera_settings.getfloat("direction"),
    view_upper_bound=camera_settings.getfloat("view_upper_bound"),
    view_lower_bound=camera_settings.getfloat("view_lower_bound"),
    view_left_bound=camera_settings.getfloat("view_left_bound"),
    view_right_bound=camera_settings.getfloat("view_right_bound"),
)

stop_flag = Event()
parser_thread = Thread(
    target=keep_planes_updated, args=(camera, FLIGHT_DATA_FILE_PATH, 2.0, stop_flag)
)

parser_thread.start()
camera.start()
