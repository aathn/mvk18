import unittest
import math
import skysensestreamer.pantiltcontrol as ptc


class PanTiltTests(unittest.TestCase):
    def test_angle_negative(self):
        self.assertRaises(ValueError, ptc._to_pan_value, -10, (0, 1000))
        self.assertRaises(ValueError, ptc._to_tilt_value, -10, (0, 1000))

    def test_pan_angle_greater_than_pi(self):
        self.assertRaises(ValueError, ptc._to_pan_value, math.pi + 0.1, (0, 1000))

    def test_tilt_angle_greater_than_pi_half(self):
        self.assertRaises(ValueError, ptc._to_tilt_value, math.pi / 2 + 0.1, (0, 1000))

    def test_angle_zero(self):
        lower_bound = 80
        self.assertEquals(
            ptc._to_pan_value(0, (lower_bound, lower_bound + 10)), lower_bound
        )
        self.assertEquals(
            ptc._to_tilt_value(0, (lower_bound, lower_bound + 10)), lower_bound
        )

    def test_pan_angle_pi(self):
        upper_bound = 100
        self.assertEquals(
            ptc._to_pan_value(math.pi, (upper_bound - 10, upper_bound)), upper_bound
        )

    def test_tilt_angle_pi_half(self):
        upper_bound = 100
        self.assertEquals(
            ptc._to_tilt_value(math.pi / 2, (upper_bound - 10, upper_bound)),
            upper_bound,
        )


if __name__ == "__main__":
    unittest.main()
