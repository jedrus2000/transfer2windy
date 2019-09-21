import requests

WINDY_UPDATE_URL = 'https://stations.windy.com/pws/update/'


def update_station(api_key: str, params: dict) -> int:
    try:
        r = requests.get(WINDY_UPDATE_URL + api_key, params=params)
        r.raise_for_status()
        return r.status_code
    except Exception as e:
        ...


def update_stations(api_key: str, observations_list: list) -> int:
    try:
        r = requests.post(WINDY_UPDATE_URL + api_key, json={'observations': observations_list})
        r.raise_for_status()
        return r.status_code
    except Exception as e:
        ...
