import pygmdl

coordinates = (45.32, 20.21)
zoom = 16
output = "output.png"

pygmdl.save_image(
    coordinates[0],
    coordinates[1],
    size=2048,
    output_path=output,
    rotation=0,
    zoom=zoom,
    from_center=True,
)
