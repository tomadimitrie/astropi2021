from PIL import Image

image = Image.open("image_round3.png")
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