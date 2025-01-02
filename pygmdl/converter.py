"""This module contains functions for converting between different formats."""

import pyproj


def calc(lon: float, lat: float, rotation: int, size: int) -> tuple[list[float], list[float]]:
    """Return the boundary of the image as a list of longitudes and latitudes.

    Arguments:
        lon (float): Longitude of the center of the image.
        lat (float): Latitude of the center of the image.
        rotation (int): Rotation of the image.
        size (int): Size of the image.

    Returns:
        tuple: Tuple of lists of longitudes and latitudes.
    """
    toprightlon, toprightlat, _ = pyproj.Geod(ellps="WGS84").fwd(lon, lat, 90 + rotation, size)
    bottomrightlon, bottomrightlat, _ = pyproj.Geod(ellps="WGS84").fwd(
        toprightlon, toprightlat, 180 + rotation, size
    )
    bottomleftlon, bottomleftlat, _ = pyproj.Geod(ellps="WGS84").fwd(
        bottomrightlon, bottomrightlat, 270 + rotation, size
    )

    lons = [lon, toprightlon, bottomrightlon, bottomleftlon]
    lats = [lat, toprightlat, bottomrightlat, bottomleftlat]

    return lons, lats
