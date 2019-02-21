"""
This module defines an object used to control the pan/tilt plattform.
Many parts of the code are currently subject to change.
"""
import maestro
import math


def _to_pan_value(angle, target_range):
    """
    Converts an angle to a corresponding value read by the Maetstro.

    :param angle: an angle in radians in range [0,π], 0 is left, π is right
    :param target_range: the range of values to map to
    :type angle: float
    :type target_range: (int, int)
    :returns: a target value for the Maestro
    :rtype: int

    """
    if angle > math.pi or angle < 0:
        raise ValueError("Expected an angle within the pan range [0,π].")

    delta_y = target_range[1] - target_range[0]
    delta_x = math.pi
    return int((delta_y / delta_x) * angle + target_range[0])


def _to_tilt_value(angle, target_range):
    """
    Converts an angle to a corresponding value read by the Maetstro.

    :param angle: an angle in range [0,π/2], 0 is horizontal, π/2 is vertical
    :param target_range: the range of values to map to
    :type angle: float
    :type target_range: (int, int)
    :returns: a target value for the Maestro
    :rtye: int

    """
    if angle > math.pi / 2 or angle < 0:
        raise ValueError("Expected an angle within the tilt range [0,π/2]")

    delta_y = target_range[1] - target_range[0]
    delta_x = math.pi / 2
    return int((delta_y / delta_x) * angle + target_range[0])


class Controller:
    def __init__(self):
        """Creates the controller object from the maestro module and
        configures the range and the speed.
        """
        # The ranges for the servos. Change these to calibrate the servos.
        self.pan_range = (2060, 9250)
        self.tilt_range = (7500, 12000)

        self.servo = maestro.Controller()
        self.servo.setRange(0, self.pan_range[0], self.pan_range[1])
        self.servo.setRange(1, self.tilt_range[0], self.tilt_range[1])
        self.servo.setSpeed(0, 0)
        self.servo.setSpeed(1, 0)

    def set_position(self, pan_angle, tilt_angle):
        """ Sets the plattform to the specified angles.

        :param pan_angle: an angle in the range [0,π]
        :param tilt_angle: an angle in the range [0,π/2]

        """
        p = _to_pan_value(pan_angle, self.pan_range)
        t = _to_tilt_value(tilt_angle, self.tilt_range)
        self.servo.setTarget(0, p)
        self.servo.setTarget(1, t)

    def exit(self):
        self.servo.close()
