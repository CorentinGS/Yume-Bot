import datetime
import json
import urllib.request

with open('./config/keys.json', 'r') as cjson:
    keys = json.load(cjson)


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_meteo(city):
    user_api = keys["weather"]
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/weather?q='

    full_url = api + str(city) + '&mode=json&units=' + \
        unit + '&APPID=' + user_api
    return full_url


def data_fetch(full_url):
    url = urllib.request.urlopen(full_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


def data_return(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        description=raw_api_dict['weather'][0]['description'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_dir=raw_api_dict.get('wind').get('code'),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )

    return data
