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


if __name__ == "__main__":
    unittest.main()
