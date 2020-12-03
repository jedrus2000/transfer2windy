from bs4 import BeautifulSoup
from typing import List
import re
import requests
import logging
logger = logging.getLogger()
from metar import Metar

IMGW_BASE_URL = "http://awiacja.imgw.pl/metarmil.php"


def get_milmetar_station_meteo_data(station_id: str) -> dict:
    return parse_milmetar_data(download_milmetar_data(station_id))


def parse_milmetar_data(station_html_data: str) -> dict:
    result = dict()
    try:
        soup = BeautifulSoup(station_html_data, 'html.parser')
        obs = Metar.Metar(soup.find_all('description')[1].text.strip())
        if not obs.code:
            logger.info("No data")
            return result
        tempresult = dict()
        tempresult['dateutc'] = str(obs.time)
        if len(obs._unparsed_remarks) > 1:
            temp = obs._unparsed_remarks[0].split('M')
            tempresult['temp'] = -1*int(temp[1])/10 if len(temp)>1 else int(temp[0])/10
            tempresult['humidity'] = int(obs._unparsed_remarks[1])
        else:
            tempresult['temp'] = obs.temp.value()

        tempresult['dewpoint'] = obs.dewpt.value()
        tempresult['wind'] = obs.wind_speed.value('mps')
        tempresult['winddir'] = obs.wind_dir.value()
        tempresult['mbar'] = obs.press.value()

        result = {key: value for (key, value) in tempresult.items() if value}
    except Exception as e:
        logger.error(f"parse_milmetar_data {e}")
        logger.debug(f"error while parsing {station_html_data}")

    return result


def download_milmetar_data(station_id: str) -> str:
    result = ''
    try:
        r = requests.get(IMGW_BASE_URL, params={'airport': station_id.upper()})
        r.raise_for_status()
        result = r.text
    except Exception as e:
        logger.error(e)

    return result

