""" coords.py

This file is part of the project fr24/mvk18.
Created 2019-02-06 by Anders Ågren Thuné.
Last updated 2019-02-06 by Anders Ågren Thuné.

This file contains functions for processing of coordinate data.
"""

import numpy as np
import numpy.linalg as la


def to_polar(camera, position):
    """
    to_polar(camera, position)

    camera: object recording the location of the camera (tentative)
    position: 3 x 1 numpy array or list [latitude, longitude, altitude]

    Computes the angles that the camera should face in order to capture an
    airplane at the given position.

    Code written by Anders Ågren Thuné based on a draft by Theo Puranen Åhfeldt.
    (https://docs.google.com/document/d/1MtJNY73QoCYKpOv9H7nnySst_zIJB9eUzAs19oHi3uQ)
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
