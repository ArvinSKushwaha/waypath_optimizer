import unittest
import shutil
import os

from .random_trackgen import create_track, convert_track


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
        track_generate()

    def tearDown(self) -> None:
        shutil.rmtree("./maps")
        shutil.rmtree("./centerline")


if __name__ == "__main__":
    unittest.main()
