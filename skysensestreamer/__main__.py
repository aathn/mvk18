"""This main file is responsible for starting the camera and also the flight data parsing in an additional thread.

This module does the following:

1. Parse the `config file <config.ini>`_.
2. Create a Camera with settings parsed from the config file.
3. Start a thread with a process that parses and updates flight airplane data.

"""

from skysensestreamer.camera import Camera
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.parser import keep_planes_updated, parse_gps_coord
from threading import Thread, Event
from configparser import ConfigParser

CONFIG_FILE_PATH = "skysensestreamer/conf.ini"
FLIGHT_DATA_FILE_PATH = "/tmp/flights.js"
GPS_POS_FILE_PATH = "/var/tmp/position.txt"

config_parser = ConfigParser()
config_parser.read(CONFIG_FILE_PATH)
camera_settings = config_parser["camera_settings"]
blacklist = config_parser["blacklist"]

camera = Camera(
    gps_position=parse_gps_coord(GPS_POS_FILE_PATH),
    direction=camera_settings.getfloat("direction"),
    view_upper_bound=camera_settings.getfloat("view_upper_bound"),
    view_lower_bound=camera_settings.getfloat("view_lower_bound"),
    view_left_bound=camera_settings.getfloat("view_left_bound"),
    view_right_bound=camera_settings.getfloat("view_right_bound"),
    view_distance=camera_settings.getint("view_distance"),
    blacklisted_flights=blacklist["blacklisted_flight_numbers"].split(","),
    blacklisted_ids=blacklist["blacklisted_ids"].split(","),
)

stop_flag = Event()
parser_thread = Thread(
    target=keep_planes_updated, args=(camera, FLIGHT_DATA_FILE_PATH, 2.0, stop_flag)
)

parser_thread.start()
camera.start()
