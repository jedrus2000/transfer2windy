import os
from pathlib import Path
import unittest

from transfer2windy.gddkia_meteo_data import parse_gddkia_station_meteo_data

stations_filenames = ['stid_101.html', 'stid_145.html', 'stid_180.html', 'stid_1100.html']

texts = [open(Path(os.path.dirname(__file__), 'resources', f), encoding="iso-8859-2").read()
                           for f in stations_filenames]


class TestGddkiaMeteoData(unittest.TestCase):
    def test_parse_gddkia_station_meteo_data(self):
        for text in texts:
            print(parse_gddkia_station_meteo_data(text))

