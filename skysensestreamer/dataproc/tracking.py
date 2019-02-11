"""
This file contains functions for controlling how the camera should prioritize
tracking different planes, handling of sight and extrapolation of airplane
positions.

We might want to make a class keeping a list of airplanes within reach along
with their extrapolated position and visibility status.
"""

import numpy as np
import numpy.linalg as la
from typing import Callable


def extrapolate(
    positions: np.ndarray, times: np.ndarray
) -> Callable[[float], np.ndarray]:
    """Extrapolate flight positions based on previous data

    Produce a function giving the extrapolated position for a given time,
    based on the observations in the input. The extrapolation is
    linear and uses numpy's least squares function.

    :param positions: n x k array of positional data (k = 2 for camera angles)
    :param times: n x 1 array of times belonging to the positions
    :returns: function producing the position at time t

    """
    positions = np.array(positions)
    times = np.array(times)

    direction, intercept = la.lstsq(
        np.vstack([times, np.ones(len(times))]).transpose(), positions, rcond=None
    )[0]

    return lambda t: intercept + t * direction
