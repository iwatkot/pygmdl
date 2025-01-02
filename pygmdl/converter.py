"""This module contains functions for converting between different formats."""

import pyproj
from geopy.distance import distance  # type: ignore


def calc(lat: float, lon: float, rotation: int, size: int) -> tuple[list[float], list[float]]:
    """Return the boundary of the image as a list of longitudes and latitudes.

    Arguments:
        lat (float): Latitude of the center of the image.
        lon (float): Longitude of the center of the image.
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

    return lats, lons


def top_left_from_center(
    center_lat: float, center_lon_float, size: int, rotation: int
) -> tuple[float, float]:
    """Calculate the top left corner of the image from the center coordinates.

    Arguments:
        center_lat (float): Latitude of the center of the image.
        center_lon_float (float): Longitude of the center of the image.
        size (int): Size of the image.
        rotation (int): Rotation of the image.

    Returns:
        tuple: Tuple of latitude and longitude of the top left corner.
    """
    step_distance = size // 2
    top = distance(meters=step_distance).destination((center_lat, center_lon_float), 0 + rotation)
    top_coordinates = (top.latitude, top.longitude)
    top_left = distance(meters=step_distance).destination(top_coordinates, -90 + rotation)
    return top_left.latitude, top_left.longitude
