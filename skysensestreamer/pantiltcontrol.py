"""
This module defines an object used to control the pan/tilt plattform.
Many parts of the code are currently subject to change.
"""
import maestro
import math


def _to_pan_value(angle):
    """Converts and angle to a corresponding value read by the Maetstro.

    :param angle: an angle in the range [0,π]
    :returns: an integer value to be read by the maestro

    """
    if angle > math.pi or angle < 0:
        raise ValueError("Expected an angle in range [0,π]")

    return int((7040 / math.pi) * angle + 2360)


def _to_tilt_value(angle):
    """Converts and angle to a corresponding value read by the Maetstro.

    :param angle: an angle in the range [0,π/2]
    :returns: an integer value to be read by the maestro

    """
    if angle > math.pi / 2 or angle < 0:
        raise ValueError("Expected an angle in range [0,π/2]")

    return int((6080 / math.pi) * angle + 7760)


class Controller:
    def __init__(self):
        """Creates the controller object from the maestro module and
        configures the range and the speed.
        """
        self.servo = maestro.Controller()
        self.servo.setRange(0, 2360, 9400)  # The ranges may need tweaking
        self.servo.setRange(1, 7760, 10800)
        self.servo.setSpeed(0, 10)
        self.servo.setSpeed(1, 10)

    def set_position(self, pan_angle, tilt_angle):
        """ Sets the plattform to the specified angles.

        :param pan_angle: an angle in the range [0,π]
        :param tilt_angle: an angle in the range [0,π/2]

        """
        p = _to_pan_value(pan_angle)
        t = _to_tilt_value(tilt_angle)
        self.servo.setTarget(0, p)
        self.servo.setTarget(1, t)

    def exit(self):
        self.servo.close()
