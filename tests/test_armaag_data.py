import os
import sys
from pathlib import Path
import unittest
import logging
logger = logging.getLogger()

from transfer2windy.armaag_data import parse_armaag_station_meteo_data, get_armaag_station_meteo_data

stations_filenames = ['weather_wszystko2.xml']

texts = [open(Path(os.path.dirname(__file__), 'resources', f)).read()
         for f in stations_filenames]


class TestArmaagMetarData(unittest.TestCase):
    def setUp(self):
        logger.setLevel('DEBUG')
        logger.addHandler(logging.StreamHandler(sys.stdout))

    def test_parse_armaag_station_meteo_data(self):
        for text in texts:
            print(parse_armaag_station_meteo_data(text, 'AM4'))

    def test_get_armaag_station_meteo_data(self):
        print(get_armaag_station_meteo_data('AM4'))
        print(get_armaag_station_meteo_data('AM11'))
