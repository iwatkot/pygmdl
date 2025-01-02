"""This module contains conversion functions for latitude and longitude to pixel and tile
coordinates."""

import math


def latlon2px(zoom: int, lat: float, lon: float) -> tuple[int, int]:
    """Converts latitude and longitude to pixel coordinates.

    Arguments:
        zoom (int): Zoom level.
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        tuple: Tuple of pixel coordinates.
    """
    x = 2**zoom * (lon + 180) / 360 * 256
    y = (
        -(
            0.5
            * math.log((1 + math.sin(math.radians(lat))) / (1 - math.sin(math.radians(lat))))
            / math.pi
            - 1
        )
        * 256
        * 2 ** (zoom - 1)
    )
    return x, y


def latlon2xy(zoom: int, lat: float, lon: float) -> tuple[int, int, int, int]:
    """Converts latitude and longitude to tile coordinates.

    Arguments:
        zoom (int): Zoom level.
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        tuple: Tuple of tile coordinates.
    """
    x, y = latlon2px(zoom, lat, lon)

    remain_x = int(x % 256)
    remain_y = int(y % 256)

    x = int(x / 256)
    y = int(y / 256)

    return x, y, remain_x, remain_y
