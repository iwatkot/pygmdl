import os
from random import choice, randint

from PIL import Image

import pygmdl

coordinate_cases = [(45.32, 20.21), (45.27, 19.60), (45.24, 16.95)]
size_cases = [512, 1024, 2048]
zoom_cases = [12, 14, 16]

output_path = "tests/test.png"


def test_save_image():
    for coordinate_case in coordinate_cases:
        for size in size_cases:
            for zoom in zoom_cases:
                rotation = randint(0, 90)

                lat, lon = coordinate_case
                from_center = choice([True, False])

                pygmdl.save_image(
                    lat,
                    lon,
                    size=size,
                    output_path=output_path,
                    rotation=rotation,
                    zoom=zoom,
                    from_center=from_center,
                )

                assert os.path.isfile(output_path), "Can't find the output file."

                # Read the image using PIL and check if it's valid.
                Image.open(output_path)

                try:
                    os.remove(output_path)
                except Exception:
                    pass
