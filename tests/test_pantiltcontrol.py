import unittest
import math
import skysensestreamer.pantiltcontrol as ptc


class PanTiltTests(unittest.TestCase):
    def test_angle_negative(self):
        self.assertRaises(ValueError, ptc._convert_angle, -10, (0, math.pi), (0, 1000))

    def test_pan_angle_greater_than_pi(self):
        self.assertRaises(
            ValueError, ptc._convert_angle, math.pi + 0.1, (0, math.pi), (0, 1000)
        )

    def test_tilt_angle_greater_than_pi_half(self):
        self.assertRaises(
            ValueError,
            ptc._convert_angle,
            math.pi / 2 + 0.1,
            (0, math.pi / 2),
            (0, 1000),
        )

    def test_angle_zero(self):
        lower_bound = 80
        self.assertEqual(
            ptc._convert_angle(0, (0, math.pi), (lower_bound, lower_bound + 10)),
            lower_bound,
        )

    def test_pan_angle_pi(self):
        upper_bound = 100
        self.assertEqual(
            ptc._convert_angle(math.pi, (0, math.pi), (upper_bound - 10, upper_bound)),
            upper_bound,
        )

    def test_tilt_angle_pi_half(self):
        upper_bound = 100
        self.assertEqual(
            ptc._convert_angle(
                math.pi / 2, (0, math.pi / 2), (upper_bound - 10, upper_bound)
            ),
            upper_bound,
        )

    def test_pan_angle_pi_half(self):
        lower_bound = 100
        upper_bound = 200
        self.assertEqual(
            ptc._convert_angle(math.pi / 2, (0, math.pi), (lower_bound, upper_bound)),
            (upper_bound - lower_bound) / 2 + lower_bound,
        )

    def test_tilt_angle_pi_divided_by_four(self):
        lower_bound = 100
        upper_bound = 200
        self.assertEqual(
            ptc._convert_angle(
                math.pi / 4, (0, math.pi / 2), (lower_bound, upper_bound)
            ),
            (upper_bound - lower_bound) / 2 + lower_bound,
        )


if __name__ == "__main__":
    unittest.main()
