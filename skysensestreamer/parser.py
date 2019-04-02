"""
This function parses JSON flight data to and returns the data as python dictionaries.
"""
import json
from typing import Dict, List
from enum import IntEnum
from os import stat
from skysensestreamer.dataproc.coords import GPSCoord
from skysensestreamer.camera import Camera, Airplane
from threading import Event, Lock
from time import sleep


class DataIndices(IntEnum):
    """Enumeration for elements in JSON data"""

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


def parseGPSCoord(source_file: str) -> GPSCoord:
    """Parses GPS positions from file

    :param source_file: The file with the GPS data.
    :return: A GPSCoord object.
    """
    with open(source_file, "r") as file:
        pos = [float(coord) for coord in file.readline().split(",")]
    return GPSCoord(pos[0], pos[1], pos[2])


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
    """Update a camera's airplane list
    
    Replaces the current airplane list with an updated one based on
    source_file. Airplanes not present in source_file are
    removed. Airplanes present in source_file but not the existing
    list are created and added to the new list. Existing airplanes
    present in the source file are updated and added to the new list.
    
    :param camera: The Camera object to be updated
    :param source_file: Source file to read data from

    """
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
    camera: Camera, source_file: str, update_interval: int, stop_flag: Event
):
    """Updates the planes in camera class when new information is available
    
    Start this using something like:
    :code:`p = threading.Thread(target = keep_planes_updated, args = (camera, source_file, 1.0, stop_flag))`

    End the thread using :code:`stop_flag.set()`.

    :param camera: Camera class that stores the plane information
    :param source_file: A file with JSON airplane data
    :param update_interval: The time between checking the status of the file
    :param stop_flag: An Event used to determine when to stop looping

    """
    modified_time = 0
    while not stop_flag.is_set():
        new_time = stat(source_file).st_mtime
        if new_time != modified_time:
            modified_time = new_time
            print("updating airplane list")
            update_airplanes(camera, source_file)
        sleep(update_interval)
