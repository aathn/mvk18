import unittest
from skysensestreamer.camera import Airplane
from skysensestreamer.dataproc.coords import GPSCoord


class AirplaneTests(unittest.TestCase):
    def setUp(self):
        self.airplane = Airplane()

        self.time1 = 1551365010.156895
        self.time1int = int(self.time1)
        self.coord1 = GPSCoord(20, 20, 700)

        self.time2 = 1551365015.156895
        self.time2int = int(self.time2)
        self.coord2 = GPSCoord(21, 21, 800)

        self.time3 = 1551365020.156895
        self.time3int = int(self.time3)
        self.coord3 = GPSCoord(22, 22, 900)

    def test_airplane_single_position_extrapolation_is_constant(self):
        self.airplane.append_position(self.time1int, self.coord1)

        self.assertEqual(self.airplane.extrapolation(self.time2), self.coord1)
        self.assertEqual(self.airplane.extrapolation(self.time3), self.coord1)

    def test_airplane_append_linear_positions_returns_GPSCoord(self):
        self.airplane.append_position(self.time1int, self.coord1)
        self.airplane.append_position(self.time2int, self.coord2)
        self.airplane.append_position(self.time3int, self.coord3)

        self.assertIsInstance(self.airplane.extrapolation(self.time4), GPSCoord)


if __name__ == "__main__":
    unittest.main()
