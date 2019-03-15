"""
This file contains functions for processing of coordinate data.
"""

from __future__ import annotations
import numpy as np
import numpy.linalg as la


# The radii of the Earth's major and minor axes, in feet
equatorial_radius = 20925646.3
polar_radius = 20855486.5


class LocalCoord:
    def __init__(self, azimuth, altitude_angle, distance):
        self.azimuth = azimuth
        """The angle in radians one should turn clockwise from north, to face the object"""
        self.altitude_angle = altitude_angle
        """The angle in radians one should look down from straight up, to face the object"""
        self.distance = distance

    @property
    def azimuth(self):
        return self.__azimuth

    @azimuth.setter
    def azimuth(self, azimuth):
        """Formats equivalent angles to be in the range 0-2π"""
        self.__azimuth = azimuth % (2 * np.pi)

    @property
    def altitude_angle(self):
        return self.__altitude_angle

    @altitude_angle.setter
    def altitude_angle(self, altitude_angle):
        """Sets altitude_angle to the nearest angle in the range 0-π"""
        if altitude_angle < 0:
            self.__altitude_angle = 0
        elif altitude_angle > np.pi:
            self.__altitude_angle = np.pi
        else:
            self.__altitude_angle = altitude_angle

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, distance):
        """Sets distance to be an absolute value (always positive)"""
        self.__distance = np.abs(distance)


class GPSCoord:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __eq__(self, other: GPSCoord):
        return (
            self.latitude == other.latitude
            and self.longitude == other.longitude
            and self.altitude == other.altitude
        )

    def __ne__(self, other: GPSCoord):
        return not self.__eq__(other)

    def __repr__(self):
        return "GPSCoord({}, {}, {})".format(
            self.latitude, self.longitude, self.altitude
        )

    def to_local(self, target: GPSCoord) -> LocalCoord:
        """Calculate the angles and distance from self to target.

        The implementation is based on this `post <https://gis.stackexchange.com/questions/58923/calculate-view-angle>`_, with modifications for the azimuth calculation.

        :param target: GPS coordinates for the target point.
        :returns: The angles in radians and distance in feet. The vertical angle
                  is in the range (0, pi), 0 is straight up and pi straight down.
                  The horizontal angle is in the range (-pi/2, 3pi/2), going from
                  west to west in clockwise direction.
        """

        self_ecef = self.get_ecef()
        delta = target.get_ecef() - self_ecef
        delta_norm = la.norm(delta)

        vertical = np.arccos(self_ecef.dot(delta) / (la.norm(self_ecef) * delta_norm))

        level_north = np.array(
            [
                -self_ecef[0] * self_ecef[2],
                -self_ecef[1] * self_ecef[2],
                self_ecef[0] ** 2 + self_ecef[1] ** 2,
            ]
        )
        level_east = np.array([-self_ecef[1], self_ecef[0], 0.0])

        north_proj = level_north.dot(delta) / la.norm(level_north)
        east_proj = level_east.dot(delta) / la.norm(level_east)
        if np.isclose(north_proj, 0):
            horizontal = np.pi / 2
        else:
            horizontal = np.arctan(east_proj / north_proj)

        if self.latitude > target.latitude:
            horizontal += np.pi

        return LocalCoord(horizontal, vertical, delta_norm)

    def get_ecef(self) -> np.ndarray:
        """Get the ECEF (earth-centered, earth-fixed) coordinates of self (as described `here <https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates>`_).

        :returns: self in ECEF coordinates
        """
        radian_lat = self.latitude * np.pi / 180
        radian_long = self.longitude * np.pi / 180
        radian_alt = self.altitude * np.pi / 180

        n_phi = _prime_vertical_radius_of_curvature(radian_lat)
        x = (n_phi + radian_alt) * np.cos(radian_lat) * np.cos(radian_long)
        y = (n_phi + radian_alt) * np.cos(radian_lat) * np.sin(radian_long)
        z = (
            (polar_radius ** 2 / equatorial_radius ** 2) * n_phi + radian_alt
        ) * np.sin(radian_lat)
        return np.array([x, y, z])


def _prime_vertical_radius_of_curvature(phi: float) -> float:
    """Helper for the ECEF function.

    :param phi: The angle for which to calculate the radius of curvature
    :returns: The prime vertical radius of curvature
    """
    return equatorial_radius / np.sqrt(
        1 - (1 - polar_radius ** 2 / equatorial_radius ** 2) * np.sin(phi) ** 2
    )
