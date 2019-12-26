import unittest

from transfer2windy.__main__ import lambda_handler

class TestMain(unittest.TestCase):
    def test_lambda_handler(self):
        stations = [ { "source_type": "gddkia", "source_id": "145", "windy_station_id": "0" },
                     { "source_type": "polmil-metar", "source_id": "EPOK","windy_station_id": "1" },
                     { "source_type": "armaag", "source_id": "AM4", "windy_station_id": "2" },
                     { "source_type": "armaag", "source_id": "AM11", "windy_station_id": "3" },
                     { "source_type": "armaag", "source_id": "AM12", "windy_station_id": "4" },
                     { "source_type": "iopan", "source_id": "SOPOT", "windy_station_id": "5" } ]
        print(lambda_handler(stations, None))

