import numpy as np
from PIL import Image
from scipy import linalg

import helpers


def compute_normals(light_matrix, mask_array, image_array, threshold=100):
    shaper = (mask_array.shape[0], mask_array.shape[1], 3)

    normal_map = np.zeros(shaper)
    ivec = np.zeros(1)

    for (xT, value) in np.ndenumerate(mask_array):
        if value > threshold:
            ivec[0] = image_array[xT[0], xT[1]]

            (normal, res, rank, s) = linalg.lstsq(light_matrix, ivec)

            normal /= linalg.norm(normal)

            if not np.isnan(np.sum(normal)):
                normal_map[xT] = normal

    return normal_map


def compute_albedo(light_matrix, mask_array, image_array, normal_map, threshold=100):
    shaper = (mask_array.shape[0], mask_array.shape[1], 3)

    albedo_map = np.zeros(shaper)
    ivec = np.zeros((1, 3))

    for (xT, value) in np.ndenumerate(mask_array):
        if value > threshold:
            ivec[0] = image_array[xT[0], xT[1]]

            i_t = np.dot(light_matrix, normal_map[xT])

            k = np.dot(np.transpose(ivec), i_t) / (np.dot(i_t, i_t))

            if not np.isnan(np.sum(k)):
                albedo_map[xT] = k

    return albedo_map


def simple_photometric_stereo(image_file, mask_image_file, light_directions, threshold=25):
    lights = [light_directions]
    mask_image = Image.open(mask_image_file)
    mask_image_gray = mask_image.convert("L")
    mask_image_array = np.asarray(mask_image_gray)

    image = Image.open(image_file).convert("RGB")
    image_array = np.asarray(image)
    image_gray = image.convert("L")
    image_gray_array = np.asarray(image_gray)

    normal_map = compute_normals(np.array(lights), mask_image_array, image_gray_array)
    albedo_map = compute_albedo(np.array(lights), mask_image_array, image_array, normal_map)

    return normal_map, albedo_map


def compute(file_path, light_directions):
    file_name = helpers.get_file_name_from_path(file_path)
    data = simple_photometric_stereo(
        file_path,
        'helper_images/lens_white.png',
        light_directions
    )

    normal_array = (data[0] * 255).astype(np.uint8)
    albedo_array = (data[1] * 255).astype(np.uint8)

    normal_map = Image.fromarray(normal_array)
    albedo_map = Image.fromarray(albedo_array)

    normal_map.save(f"output_normals/{file_name}.png")
    albedo_map.save(f"output_albedos/{file_name}.png")
