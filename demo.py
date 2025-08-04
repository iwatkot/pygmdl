import os
from time import perf_counter

import pygmdl

coordinates = (45.32, 20.21)
zoom = 18
output = "output.png"

tiles_dir = os.path.join(os.getcwd(), "temp_directory")
os.makedirs(tiles_dir, exist_ok=True)

start_time = perf_counter()
pygmdl.save_image(
    coordinates[0],
    coordinates[1],
    size=2048,
    output_path=output,
    rotation=0,
    zoom=zoom,
    from_center=True,
    tiles_dir=tiles_dir,
)
end_time = perf_counter()
print(f"Processed in {end_time - start_time:.2f} seconds")
