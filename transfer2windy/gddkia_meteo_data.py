from bs4 import BeautifulSoup
from typing import List
import re
import requests

GDDKIA_BASE_URL = "https://www.traxelektronik.pl/pogoda/stacja/stacja.php"


def get_gddkia_station_meteo_data(station_id: str) -> dict:
    return parse_gddkia_station_meteo_data(download_gddkia_station_meteo_data(station_id))


def parse_gddkia_station_meteo_data(station_html_data: str) -> dict:
    properties: List = [
        {
            'property_name': 'temp',
            'regex': r'^temp\.php?.temp\=([0-9\.-]*).*name\=Temperatura\,powietrza$'
        },
        {
            'property_name': 'dewpoint',
            'regex': r'^temp\.php?.temp\=([0-9\.-]*).*name=Temperatura,punktu,rosy'
        },
        {
            'property_name': 'wind',
            'regex': r'^wiatr\.php?.v\=([0-9\.]*)'
        },
        {
            'property_name': 'winddir',
            'regex': r'^wiatr\.php.*k\=([0-9\.-]*)'
        },
        {
            'property_name': 'humidity',
            'regex': r'^higro\.php?.h\=([0-9\.]*)'
        },

    ]

    result = dict()

    soup = BeautifulSoup(station_html_data, 'html.parser')

    try:
        # get temperatures, wind speed, humidity
        table_rows = soup.find_all('table')[1].find_all('img')
        for prop in properties:
            for row in table_rows:
                text = row['src']
                search_res = re.match(prop['regex'], text)
                if not search_res or not search_res.groups()[0] or not float(search_res.groups()[0]) > -1000:
                    continue
                result[prop['property_name']] = search_res.groups()[0]
    except Exception as e:
        ...

    return result


def download_gddkia_station_meteo_data(station_id: str) -> str:
    result = ''
    try:
        r = requests.get(GDDKIA_BASE_URL, params={'stid': station_id, 'w_ekr': '1024'})
        r.raise_for_status()
        result = r.text
    except Exception as e:
        ... # print(e)

    return result
