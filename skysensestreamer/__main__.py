from skysensestreamer.camera import Camera, View
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.parser import keep_planes_updated
from threading import Thread, Event, Lock
from math import pi

data_dir = "/tmp/flights.js"  # "/tmp/flights.js"

stop_flag = Event()
camera = Camera()
parser_thread = Thread(
    target=keep_planes_updated, args=(camera, data_dir, 2.0, stop_flag)
)

camera.direction = 3 * pi / 2
camera.gps_position = GPSCoord(59.477894166666665, 17.905329683333335, 33.720)
camera.view = View(0, pi / 2, pi / 2, 3 * pi / 2, 40000)

parser_thread.start()
camera.start()
