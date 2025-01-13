"""This module contains functions to download and merge tiles from Google Maps."""

import concurrent.futures
import math
import os
import random
import time
import urllib.request
from math import cos, sin

from PIL import Image
from tqdm import tqdm

from pygmdl.config import HEADERS, SAT_URL, TILES_DIRECTORY, Logger
from pygmdl.converter import calc, top_left_from_center
from pygmdl.gmapper import latlon2xy

Image.MAX_IMAGE_PIXELS = None


def download_tile(
    x: int,
    y: int,
    zoom: int,
    logger: Logger,
    pbar: tqdm,
) -> None:
    """Download an individual tile for a given x, y, and zoom level.

    Args:
        x (int): X coordinate of the tile.
        y (int): Y coordinate of the tile.
        zoom (int): Zoom level of the tile.
        logger (Logger): Logger object.
        pbar (tqdm): Progress bar object.
    """
    url = SAT_URL % (x, y, zoom)
    tile_name = f"{zoom}_{x}_{y}_s.png"

    tile_path = os.path.join(TILES_DIRECTORY, tile_name)

    if not os.path.exists(tile_path):
        try:
            req = urllib.request.Request(url, data=None, headers=HEADERS)
            response = urllib.request.urlopen(req)  # pylint: disable=R1732
            data = response.read()
        except Exception as e:
            logger.error(f"Error downloading {tile_path}: {e}")
            raise RuntimeError(f"Error downloading {tile_path}: {e}")  # pylint: disable=W0707

        if data.startswith(b"<html>"):
            logger.error(f"Error downloading {tile_path}: Forbidden")
            raise RuntimeError(f"Error downloading {tile_path}: Forbidden")

        with open(tile_path, "wb") as f:
            f.write(data)

        time.sleep(random.random())

    pbar.update(1)


# pylint: disable=R0913, R0917
def download_tiles(
    lat_start: float,
    lat_stop: float,
    lon_start: float,
    lon_stop: float,
    zoom: int,
    logger: Logger,
) -> None:
    """Download tiles for a given boundary.

    Arguments:
        lat_start (float): Latitude of the top-left corner.
        lat_stop (float): Latitude of the bottom-right corner.
        lon_start (float): Longitude of the top-left corner.
        lon_stop (float): Longitude of the bottom-right corner.
        zoom (int): Zoom level.
        logger (Logger): Logger object.
    """
    start_x, start_y, _, _ = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y, _, _ = latlon2xy(zoom, lat_stop, lon_stop)
    number_of_tiles = (stop_y - start_y + 1) * (stop_x - start_x + 1)

    logger.info("Starting to download %s tiles...", number_of_tiles)

    with tqdm(total=number_of_tiles, desc="Downloading tiles", unit="tiles") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for x in range(start_x, stop_x + 1):
                for y in range(start_y, stop_y + 1):
                    executor.submit(download_tile, x, y, zoom, logger, pbar)


# pylint: disable=R0914, R0917, R0913
def merge_tiles(
    lat_start: float,
    lat_stop: float,
    lon_start: float,
    lon_stop: float,
    rotation: int,
    output: str,
    zoom: int,
    logger: Logger,
):
    """Merge downloaded tiles into a single image.

    Arguments:
        lat_start (float): Latitude of the top-left corner.
        lat_stop (float): Latitude of the bottom-right corner.
        lon_start (float): Longitude of the top-left corner.
        lon_stop (float): Longitude of the bottom-right corner.
        rotation (int): Rotation of the image.
        output (str): Output path.
        zoom (int): Zoom level.
        logger (Logger): Logger object.
    """
    tile_type, ext = "s", "png"

    x_start, y_start, remain_x_start, remain_y_start = latlon2xy(zoom, lat_start, lon_start)
    x_stop, y_stop, remain_x_stop, remain_y_stop = latlon2xy(zoom, lat_stop, lon_stop)

    w = (x_stop + 1 - x_start) * 256
    h = (y_stop + 1 - y_start) * 256

    result = Image.new("RGB", (w, h))

    number_of_tiles = (y_stop - y_start + 1) * (x_stop - x_start + 1)

    with tqdm(total=number_of_tiles, desc="Merging tiles", unit="tiles") as pbar:
        for x in range(x_start, x_stop + 1):
            for y in range(y_start, y_stop + 1):
                tile_name = f"{zoom}_{x}_{y}_{tile_type}.{ext}"
                tile_path = os.path.join(TILES_DIRECTORY, tile_name)

                if not os.path.exists(tile_path):
                    logger.warning(f"Tile {tile_path} not found, skipping...")
                    continue

                x_paste = (x - x_start) * 256
                y_paste = h - (y_stop + 1 - y) * 256

                try:
                    image = Image.open(tile_path)
                except Exception as e:  # pylint: disable=W0718
                    logger.error(f"Error opening {tile_path}: {e}")
                    try:
                        os.remove(tile_path)
                    except Exception:  # pylint: disable=W0718
                        pass
                    continue

                result.paste(image, (x_paste, y_paste))

                pbar.update(1)

    cropped = result.crop(
        (remain_x_start, remain_y_start, w - (256 - remain_x_stop), h - (256 - remain_y_stop))
    )
    rotated = cropped.rotate(rotation, expand=False)
    new_width = 1 * cos(math.radians(abs(rotation))) + 1 * sin(math.radians(abs(rotation)))

    ratio = 1 / new_width

    box = (
        int((rotated.width - ratio * rotated.width) / 2),
        int((rotated.height - ratio * rotated.height) / 2),
        int(rotated.width - (rotated.width - ratio * rotated.width) / 2),
        int(rotated.height - (rotated.height - ratio * rotated.height) / 2),
    )

    cropped2 = rotated.crop(box)
    cropped2 = cropped2.resize(
        (int(min(cropped2.width, cropped2.height)), int(min(cropped2.width, cropped2.height)))
    )

    logger.info("Shape of the image: %s", cropped2.size)

    cropped2.save(output)
    logger.info("Saved image as %s", output)


def save_image(
    lat: float,
    lon: float,
    size: int,
    output_path: str,
    rotation: int = 0,
    zoom: int = 18,
    from_center: bool = False,
    logger: Logger | None = None,
) -> str:
    """Save an image from a given coordinates, size, and rotation.
    By default function expects that the input coordinates are the top-left corner of the image.
    If you need to provide the center of the image, set from_center to True.

    Arguments:
        lat (float): Latitude of the top-left corner.
        lon (float): Longitude of the top-left corner.
        size (int): Size of the image.
        output_path {str}: Output path.
        rotation (int, optional): Rotation of the image. Defaults to 0.
        zoom (int, optional): Zoom level. Defaults to 18.
        from_center (bool, optional): If set to True, function expects that the input coordinates
            are the center of the image. Defaults to False.
        logger (Logger, optional): Logger object.

    Returns:
        str: Output path.
    """
    if logger is None:
        logger = Logger()

    if from_center:
        lat, lon = top_left_from_center(lat, lon, size, rotation)

    lats, lons = calc(lat, lon, rotation, size)
    logger.info("Boundary coordinates: %s %s", lats, lons)

    download_tiles(max(lats), min(lats), min(lons), max(lons), zoom, logger)
    logger.info("Satellite tiles downloaded, starting to merge...")

    merge_tiles(
        max(lats),
        min(lats),
        min(lons),
        max(lons),
        rotation,
        output_path,
        zoom,
        logger,
    )
    logger.info("Image merged successfully to %s", output_path)
    return output_path
