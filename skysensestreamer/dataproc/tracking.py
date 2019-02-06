""" tracking.py

Denna fil är del av projektet fr24/mvk18.
Skapad 2019-02-06 av Anders Ågren Thuné.
Uppdaterad 2019-02-06 av Anders Ågren Thuné.

Den här filen innehåller funktioner för styrning av hur kameran ska prioritera
flygplan, hantering av sikt och extrapolering av flygplanspositioner.

Eventuellt bör vi göra en klass som har en lista med flygplan inom räckvidd
och som håller koll på extrapolerade positioner och synlighetsstatus för varje.
"""

import numpy as np
import numpy.linalg as la

def extrapolate (positions, times):
    """
    En funktion som tar en uppsättning av tidigare positioner och tider och
    producerar en funktion av tiden som returnerar en extrapolerad position.

    positions: n x 3 array med positionsdata
    times: n x 1 array med tider
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
        np.hstack([times, ones(len(times))]), positions, rcond = None)[0]
    return lambda t: intercept + t*direction
