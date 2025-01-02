import os
from random import choice, randint

import pygmdl

coordinate_cases = [(45.32, 20.21), (45.27, 19.60), (45.24, 16.95)]
size_cases = [512, 1024, 2048]
zoom_cases = [12, 14, 16]

output_filename = "tests/test.png"


def test_save_image():
    for coordinate_case in coordinate_cases:
        size = choice(size_cases)
        zoom = choice(zoom_cases)
        rotation = randint(0, 90)

        lat, lon = coordinate_case

        pygmdl.save_image(lat, lon, rotation, size, output_filename, zoom=zoom)

        assert os.path.isfile(output_filename), "Can't find the output file."

        try:
            os.remove(output_filename)
        except Exception:
            pass
