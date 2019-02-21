"""
This file contains functions for processing of coordinate data.
"""

import numpy as np
import numpy.linalg as la


# The radii of the Earth's major and minor axes, in feet
equatorial_radius = 20925646.3
polar_radius = 20855486.5


def angles_toward(self, target: GPSCoords) -> float:
    """ Calculate the horizontal and vertical bearings between self and the target point.

    The implementation is based on this `post <https://gis.stackexchange.com/questions/58923/calculate-view-angle>`_.

    :param target: GPS coordinates for the target point.
    :returns: The angles in the direction of the target, in radians. The vertical angle
              is in the range (0, pi), 0 is straight up and pi straight down.
              The horizontal angle is in the range (-pi/2, 3pi/2).
    """

    self_ecef = self.get_ecef()
    delta = self_ecef - target.get_ecef()
    delta_norm = la.norm(delta)

    vertical = np.acos(self_ecef.dot(delta) / (la.norm(self_ecef) * delta_norm))

    level_north = np.array(
        -self_ecef[0] * self_ecef[2],
        -self_ecef[1] * self_ecef[2],
        self_ecef[0] ** 2 + self_ecef[1] ** 2,
    )
    level_east = np.array(-self_ecef[1], self_ecef[0], 0.0)

    cos_azimuth = level_north.dot(delta) / (la.norm(level_north) * delta_norm)
    sin_azimuth = level_east.dot(delta) / (la.norm(level_east) * delta_norm)
    horizontal = np.atan(sin_azimuth / cos_azimuth)
    if self.lat < target.lat:
        horizontal += np.pi

    return AngularCoords(vertical, horizontal)


def get_ecef(self) -> np.ndarray:
    """ Get the ECEF (earth-centered, earth-fixed) coordinates of self (as described `here <https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates>`_).

    :returns: self in ECEF coordinates
    """
    n_phi = _prime_vertical_radius_of_curvature(self.lat)
    x = (n_phi + self.alt) * np.cos(self.lat) * np.cos(self.long)
    y = (n_phi + self.alt) * np.cos(self.lat) * np.sin(self.long)
    z = ((polar_radius ** 2 / equatorial_radius ** 2) * n_phi + self.alt) * np.sin(
        self.lat
    )
    return np.array([x, y, z])


def _prime_vertical_radius_of_curvature(phi: float) -> float:
    """ Helper for the ECEF function.

    :param phi: The angle for which to calculate the radius of curvature
    :returns: The prime vertical radius of curvature
    """
    return np.sqrt(
        1 - (1 - polar_radius ** 2 / equatorial_radius ** 2) * np.sin(phi) ** 2
    )
