import unittest

from transfer2windy.__main__ import lambda_handler

class TestMain(unittest.TestCase):
    def test_lambda_handler(self):
        stations = [
            {"source_type": "polmil-metar", "source_id": "EPOK", "windy_station_id": ""},
            {"source_type": "armaag", "source_id": "AM4", "windy_station_id": ""},
            {"source_type": "armaag", "source_id": "AM11", "windy_station_id": ""},
            {"source_type": "gddkia", "source_id": "145", "windy_station_id": ""}
        ]
        print(lambda_handler(stations, None))

