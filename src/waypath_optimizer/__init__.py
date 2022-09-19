from typing import Optional
from PIL import Image
import numpy as np
import yaml


def get_dt(img: np.ndarray, map_resolution: float) -> np.ndarray | None:
    return None


class Waypath:
    @staticmethod
    def decode_from_file(map_image_path: str, map_yaml_path: str) -> Optional["Waypath"]:
        img = np.array(Image.open(map_image_path).transpose(Image.FLIP_TOP_BOTTOM)).astype(np.float64)
        img[img <= 128.] = 0.0
        img[img > 128.] = 1.0

        width, height = img.shape

        with open(map_yaml_path, 'r') as yaml_stream:
            yaml_data = yaml.load(yaml_stream, Loader=yaml.FullLoader)
            map_resolution = yaml_data['resolution']
            map_origin = yaml_data['origin']

        orig_x, orig_y, theta = map_origin
        orig_s, orig_c = np.sin(theta), np.cos(theta)

        dt = get_dt(img, map_resolution)
