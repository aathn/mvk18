import unittest
from skysensestreamer.camera import Airplane, Camera, View
from skysensestreamer.dataproc.coords import GPSCoord, LocalCoord
from math import pi


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.view1 = View(0.5, 1.5, 1, 3)
        self.view2 = View(1, 3, 5, 2)
        self.full_view = View(0, pi, 0, 0)
        self.pos0 = LocalCoord(0, 1.5, 0)
        self.pos1 = LocalCoord(0.5, 3, 0)
        self.pos2 = LocalCoord(2, 5.5, 0)
        self.pos3 = LocalCoord(1.4, 1.5, 0)

    def test_contains_returns_true_for_positions_it_does_contain(self):
        self.assertTrue(self.view1.contains(self.pos1))
        self.assertTrue(self.view2.contains(self.pos2))
        self.assertTrue(self.view1.contains(self.pos3))
        self.assertTrue(self.view2.contains(self.pos3))

    def test_contains_returns_false_for_positions_it_does_not_contain(self):
        self.assertFalse(self.view1.contains(self.pos2))
        self.assertFalse(self.view2.contains(self.pos1))
        self.assertFalse(self.view1.contains(self.pos0))
        self.assertFalse(self.view1.contains(self.pos0))

    def test_full_view_contains_everything(self):
        self.assertTrue(self.full_view.contains(self.pos0))
        self.assertTrue(self.full_view.contains(self.pos1))
        self.assertTrue(self.full_view.contains(self.pos2))
        self.assertTrue(self.full_view.contains(self.pos3))

class CameraTests(unittest.TestCase):
    def setUp(self):
        self.camera = Camera()
        self.local_coord1 = LocalCoord(0, 0, 0)
        self.local_coord2 = LocalCoord(pi / 2, pi / 2, 0)
        self.local_coord3 = LocalCoord(3 * pi / 2, pi / 6, 0)


    def test_correct_tilt_angle_conversion(self):
        self.camera.direction = 0
        (_, tilt1) = self.camera.to_servo(self.local_coord1)
        self.assertAlmostEqual(tilt1, pi / 2)
        (_, tilt2) = self.camera.to_servo(self.local_coord2)
        self.assertAlmostEqual(tilt2, 0)
        (_, tilt3) = self.camera.to_servo(self.local_coord3)
        self.assertAlmostEqual(tilt3, pi / 3)


    def test_correct_pan_angle_conversion_when_camera_direction_is_zero(self):
        self.camera.direction = 0
        (pan1, _) = self.camera.to_servo(self.local_coord1)
        self.assertAlmostEqual(pan1, 0)
        (pan2, _) = self.camera.to_servo(self.local_coord2)
        self.assertAlmostEqual(pan2, 3 * pi / 2)
        (pan3, _) = self.camera.to_servo(self.local_coord3)
        self.assertAlmostEqual(pan3, pi / 2)


    def test_correct_pan_angle_conversion_when_camera_direction_is_pi(self):
        self.camera.direction = pi
        (pan1, _) = self.camera.to_servo(self.local_coord1)
        self.assertAlmostEqual(pan1, pi)
        (pan2, _) = self.camera.to_servo(self.local_coord2)
        self.assertAlmostEqual(pan2, pi / 2)


    def test_correct_pan_angle_conversion_when_camera_direction_is_pi_half(self):
        self.camera.direction = pi / 2
        (pan1, _) = self.camera.to_servo(self.local_coord1)
        self.assertAlmostEqual(pan1, pi / 2)
        (pan2, _) = self.camera.to_servo(self.local_coord2)
        self.assertAlmostEqual(pan2, 0)
        (pan3, _) = self.camera.to_servo(self.local_coord3)
        self.assertAlmostEqual(pan3, pi)


class AirplaneTests(unittest.TestCase):
    def setUp(self):
        init_time = 1551365000.156895
        self.airplane = Airplane(init_time)

        self.time1 = 1551365010.156895
        self.time1int = int(self.time1)
        self.coord1 = GPSCoord(20, 20, 700)

        self.time2 = 1551365015.156895
        self.time2int = int(self.time2)
        self.coord2 = GPSCoord(21, 21, 800)

        self.time3 = 1551365020.156895
        self.time3int = int(self.time3)
        self.coord3 = GPSCoord(22, 22, 900)

    def test_single_position_extrapolation_is_constant(self):
        self.airplane.append_position(self.time1int, self.coord1)

        self.assertEqual(self.airplane.extrapolation(self.time2), self.coord1)
        self.assertEqual(self.airplane.extrapolation(self.time3), self.coord1)

    def test_extrapolation_varies_according_to_input_time(self):
        time4 = 1551369827.156829
        time5 = 1551361021.789043

        self.airplane.append_position(self.time1int, self.coord1)
        self.airplane.append_position(self.time2int, self.coord2)
        self.airplane.append_position(self.time3int, self.coord3)

        self.assertNotEqual(
            self.airplane.extrapolation(time4), self.airplane.extrapolation(time5)
        )

    def test_append_linear_positions_returns_correctly_extrapolated_coord(self):
        time_given_linear_extrapolation = 1551365025.0
        coord_assumed_linear_extrapolation = GPSCoord(23, 23, 1000)

        self.airplane.append_position(self.time1int, self.coord1)
        self.airplane.append_position(self.time2int, self.coord2)
        self.airplane.append_position(self.time3int, self.coord3)

        extrapolated_coord = self.airplane.extrapolation(
            time_given_linear_extrapolation
        )

        self.assertAlmostEqual(
            extrapolated_coord.latitude, coord_assumed_linear_extrapolation.latitude
        )
        self.assertAlmostEqual(
            extrapolated_coord.longitude, coord_assumed_linear_extrapolation.longitude
        )
        self.assertAlmostEqual(
            extrapolated_coord.altitude, coord_assumed_linear_extrapolation.altitude
        )


if __name__ == "__main__":
    unittest.main()
