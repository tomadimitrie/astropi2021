from PIL import Image
import numpy
import math


def compute_centroid(im_array, threshold=100):
    valid = [point for point, value in numpy.ndenumerate(im_array) if value > threshold]
    xs = sum([point[0] for point in valid])
    ys = sum([point[1] for point in valid])
    tot = len(valid)
    return xs / tot, ys / tot


def compute_radius(im_array, centroid, threshold=100):
    distances = [
        math.sqrt((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2)
        for point, value in numpy.ndenumerate(im_array)
        if value > threshold
    ]

    return max(0, *distances)


def compute_light_directions(image_file, mask_image_file):
    mask_image = Image.open(mask_image_file)
    mask_image_gray = mask_image.convert("L")
    mask_image_array = numpy.asarray(mask_image_gray)
    mask_centroid = compute_centroid(mask_image_array)
    mask_radius = compute_radius(mask_image_array, mask_centroid)

    image = Image.open(image_file)
    image_gray = image.convert("L")
    image_array = numpy.asarray(image_gray)
    centroid = compute_centroid(image_array)

    dx = centroid[1] - mask_centroid[1]
    dy = -(centroid[0] - mask_centroid[0])

    n = numpy.array([
        dx / mask_radius,
        dy / mask_radius,
        math.sqrt(mask_radius * mask_radius - dx * dx - dy * dy) / mask_radius
    ])
    n *= n[2] * 2
    n[2] -= 1
    return n


def compute():
    light_directions = compute_light_directions("image.jpg", "lens_white.png")

    with open('output.txt', 'w') as output_file:
        output_file.write('%lf %lf %lf\n' % (light_directions[0], light_directions[1], light_directions[2]))
