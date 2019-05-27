"""This main file is responsible for starting the camera and also the flight data parsing in an additional thread.

This module does the following:

1. Parse the `config file <config>`_.
2. Create a Camera with settings parsed from the config file.
3. Start a thread with a process that parses and updates flight airplane data.

"""

from skysensestreamer.camera import Camera
from skysensestreamer.parser import keep_planes_updated, parse_gps_coord
from threading import Thread, Event
from configparser import ConfigParser
import sys
import pkg_resources

CONFIG_FILE_NAME = "config"

config_parser = ConfigParser()
config_parser.read_string(
    pkg_resources.resource_string(__name__, CONFIG_FILE_NAME).decode("utf-8")
)


if len(sys.argv) >= 3:
    file_locations = {"flight_data": sys.argv[1], "gps_pos": sys.argv[2]}
else:
    file_locations = config_parser["file_locations"]

camera_settings = config_parser["camera_settings"]
stream_settings = config_parser["stream_settings"]
blacklist = config_parser["blacklist"]

camera = Camera(
    gps_position=parse_gps_coord(file_locations["gps_pos"]),
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
    target=keep_planes_updated,
    args=(camera, file_locations["flight_data"], 2.0, stop_flag),
)

parser_thread.start()
camera.start(
    stream_settings["input_device"],
    stream_settings["format"],
    stream_settings["resolution"],
    stream_settings["bitrate"],
    stream_settings["base_url"],
)
