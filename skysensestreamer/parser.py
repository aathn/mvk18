"""
This function parses JSON flight data to and returns the data as python dictionaries.
"""
import json
from typing import Dict, List
from enum import IntEnum
from os import stat
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.camera import Camera, Airplane
from threading import Condition


class DataIndices(IntEnum):
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
    new_coord = GPSCoord(
        data[DataIndices.LAT], data[DataIndices.LONG], data[DataIndices.ALT]
    )
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


def keep_planes_updated(
    camera: Camera, source_file: str, update_interval: int, cond: Condition
):
    """Updates the planes in camera class when new information is available
    
    Start this using something like:
    :code:`p = threading.Thread(target = keep_planes_updated, args = (camera, source_file, 1.0, cond))`

    End the thread using :code:`cond.notify()`, after acquiring `cond`.

    :param camera: Camera class that stores the plane information
    :param source_file: A file with JSON airplane data
    :param update_interval: The time between checking the status of the file
    :param cond: A Condition used to exclusively access camera and determine when to stop looping

    """
    modified_time = 0
    with cond:
        while True:
            new_time = stat(source_file).st_mtime
            if new_time != modified_time:
                modified_time = new_time
                update_airplanes(camera, source_file)
            if cond.wait(update_interval):
                break