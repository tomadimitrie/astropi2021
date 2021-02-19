from PIL import Image, ImageChops

image = Image.open("output_albedo.png").convert("RGBA")
lens = Image.open("lens.png")

image = ImageChops.subtract(image, lens)

width, height = image.size
pixels = image.load()

albedos = []

for i in range(width):
    for j in range(height):
        r, g, b, a = pixels[i, j]
        if a == 0:
            continue
        luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b)
        albedos.append(luminance / 255 * 0.65)

avg = sum(albedos) / len(albedos)
print(avg)


# import compute_light_directions
#
# compute_light_directions.compute()

# import simple_photometric_stereo
# simple_photometric_stereo.compute()