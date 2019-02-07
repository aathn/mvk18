"""
This file contains functions for processing of coordinate data.
"""

import numpy as np
import numpy.linalg as la


def to_polar(camera, position: np.ndarray) -> (float, float):
    """ Compute the angle that the camera should face to capture a plane

    Based on a `draft <https://docs.google.com/document/d/1MtJNY73QoCYKpOv9H7nnySst_zIJB9eUzAs19oHi3uQ)>`_ by Theo Puranen Åhfeldt.

    :param camera: object recording the location of the camera (tentative)
    :param position: 1 x 3 numpy array or list [latitude, longitude, altitude]
    :returns: horizontal and vertical angles for the camera to face

    """
    if not isinstance(np.ndarray, position):
        try:
            position = np.array(position)
        except:
            raise TypeError("Input must be in np array compatible format!")
    if not position.shape[0] == 3:
        raise ValueError("Expected position as [lat, long, alt]!")

    delta = position - camera.position  # delta = [dx, dy, dz]
    flat_distance = la.norm(delta[:-1])

    hrs_angle = np.pi / 2
    if delta[0] != 0:
        hrs_angle = np.arctan(delta[1] / delta[0])
        if delta[0] < 0:
            hrs_angle += np.pi
    elif delta[1] < 0:
        hrs_angle = -np.pi / 2

    vrt_angle = np.pi / 2
    if delta[1] != 0:
        vrt_angle = np.arctan(delta[2] / flat_distance)
    elif delta[2] < 0:
        vrt_angle = -np.pi / 2

    return (hrs_angle, vrt_angle)
