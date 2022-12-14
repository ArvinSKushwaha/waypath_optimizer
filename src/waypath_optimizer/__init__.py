from typing import Optional, Union
from PIL import Image
import numpy as np
import yaml
from scipy.ndimage import distance_transform_edt


def get_dt(img: np.ndarray, map_resolution: float) -> Union[np.ndarray, None]:
    """
    Get distance transform of the image. The image is assumed to be a binary
    image with 0 as free space and 1 as occupied space.
    """
    if img.dtype != np.bool8 or img.ndim != 2:
        return None

    return distance_transform_edt(img, map_resolution, return_distances=True) # type: ignore


def image_fill(img: np.ndarray, origin_x: int, origin_y: int) -> Union[np.ndarray, None]:
    """
    Flood fill the image from the origin point.
    """
    if img.dtype != np.bool8 or img.ndim != 2:
        return None

    if img.shape[0] <= origin_x or img.shape[1] <= origin_y:
        return None

    stack = [(origin_x, origin_y)]
    while stack:
        x, y = stack.pop()
        if img[x, y]:
            continue
        img[x, y] = True
        if x > 0 and not img[x - 1, y]:
            stack.append((x - 1, y))
        if x < img.shape[0] - 1 and not img[x + 1, y]:
            stack.append((x + 1, y))
        if y > 0 and not img[x, y - 1]:
            stack.append((x, y - 1))
        if y < img.shape[1] - 1 and not img[x, y + 1]:
            stack.append((x, y + 1))

    return img


class Waypath:
    @staticmethod
    def decode_from_file(map_image_path: str, map_yaml_path: str) -> Optional["Waypath"]:
        img = np.array(Image.open(map_image_path).transpose(Image.FLIP_TOP_BOTTOM)).astype(np.float64)
        img[img <= 128.] = 0
        img[img > 128.] = 1
        img = img.astype(np.bool8)

        width, height = img.shape

        with open(map_yaml_path, 'r') as yaml_stream:
            yaml_data = yaml.load(yaml_stream, Loader=yaml.FullLoader)
            map_resolution = yaml_data['resolution']
            map_origin = yaml_data['origin']

        orig_x, orig_y, theta = map_origin
        orig_s, orig_c = np.sin(theta), np.cos(theta)

        # Computed an array of distances to the nearest black pixel
        dt = get_dt(img, map_resolution)

        if dt is None:
            return None

        # Now, find the set of pixels that are contigous white pixels starting from the origin.
        # This is the set of pixels that are on the waypath.
        img_orig_x, img_orig_y = int(orig_x / map_resolution + width / 2), int(orig_y / map_resolution + height / 2)

        filled_img = np.copy(img)
        filled_img = image_fill(filled_img, img_orig_x, img_orig_y)

        # if filled_img is None:
        #     raise ValueError("Failed to fill image")
        #
        # filled_img ^= img

        Image.fromarray(filled_img.astype(np.uint8) * 255).show()
        # Image.fromarray(img.astype(np.uint8) * 255).show()

