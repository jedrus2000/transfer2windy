# https://armaag.gda.pl/data/xml/weather_wszystko2.xml
# every hour
import os
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import requests
import logging
logger = logging.getLogger()

# data can be cached as all ARMAAG sites are in one file
cached_data = None

ARMAAG_BASE_URL = "https://armaag.gda.pl/data/xml/weather_wszystko2.xml"


def get_armaag_station_meteo_data(station_id: str) -> dict:
    return parse_armaag_station_meteo_data(download_armaag_station_meteo_data(), station_id)


def parse_armaag_station_meteo_data(stations_xml_data: str, station_id: str) -> dict:
    properties: List = [
        {
            'property_name': 'temp',
            'substance_type': 'TEMP'
        },
        {
            'property_name': 'wind',
            'substance_type': 'WV'
        },
        {
            'property_name': 'winddir',
            'substance_type': 'WD'
        },
        {
            'property_name': 'humidity',
            'substance_type': 'WILG'
        },
        {
            'property_name': 'mbar',
            'substance_type': 'CISN'
        },
        {
            'property_name': 'percip',
            'substance_type': 'RAIN'
        },
    ]
    result = dict()

    try:
        last_index_with_value = None
        soup = BeautifulSoup(stations_xml_data, 'xml')
        start_date_unix_epoch = int(soup.document['start_date'])
        station = soup.document.find('station', {'name': station_id})

        for prop in properties:
            substance = station.find('substance', {'type': prop['substance_type']})
            if not substance:
                continue
            values_list = substance.text.split('|')
            last_index_with_value = max(loc for loc, val in enumerate(values_list) if val != '-999')
            result[prop['property_name']] = values_list[last_index_with_value]

        if last_index_with_value is not None:
            local_tz = timezone(os.environ.get('TZ', 'Europe/Warsaw').strip(':'))
            loc_dt = local_tz.localize(datetime.fromtimestamp(start_date_unix_epoch+last_index_with_value*3600))
            result['dateutc'] = loc_dt.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
            if result['winddir'] is not None:
                result['winddir'] = round(float(result['winddir']))

    except Exception as e:
        logger.error(e)

    return result


def download_armaag_station_meteo_data() -> str:
    global cached_data
    if cached_data:
        logger.debug("using cached data: no need to download")
        return cached_data

    logger.debug("downloading data")
    result = ''
    try:
        r = requests.get(ARMAAG_BASE_URL)
        r.raise_for_status()
        result = r.text
        cached_data = result
    except Exception as e:
        logger.error(e)

    return result
