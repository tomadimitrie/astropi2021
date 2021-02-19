from pathlib import Path

from PIL import Image
import numpy
import math


def compute_centroid(im_array, threshold=100):
    """
    Function that computes the centroid of an image (the centered area to start the computations from)
    :param im_array: the array of the image (ndarray)
    :param threshold: a value below which pixels are not considered for computing light directions (they are not "bright" enough)
    :return: the average middle of the centroid
    """

    valid = [point for point, value in numpy.ndenumerate(im_array) if value > threshold]
    xs = sum([point[0] for point in valid])
    ys = sum([point[1] for point in valid])
    tot = len(valid)
    return xs / tot, ys / tot


def compute_radius(im_array, centroid, threshold=100):
    """
    Function that computes the radius of the centroid
    :param im_array: the array of the image (ndarray)
    :param centroid: the previously computed centroid for the image (the pixel in the centre of the centroid)
    :param threshold: pixels with value below this centroid are not taken into consideration for computing the light directions
    :return: the radius of the centroid (float)
    """
    # here we compute the average distances between pixels which are bright enough and the centre of the centroid. The
    # distance between the pixel located the furthest and the central pixel is, in fact, the radius of the centroid
    distances = [
        math.sqrt((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2)  # Euclidean distance formula
        for point, value in numpy.ndenumerate(im_array)
        if value > threshold
    ]

    return max(0, *distances)


def compute_light_directions(image_file, mask_image_file):
    """
    Function that computes the light directions on coordinates for the given image file
    :param image_file: the input image
    :param mask_image_file: the mask for the image (pixels that should not be considered, in our case, the black margins
    of the photo)
    :return: the light coordinates, as a 3D list
    """
    # we eliminate the mask region from the photo
    mask_image = Image.open(mask_image_file)
    mask_image_gray = mask_image.convert("L")
    mask_image_array = numpy.asarray(mask_image_gray)
    mask_centroid = compute_centroid(mask_image_array)

    # we compute the radius of the mask
    mask_radius = compute_radius(mask_image_array, mask_centroid)

    image = Image.open(image_file)
    image_gray = image.convert("L")
    image_array = numpy.asarray(image_gray)

    # we compute the centroid of the given image (minus the masked region)
    centroid = compute_centroid(image_array)

    # we compute the small distances in both coordinates between the coordinates of the centre pixel of the mask image,
    # and the coordinates of the centre pixel of the actual image
    dx = centroid[1] - mask_centroid[1]
    dy = -(centroid[0] - mask_centroid[0])

    # we compute the list of light directions, relative to the calculated radius of the centroid
    n = numpy.array([
        dx / mask_radius,
        dy / mask_radius,
        math.sqrt(mask_radius * mask_radius - dx * dx - dy * dy) / mask_radius
    ])
    n *= n[2] * 2
    n[2] -= 1
    return n


def compute(file_path):
    """
    Function that returns the light directions for the image given at a certain path
    :param file_path: the path of the image to compute on
    :return: the light directions for the image located at that path
    """
    dir_path = Path(__file__).parent.resolve()
    return compute_light_directions(file_path, dir_path / "helper_images" / "lens_white.png").tolist()
