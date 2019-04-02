from skysensestreamer.camera import Camera, View
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.parser import keep_planes_updated, parseGPSCoord
from threading import Thread, Event, Lock
from math import pi

data_dir = "/tmp/flights.js"  # "/tmp/flights.js"
gps_dir = "/var/tmp/position.txt"

stop_flag = Event()
camera = Camera()
parser_thread = Thread(
    target=keep_planes_updated, args=(camera, data_dir, 2.0, stop_flag)
)

camera.direction = 3 * pi / 2
camera.gps_position = parseGPSCoord(gps_dir)
camera.view = View(0, pi / 2, pi / 2, 3 * pi / 2, 40000)

parser_thread.start()
camera.start()
