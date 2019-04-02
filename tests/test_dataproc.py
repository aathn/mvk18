from skysensestreamer.dataproc import coords
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.dataproc import util

import unittest
import numpy as np


class ExtrapolateTests(unittest.TestCase):
    def test_linear_function_exactly_extrapolated(self):
        def lin_f(t):
            return np.array([0.5, 2.4, -4.1]) + t * np.array([1.0, 1.0, 1.0])

        ts = np.array([0.5, 1.0, 1.5])
        extrapolated = util.extrapolate(ts, np.vstack([lin_f(t) for t in ts]))
        for t in range(2, 10):
            self.assertTrue(np.allclose(extrapolated(t), lin_f(t)))


class CoordTests(unittest.TestCase):
    def setUp(self):
        self.zero_coord = GPSCoord(0.0, 0.0, 0.0)

    def test_get_ecef_x(self):
        ecef_on_x_axis = GPSCoord(0.0, 0.0, 0.0).get_ecef()
        self.assertTrue(np.allclose(ecef_on_x_axis[1:], np.zeros(2)))
        self.assertEqual(ecef_on_x_axis[0], coords.equatorial_radius)

    def test_get_ecef_y(self):
        ecef_on_y_axis = GPSCoord(0.0, 90.0, 0.0).get_ecef()
        self.assertTrue(np.allclose(ecef_on_y_axis[[0, 2]], np.zeros(2)))
        self.assertEqual(ecef_on_y_axis[1], coords.equatorial_radius)

    def test_get_ecef_z(self):
        ecef_on_z_axis = GPSCoord(90.0, 0.0, 0.0).get_ecef()
        self.assertTrue(np.allclose(ecef_on_z_axis[:-1], np.zeros(2)))
        self.assertEqual(ecef_on_z_axis[2], coords.polar_radius)

    def test_get_ecef_mixed(self):
        ecef_mixed = GPSCoord(45.0, 45.0, 0.0).get_ecef()
        self.assertTrue(np.allclose(ecef_mixed[:-1], np.ones(2) * 10480377))
        self.assertTrue(np.isclose(ecef_mixed[2], 14722270))

    def test_to_local_for_straight_north(self):
        north_coord = GPSCoord(45.0, 0.0, 0.0)
        local_north = self.zero_coord.to_local(north_coord)
        self.assertEqual(local_north.azimuth, 0)

    def test_to_local_for_straight_east(self):
        east_coord = GPSCoord(0.0, 90.0, 0.0)
        local_east = self.zero_coord.to_local(east_coord)
        self.assertEqual(local_east.azimuth, np.pi / 2)

    def test_to_local_for_mixed(self):
        mixed_coord = GPSCoord(45.0, 45.0, 0.0)
        local_coord = self.zero_coord.to_local(mixed_coord)
        self.assertTrue(np.isclose(local_coord.azimuth, 0.61865))
        self.assertTrue(np.isclose(local_coord.altitude_angle, 2.09488))
        self.assertTrue(np.isclose(local_coord.distance, 20925520, rtol=0.01))

    def test_to_local_vertical_angle(self):
        self_pos = GPSCoord(59.47789, 17.90532, 32.8084)
        target_pos = GPSCoord(59.47790, 17.90364, 875.9843)
        local_coord = self_pos.to_local(target_pos)
        self.assertTrue(np.isclose(local_coord.altitude_angle, 0.354899))


if __name__ == "__main__":
    unittest.main()
