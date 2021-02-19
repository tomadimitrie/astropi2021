from PIL import Image, ImageChops


def compute(file_path):
    image = Image.open(file_path)
    if image.mode == "RGB":
        image.putalpha(255)
    lens = Image.open("helper_images/lens_transparent.png")

    image = ImageChops.subtract(image, lens)
    image.show()

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

    return sum(albedos) / len(albedos)
