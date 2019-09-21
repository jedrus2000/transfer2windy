import os
from pathlib import Path
import unittest

from transfer2windy.polmil_metar import parse_milmetar_data, get_milmetar_station_meteo_data

stations_filenames = ['epok_metar_request.html', 'epok_metar_empty.html']

texts = [open(Path(os.path.dirname(__file__), 'resources', f)).read()
         for f in stations_filenames]


class TestPolmilMetarData(unittest.TestCase):
    def test_parse_milmetar_data(self):
        for text in texts:
            print(parse_milmetar_data(text))

    def test_get_milmetar_station_meteo_data(self):
        print(get_milmetar_station_meteo_data('EPOK'))


