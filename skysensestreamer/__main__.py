from skysensestreamer.camera import Camera, View
from skysensestreamer.coords import GPSCoord
from skysensestreamer.parser import keep_airplanes_updated
from threading import Thread, event, lock
from math import pi

data_dir = "../test.js"  # "/var/flights.js"

stop_flag = Event()
camera = Camera()
parser_thread = Thread(
    target=keep_airplanes_updated, args=(camera, data_dir, 2.0, stop_flag)
)

camera.direction = 0
camera.gps_position = GPSCoord(0, 0, 0)
camera.view = View(0, pi / 2, pi, 0)

camera.start()
