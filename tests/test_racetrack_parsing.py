import unittest
import shutil
import os

import numpy as np

from .random_trackgen import create_track, convert_track
from waypath_optimizer import image_fill


def track_generate():
    while True:
        track_data = create_track()
        if track_data != False:
            track, track_int, track_ext = track_data
            convert_track(track, track_int, track_ext, 0)
            break


class TestRacetrackParsing(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("./maps")
        os.mkdir("./centerline")

    def test_track_parse(self):
        pass

    def test_flood_fill(self):
        assert np.all(image_fill(np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ], dtype=np.bool_), 2, 2) == np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ], dtype=np.bool_))

    def tearDown(self) -> None:
        shutil.rmtree("./maps")
        shutil.rmtree("./centerline")


if __name__ == "__main__":
    unittest.main()
