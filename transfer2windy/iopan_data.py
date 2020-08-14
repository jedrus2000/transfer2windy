import os
import re
import ast
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import requests
import logging
logger = logging.getLogger()

IOPAN_BASE_URL = "http://www.iopan.gda.pl/MarPoLab/wykresy/wykresy.php"


def get_iopan_station_meteo_data(station_id_ignored: str) -> dict:
    return parse_iopan_station_meteo_data(download_iopan_station_meteo_data(), station_id_ignored)


def parse_iopan_station_meteo_data(stations_xml_data: str, station_id_ignored: str) -> dict:
    if not stations_xml_data:
        return dict()

    #   'property_name': 'winddir',
    properties: Dict = {
        0: 'wind',  # prwt
        2: 'gust',  # prwtmax
        3: 'temp',  # temp
        5: 'precip',  # opad
        6: 'mbar',  # cis
        8: 'humidity'  # wil
    }
    result = dict()

    try:
        start_date_unix_epoch = None
        soup = BeautifulSoup(stations_xml_data, 'html.parser')
        # wind direction is only in fancy table
        cell = soup.find('div', {'id': 'kierwiat'}).\
                         find('div', {'class': 'tabelka'}).\
                         find_all('div', {'class': 'komorka'})[-1]

        #  date_str = cell.find('p', {'class', 'kdata'}).text  # <p class="kdata" style="background-color:#D4D4D4;">25-VII 2019</p>
        #  time_str = cell.find('p', {'class', 'kczas'}).text  # <p class="kczas" style="background-color:#D4D4D4;">05:00</p>
        result['winddir'] = round(float(cell.find('p', {'class', 'kwartosc'}).text.strip()))  # <p class="kwartosc" style="background-color:#D4D4D4;">296.26<br>
        #  day = date_str[0:date_str.index('-')]
        #  month = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'].\
        #                index(date_str[date_str.index('-')+1:-4].strip())+1
        #  year = date_str[-4:]


        # ... rest of parameters
        data_js = soup.find('script', {'id': 'source'}).text.strip()
        search_res = re.findall(r"\=\s*(\[[^;]*)", data_js, re.MULTILINE)

        for prop_k, prop_v in properties.items():
            data = [a for a in reversed(ast.literal_eval(search_res[prop_k])) if len(a)>1]
            if start_date_unix_epoch is not None and start_date_unix_epoch != data[0][0]:
                logger.warning(f'Values lists at {prop_k} do not match by epoch. Current epoch: {start_date_unix_epoch}, found: {data[0][0]}')
                # logger.debug(f'Value object: {data[0]}')
            else:
                start_date_unix_epoch = data[0][0]
            result[prop_v] = data[0][1]

        local_tz = timezone(os.environ.get('TZ', 'Europe/Warsaw').strip(':'))
        mistake_factor = 2*3600
        epoch_without_milis = round(start_date_unix_epoch/1000)-mistake_factor
        loc_dt = local_tz.localize(datetime.fromtimestamp(epoch_without_milis))
        result['dateutc'] = loc_dt.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        logger.error(e)
        # raise e

    return result


def download_iopan_station_meteo_data() -> str:
    result = ''
    try:
        r = requests.get(IOPAN_BASE_URL, timeout=180)
        r.raise_for_status()
        result = r.text
    except Exception as e:
        logger.error(e)

    return result
