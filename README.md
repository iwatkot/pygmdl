<p align="center">
<a href="https://github.com/iwatkot/maps4fs">maps4fs</a> •
<a href="https://github.com/iwatkot/maps4fsui">maps4fs UI</a> •
<a href="https://github.com/iwatkot/maps4fsapi">maps4fs API</a> •
<a href="https://github.com/iwatkot/maps4fsstats">maps4fs Stats</a> •
<a href="https://github.com/iwatkot/maps4fsbot">maps4fs Bot</a><br>
<a href="https://github.com/iwatkot/pygmdl">pygmdl</a> •
<a href="https://github.com/iwatkot/pydtmdl">pydtmdl</a>
</p>

<div align="center" markdown>
<img src="https://github.com/user-attachments/assets/4ecd8574-6fbd-4541-bb3b-17767df410dd">
</a>

<p align="center">
  <a href="#Quick-Start">Quick Start</a> •
  <a href="#Overview">Overview</a> • 
  <a href="How-to-Use">How to Use</a> •
  <a href="Bugs-and-Feature-Requests">Bugs and Feature Requests</a>
</p>

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/iwatkot/pygmdl)](https://github.com/iwatkot/pygmdl/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/pygmdl)](https://pypi.org/project/pygmdl)
[![GitHub issues](https://img.shields.io/github/issues/iwatkot/pygmdl)](https://github.com/iwatkot/pygmdl/issues)
[![Maintainability](https://api.codeclimate.com/v1/badges/373eb79586deebf5c264/maintainability)](https://codeclimate.com/github/iwatkot/pygmdl/maintainability)<br>
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pygmdl)](https://pypi.org/project/pygmdl)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Build Status](https://github.com/iwatkot/pygmdl/actions/workflows/checks.yml/badge.svg)](https://github.com/iwatkot/pygmdl/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/373eb79586deebf5c264/test_coverage)](https://codeclimate.com/github/iwatkot/pygmdl/test_coverage)
[![GitHub Repo stars](https://img.shields.io/github/stars/iwatkot/pygmdl)](https://github.com/iwatkot/pygmdl/stargazers)<br>

</div>

## Quick Start
1. Install the package via pip:

```bash
pip install pygmdl
```

2. Import the package and use it:

```python
import pygmdl

lat = 35.681236
lon = 139.767125
size = 2000
output_path = "satellite_image.png"

pygmdl.save_image(lat, lon, size, output_path)
```

It will took a while to download the image, but as soon as it's done, you will see the image in the specified path.

## Overview

This package is designed to download satellite images from Google Maps in a simple way. This repository is a fork of [satmap_downloader](https://github.com/Paint-a-Farm/satmap_downloader), which provides CLI to download satellite images. So if you need a CLI tool, please use the original repository.

## How to Use

Here, you'll find the detailed explanation of the `save_image` function.

### Function signature

```python
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
```

Note, that by default the function expects that provided coordinates (lat, lon) are coordinates of the top-left corner of the image. If you want to provide the coordinates of the center of the image, you can set `from_center` to `True`.

### Function arguments

|      Parameters      |              Type              |                    Description                     |
| :------------------: | :----------------------------: | :------------------------------------------------: |
|         lat          |            float             | Latitude of the point to download the image from. |
|         lon          |            float             | Longitude of the point to download the image from.|
|         size         |            int               | Size of the ROI in meters.                     |
|     output_path      |            str               | Path to save the image.                           |
|      rotation        |            int               | Rotation of the image in degrees (CW).            |
|         zoom         |            int               | Zoom level for images (higher values = higher resolution). |
|     from_center      |            bool              | If True, the provided coordinates will be treated as the center of the image. |
|       logger         | Logger \| None | Logger to use for logging. If None, the default logger will be used. |

### Return value
The function returns the path to the saved image (the same as `output_path`).

### Usage example

```python
import pygmdl

lat = 35.681236
lon = 139.767125
size = 2000
output_path = "satellite_image.png"
rotation = 25
zoom = 16
from_center = True

pygmdl.save_image(lat, lon, size, output_path, rotation, zoom, from_center)
```

As a result, you will get the satellite image of a region 2000x2000 meters around the point with coordinates (35.681236, 139.767125) with the center of the image at these coordinates. The image will be rotated by 25 degrees clockwise and will be downloaded with zoom level 16.

## Bugs and Feature Requests

If you find a bug or have a feature request, please open an issue on the [issues](https://github.com/iwatkot/pygmdl/issues) page.
