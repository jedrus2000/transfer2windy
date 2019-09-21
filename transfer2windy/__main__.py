import argparse
import os
import sys
import transfer2windy

import logging
logger = logging.getLogger()


def lambda_handler(events, context):
    result = list()
    data_for_windy_list = list()
    for event in events:
        windy_msg = {'message': 'No data'}

        functions = {
            'gddkia': transfer2windy.get_gddkia_station_meteo_data,
            'polmil-metar': transfer2windy.get_milmetar_station_meteo_data,
            'armaag': transfer2windy.get_armaag_station_meteo_data,
            'iopan': transfer2windy.get_iopan_station_meteo_data
        }

        data_for_windy = functions.get(event['source_type'])(event['source_id'])
        if data_for_windy:
            data_for_windy['station'] = event['windy_station_id']
            status_code = 0 if not event['windy_station_id'] else data_for_windy_list.append(data_for_windy) # send2windy(data_for_windy)
            windy_msg['message'] = f'Windy response: {status_code}, station type: {event["source_type"]},' \
                f' data for Windy: {data_for_windy}'

        logger.info(windy_msg)
        result.append(windy_msg)

    send2windy(data_for_windy_list)

    return result


def send2windy(data_for_windy) -> int:
    api_key = os.environ.get('WINDY_API_KEY', None)
    if not api_key:
        msg = 'Missing env variable: WINDY_API_KEY !!!'
        logger.error(msg)
        return 500
    return transfer2windy.update_station(api_key, data_for_windy) if isinstance(data_for_windy, dict) else \
        transfer2windy.update_stations(api_key, data_for_windy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='transfer2windy', description='Push weather data to Windy, from different sources.')
    parser.add_argument('source_type', type=str, choices=['polmil-metar', 'gddkia', 'armaag', 'iopan'], help='source type')
    parser.add_argument('source_id', type=str, help='Source type based ID')
    parser.add_argument('windy_station_id', type=str, nargs='?', default="", help='Windy station ID')

    args = parser.parse_args()

    event = {
        'source_type': args.source_type,
        'source_id': args.source_id,
        'windy_station_id': args.windy_station_id
    }

    print(lambda_handler([event], None))

