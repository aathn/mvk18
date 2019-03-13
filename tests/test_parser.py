import unittest
from skysensestreamer import parser
from skysensestreamer.camera import Camera


data_dir = "tests/parse_data"


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.camera = Camera()

    def test_parse_many_flights(self):
        flights = {
            "x406f70": [
                "406F70",
                59.5555,
                17.9249,
                9,
                1650,
                138,
                "7001",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -896,
                "SAS095",
            ],
            "x40704a": [
                "40704A",
                59.1856,
                18.1621,
                3,
                8625,
                217,
                "7402",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -1088,
                "SAS082",
            ],
            "x440820": [
                "440820",
                59.4736,
                17.8951,
                10,
                3375,
                183,
                "6110",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -960,
                "AUA313",
            ],
            "x47807b": [
                "47807B",
                59.2445,
                17.0677,
                217,
                22800,
                432,
                "0746",
                0,
                "",
                "",
                1550677049,
                "",
                "",
                "",
                0,
                2496,
                "SAS579",
            ],
            "x47956b": [
                "47956B",
                59.5348,
                17.5763,
                80,
                4975,
                238,
                "2303",
                0,
                "",
                "",
                1550677075,
                "",
                "",
                "",
                0,
                64,
                "",
            ],
            "x47a619": [
                "47A619",
                59.6755,
                17.6982,
                252,
                7475,
                268,
                "0452",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                2624,
                "NAX817",
            ],
            "x4a815c": [
                "4A815C",
                59.3215,
                18.4402,
                225,
                4000,
                257,
                "2570",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -1152,
                "SCW269P",
            ],
            "x4aaa4c": [
                "4AAA4C",
                59.5202,
                18.1163,
                58,
                850,
                127,
                "5743",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                128,
                "HMF005",
            ],
            "x4aaf09": [
                "4AAF09",
                59.4045,
                17.8699,
                14,
                4025,
                186,
                "7075",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -320,
                "LPA256",
            ],
            "x4ab564": [
                "4AB564",
                59.9847,
                18.4121,
                182,
                16850,
                357,
                "7410",
                0,
                "",
                "",
                1550677087,
                "",
                "",
                "",
                0,
                -960,
                "BRX513S",
            ],
            "x4ab569": [
                "4AB569",
                59.3251,
                18.0232,
                305,
                1075,
                126,
                "0404",
                0,
                "",
                "",
                1550677079,
                "",
                "",
                "",
                0,
                -960,
                "",
            ],
            "x4baa73": [
                "4BAA73",
                59.3704,
                17.9930,
                261,
                4925,
                202,
                "5334",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -768,
                "THY57H",
            ],
            "x4cacc9": [
                "4CACC9",
                59.3311,
                18.8428,
                137,
                20700,
                456,
                "2531",
                0,
                "",
                "",
                1550677087,
                "",
                "",
                "",
                0,
                2368,
                "SAS1764",
            ],
            "x4caf97": [
                "4CAF97",
                59.6011,
                18.7438,
                236,
                10500,
                308,
                "5054",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                -1856,
                "IBK210",
            ],
            "xad9e4d": [
                "AD9E4D",
                59.4251,
                17.3074,
                219,
                21475,
                414,
                "0736",
                0,
                "",
                "",
                1550677088,
                "",
                "",
                "",
                0,
                3520,
                "TWY977",
            ],
        }
        self.assertEqual(parser.parse("{}/test_flights".format(data_dir)), flights)

    def test_parse_empty_json(self):
        self.assertEqual(parser.parse("{}/test_empty".format(data_dir)), {})

    def test_parse_one_flight(self):
        flight = {
            "x47956b": [
                "47956B",
                59.5348,
                17.5763,
                80,
                4975,
                238,
                "2303",
                0,
                "",
                "",
                1550677075,
                "",
                "",
                "",
                0,
                64,
                "",
            ]
        }
        self.assertEqual(parser.parse("{}/test_one_flight".format(data_dir)), flight)

    def test_update_one_flight(self):
        parser.update_airplanes(self.camera, "{}/test_one_flight".format(data_dir))
        self.assertEqual(len(self.camera.airplanes), 1)
        plane = self.camera.airplanes[0]
        self.assertEqual(plane.id, "x47956b")
        self.assertEqual(len(plane.timestamped_positions), 1)
        timestamp = plane.timestamped_positions[0][0]
        position = plane.timestamped_positions[0][1]
        self.assertEqual(timestamp, 1550677075)
        self.assertEqual(position.latitude, 59.5348)
        self.assertEqual(position.longitude, 17.5763)
        self.assertEqual(position.altitude, 4975)

    def test_update_flights_twice(self):
        parser.update_airplanes(self.camera, "{}/test_one_flight".format(data_dir))
        parser.update_airplanes(self.camera, "{}/test_two_flights".format(data_dir))
        self.assertEqual(len(self.camera.airplanes), 2)
        updated_plane = self.camera.airplanes[0]
        new_plane = self.camera.airplanes[1]
        self.assertEqual(updated_plane.id, "x47956b")
        self.assertEqual(new_plane.id, "x406f70")
        self.assertEqual(len(updated_plane.timestamped_positions), 2)
        timestamp = updated_plane.timestamped_positions[1][0]
        position = updated_plane.timestamped_positions[1][1]
        self.assertEqual(timestamp, 1550677080)
        self.assertEqual(position.latitude, 60.5348)
        self.assertEqual(position.longitude, 18.0763)

    def test_update_remove_flights(self):
        parser.update_airplanes(self.camera, "{}/test_one_flight".format(data_dir))
        parser.update_airplanes(self.camera, "{}/test_two_flights".format(data_dir))
        parser.update_airplanes(self.camera, "{}/test_empty".format(data_dir))
        self.assertEqual(len(self.camera.airplanes), 0)


if __name__ == "__main__":
    unittest.main()
