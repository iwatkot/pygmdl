from time import perf_counter

import pygmdl

coordinates = (45.32, 20.21)
zoom = 18
output = "output.png"

start_time = perf_counter()
pygmdl.save_image(
    coordinates[0],
    coordinates[1],
    size=2048,
    output_path=output,
    rotation=0,
    zoom=zoom,
    from_center=True,
)
end_time = perf_counter()
print(f"Processed in {end_time - start_time:.2f} seconds")
