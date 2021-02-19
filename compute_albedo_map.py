from pathlib import Path

import numpy as np
from PIL import Image
from scipy import linalg


def compute_normals(light_matrix, mask_array, image_array, threshold=100):
    """
    Function that computes an narray of the normals (a list of directions of the light for each pixel), given a light
    matrix
    :param light_matrix: the previously computed light directions array
    :param mask_array: the ndarray of the mask image
    :param image_array: the ndarray of the actual image
    :param threshold: below this value, the pixels are not taken into consideration for further computations (they are
    not bright enough to be changed)
    :return: the normal map (ndarray)
    """
    shaper = (mask_array.shape[0], mask_array.shape[1], 3)

    # we initialize the normal map ndarray with zeros
    normal_map = np.zeros(shaper)
    ivec = np.zeros(1)

    for (xT, value) in np.ndenumerate(mask_array):
        if value > threshold:
            # we add to ivec the value of that pixel
            ivec[0] = image_array[xT[0], xT[1]]

            # we calculate the vector which, multiplied by the light matrix value, gives us the ivec value (least
            # squares solution). This is, in fact, giving us an unoptimized value of the normal
            (normal, res, rank, s) = linalg.lstsq(light_matrix, ivec)

            # we optimize the normal value by its normalized form
            normal /= linalg.norm(normal)

            # tests whether the sum of normals is a number or not. If it is not, we do not add it to the normal map
            if not np.isnan(np.sum(normal)):
                normal_map[xT] = normal

    return normal_map


def compute_albedo(light_matrix, mask_array, image_array, normal_map, threshold=100):
    """
    Function that computes the albedo map of an image
    :param light_matrix: the previously computed light directions array
    :param mask_array: the ndarray of the mask image
    :param image_array: the ndarray of the actual image
    :param normal_map: the previously computed normal map of :param normal_map (ndarray)
    :param threshold: below this value, the pixels are not taken into consideration for further computations (they are
    not bright enough to be changed)
    :return: the albedo image of the image (ndarray)
    """
    shaper = (mask_array.shape[0], mask_array.shape[1], 3)

    # we initialize the albedo map ndarray with zeros
    albedo_map = np.zeros(shaper)
    ivec = np.zeros((1, 3))

    for (xT, value) in np.ndenumerate(mask_array):
        if value > threshold:
            # we add to ivec the value of that pixel
            ivec[0] = image_array[xT[0], xT[1]]

            # we compute the dot product between the light matrix and the normal map at pixel xT
            i_t = np.dot(light_matrix, normal_map[xT])

            # k is the actual optimized value of the pixel xT (light directions are optimized, for an albedo map output)
            k = np.dot(np.transpose(ivec), i_t) / (np.dot(i_t, i_t))

            # tests whether the sum of pixel values is a number or not. If it is not, we do not add it to the albedo map
            if not np.isnan(np.sum(k)):
                albedo_map[xT] = k

    return albedo_map


def simple_photometric_stereo(image_file, mask_image_file, light_directions):
    """
    Function that returns the normal and albedo map of a given image
    :param image_file: the actual image
    :param mask_image_file: the mask image
    :param light_directions: light directions array of the image (previously computed)
    :return: the normal and albedo map of the image
    """
    lights = [light_directions]
    # we mask the given image (eliminate the pixels within the mask)
    mask_image = Image.open(mask_image_file)
    mask_image_gray = mask_image.convert("L")
    mask_image_array = np.asarray(mask_image_gray)

    # we convert images to ndarrays
    image = Image.open(image_file).convert("RGB")
    image_array = np.asarray(image)
    image_gray = image.convert("L")
    image_gray_array = np.asarray(image_gray)

    # we compute the normal and albedo maps
    normal_map = compute_normals(np.array(lights), mask_image_array, image_gray_array)
    albedo_map = compute_albedo(np.array(lights), mask_image_array, image_array, normal_map)

    return normal_map, albedo_map


def compute(file_path, light_directions):
    """
    Function that saves the normal and albedo maps of an image
    :param file_path: the path to the image to compute on
    :param light_directions: the light directions for that image (previously computed)
    :return: -
    """
    file_name = file_path.parts[-1]
    dir_path = Path(__file__).parent.resolve()
    data = simple_photometric_stereo(
        file_path,
        dir_path / 'helper_images' / 'lens_white.png',
        light_directions
    )

    # we convert the obtained normal and albedo maps back to images and save them
    normal_array = (data[0] * 255).astype(np.uint8)
    albedo_array = (data[1] * 255).astype(np.uint8)

    normal_map = Image.fromarray(normal_array)
    albedo_map = Image.fromarray(albedo_array)

    normal_map.save(dir_path / "output_normals" / file_name)
    albedo_map.save(dir_path / "output_albedos" / file_name)
