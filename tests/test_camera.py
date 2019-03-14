import unittest
from skysensestreamer.camera import Airplane
from skysensestreamer.dataproc.coords import GPSCoord


class AirplaneTests(unittest.TestCase):
    def setUp(self):
        init_time = 1551365000.156895
        self.airplane = Airplane(None, init_time)

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
