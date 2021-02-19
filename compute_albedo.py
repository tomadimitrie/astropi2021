from PIL import Image, ImageChops


def compute(file_path):
    """
    Function that compputes the albedo of a given image
    :param file_path: the path to the image
    :return: the albedo of the image
    """
    # we open the image and convert it to RGBA, adding max opacity (255) to all pixels
    image = Image.open(file_path)
    if image.mode == "RGB":
        image.putalpha(255)
    lens = Image.open("helper_images/lens_transparent.png")

    # we subtract the lens from the image (the black zone from margins)
    image = ImageChops.subtract(image, lens)

    width, height = image.size
    pixels = image.load()

    # list of albedo values for each pixel
    albedos = []

    for i in range(width):
        for j in range(height):
            r, g, b, a = pixels[i, j]
            if a == 0:
                continue
            luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b)
            albedos.append(luminance / 255 * 0.65) # 0.65 is the albedo value of a white sheet of paper, and we compute
            # the albedo relative to this

    # we return the average of albedos of pixels
    return sum(albedos) / len(albedos)
