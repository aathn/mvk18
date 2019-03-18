from skysensestreamer.camera import Camera
from skysensestreamer.parser import keep_airplanes_updated
from threading import Thread, event, lock

data_dir = "/var/flights.js"

stop_flag = Event()
lock = Lock()
camera = Camera(lock)
parser_thread = Thread(
    target=keep_airplanes_updated, args=(camera, data_dir, 2.0, stop_flag, lock)
)

camera.start()
