from time import sleep, time
from subprocess import Popen
import atexit

longitude_limit = 0.04  # The limit for how far to the left/right the airplane is

latitude = 0.007
longitude = -longitude_limit
longitude_speed = 0.01
altitude = 1000

server = Popen(["sudo", "npm", "start"], cwd="nodeserver")
sleep(10)
streamer = Popen(
    [
        "sudo",
        "-E",
        "python3",
        "-m",
        "skysensestreamer",
        "/home/kth/src/skysensestreamer/tests/demotest/flights.js",
        "/home/kth/src/skysensestreamer/tests/demotest/position.txt",
    ]
)

atexit.register(server.terminate)
atexit.register(streamer.terminate)

while True:
    demoaircraft = (
        'fr24_callback({"x47956b":["47956B",'
        + str(latitude)
        + ","
        + str(longitude)
        + ",80,"
        + str(altitude)
        + ',238,"2303",0,"","",'
        + str(int(time()))
        + ',"","","",0,64,""]});'
    )
    with open("flights.js", "w+") as file:
        file.write(demoaircraft)
    if abs(longitude) > longitude_limit:
        longitude_speed = -longitude_speed
    longitude = round(longitude + longitude_speed, 4)
    print(demoaircraft)
    sleep(5)

