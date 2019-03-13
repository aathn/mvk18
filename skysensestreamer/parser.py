"""
This function parses JSON flight data to and returns the data as python dictionaries.
"""
import json
from typing import Dict, List
from enum import Enum
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.camera import Camera, Airplane


class DataIndices(Enum):
    LAT = 1
    LONG = 2
    ALT = 4
    TIME = 10


def parse(source_file: str) -> Dict:
    """
    Parses the string from the file specified stripping the text before and
    after actual JSON data. Returns a dict with the data in the file.

    :param source_file: The file from which to read the the JSON data.
    :returns: A python dictionary in the same format as the JSON data with
              the same key and data.
    """
    with open(source_file, "r") as file:
        stripped = file.read().strip("fr24_callback();")
    data = json.loads(stripped)
    return data


def append_pos_to_plane(data: List, plane: Airplane):
    """Append a position to a plane using raw data

    :param data: Raw flight data, as received from `parse`
    :param plane: A plane to add the position to

    """
    new_coord = GPSCoord(data[DataIndices.LAT, DataIndices.LONG, DataIndices.ALT])
    plane.append_position(data[DataIndices.TIME], new_coord)


def update_airplanes(camera: Camera, source_file: str):
    new_data = parse(source_file)
    new_planes = []
    for plane in camera.airplanes:
        if plane.id in new_data:
            append_pos_to_plane(new_data[plane.id], plane)
            del new_data[plane.id]
            new_planes.append(plane)

    for plane_id in new_data:
        new_plane = Airplane(plane_id)
        append_pos_to_plane(new_data[plane_id], new_plane)
        new_planes.append(new_plane)

    camera.airplanes = new_planes
