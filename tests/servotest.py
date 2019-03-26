from skysensestreamer import pantiltcontrol
from time import sleep
from math import pi

# Håll i hatten!
c = pantiltcontrol.Controller()
c.set_position(0, 0)
sleep(2)
c.set_position(pi / 2, pi / 4)
sleep(2)
c.set_position(pi, pi / 3)
sleep(2)
c.set_position(0, pi / 20)
