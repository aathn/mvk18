"""
This function parses JSON flight data to and returns the data as python dictionaries.
"""
import json

def data_parser(source_file: str) -> dict:
    """
    Parses the string from the file specified stripping the text before and after actual JSON data. Returns a dict with the data in the file.

    param source_file: The file from which to read the the JSON data.
    returns: A python dictionary in the same format as the JSON data with
             the same key and data.
    """
    with open(source_file, "r") as file:
        stripped = file.read().strip("fr24_callback();")
        data = json.loads(stripped)
    return data
