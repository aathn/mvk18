""" coords.py

Denna fil är del av projektet fr24/mvk18.
Skapad 2019-02-06 av Anders Ågren Thuné.
Uppdaterad 2019-02-06 av Anders Ågren Thuné.

Den här filen innehåller funktioner för bearbetning av koordinatdata.
"""

import numpy as np
import numpy.linalg as la

def to_polar (position):
    """
    En funktion för att omvandla ett flygplans position till den vinkel som kameran
    ska riktas åt för att filma planet.

    Positioner ges av tredimensionella vektorer: (latitud, longitud, altitud).
    Om vi har positionen för skysense/kameran och ett flygplan, kan vi beräkna
    den horisontella och vertikala vinkeln kameran behöver vrida sig (polära
    koordinater). En naiv men förhoppningsvis fungerande lösning är att först
    räkna ut en cartesian vektor som pekar från kamera till flygplanet, genom
    att subtrahera kamerans positionsvektor från flyplanets.

    Med våra nya polära koordinater relativa till kameran, bör det vara enkelt att
    flytta servon i rätt riktning. Förutsatt att servon står plant och inte lutar,
    krävs det bara att översätta horisontella vinkeln relativt servons
    utgångsvinkel, vilket görs genom att subtrahera utgångsvinkeln till resultatet.

    Kod skriven av Anders Ågren Thuné baserad på utkast av
    Theo Puranen Åhfeldt.

    """

    if not isinstance(np.ndarray, position):
        raise TypeError("Expected position as np array [lat, long, alt]!")
    if not position.shape[0] == 3:
        raise ValueError("Expected position as np array [lat, long, alt]!")

    delta = position - camera.position # delta = [dx, dy, dz]
    flat_distance = la.norm(delta[0:2])

    hrs_angle = np.pi/2
    if delta[0] != 0:
        hrs_angle = np.arctan(delta[1]/delta[0])
        if  delta[0] < 0:
            hrs_angle += np.pi
    elif delta[1] < 0:
        hrs_angle = -np.pi/2

    vrt_angle = np.pi/2
    if delta[1] != 0:
        vrt_angle = np.arctan(delta[2]/flat_distance)
    elif delta[2] < 0:
        vrt_angle = -np.pi/2

    return (hrs_angle, vrt_angle)
