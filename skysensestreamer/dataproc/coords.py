"""
This file contains functions for processing of coordinate data.
"""

import numpy as np
import numpy.linalg as la




def _horizontal_bearing(self, target: GPSCoords) -> float:
    """ Calculate the horizontal bearing between self and the target point.

    Get the horizontal bearing, using the following formula:
        θ = atan2(sin(Δlong).cos(target.lat),
                  cos(self.lat).sin(target.lat) − sin(self.lat).cos(target.lat).cos(Δlong))

    :param target: GPS coordinates for the target point.
    :returns: The horizontal bearing in radians
    """

    d_long = self.long - target.long

    x = np.sin(d_long) * np.cos(target.lat)
    y = np.cos(self.lat) * np.sin(target.lat) - (
        np.sin(self.lat) * np.cos(target.lat) * np.cos(d_long)
    )

    return (np.atan2(x, y) + 2 * np.pi) % 2 * np.pi
    """
