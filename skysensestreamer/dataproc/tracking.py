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

    :param positions: n x 3 array of positional data
    :param times: n x 1 array of times belonging to the positions
    :returns: function producing the position at time t

    """
    if not (isinstance(np.ndarray, positions) and isinstance(np.ndarray, times)):
        try:
            positions = np.array(positions)
            times = np.array(times)
        except:
            raise TypeError("Input must be in np array compatible format!")
    if not positions.shape[0] == times.shape[0]:
        raise ValueError("Input arrays must have the same length!")
    if len(positions.shape) != 2 or positions[1] != 3:
        raise ValueError("Position array must be n x 3!")

    direction, intercept = la.lstsq(
        np.hstack([times, np.ones(len(times))]), positions, rcond=None
    )[0]

    return lambda t: intercept + t * direction
