"""
This module defines an object used to control the pan/tilt platform.
"""
from skysensestreamer import maestro
from math import pi

PAN_ANGLE_RANGE = (0, pi)
TILT_ANGLE_RANGE = (0, pi / 2)


def _convert_angle(
    angle: float, input_range: (float, float), target_range: (int, int)
) -> int:
    """
    Converts an angle to a corresponding value read by the Maestro.

    :param angle: an angle in radians in range specified by input_range.
    :param input_range: the range of expected angles. With current hardware
    it should be [0, π] for pan and [0, π/2] for tilt.
    :param target_range: the range of values to map to
    :type angle: float
    :type input_range: (float, float)
    :type target_range: (int, int)
    :returns: a target value for the Maestro
    :rtype: int

    """
    if angle > input_range[1] or angle < input_range[0]:
        raise ValueError("Expected an angle within the specified range.")

    delta_y = target_range[1] - target_range[0]
    delta_x = input_range[1] - input_range[0]
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
        self.servo.setSpeed(0, 25)
        self.servo.setSpeed(1, 25)

    def set_position(self, pan_angle, tilt_angle):
        """ Sets the platform to the specified angles.

        :param pan_angle: an angle in the range [0,π]
        :param tilt_angle: an angle in the range [0,π/2]

        """
        p = _convert_angle(pan_angle, PAN_ANGLE_RANGE, self.pan_range)
        t = _to_tilt_value(tilt_angle, TILT_ANGLE_RANGE, self.tilt_range)
        self.servo.setTarget(0, p)
        self.servo.setTarget(1, t)

    def exit(self):
        self.servo.close()
