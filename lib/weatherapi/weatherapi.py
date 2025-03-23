import os
import json
import datetime
import requests


def get_day_or_night():
    current_time = datetime.datetime.now().time()
    sunrise_time = datetime.time(6, 0)  # 6:00 AM
    sunset_time = datetime.time(18, 0)  # 6:00 PM
    if sunrise_time <= current_time <= sunset_time:
        return "day"
    else:
        return "night"


def get_weather_condition_code(API_KEY, LAT, LON):
    querystring = f"key={API_KEY}&q={LAT},{LON}"
    url = f"http://api.weatherapi.com/v1/current.json?{querystring}"

    response = requests.get(url)
    data = response.json()
    weather_condition_code = data['current']['condition']['code']

    return weather_condition_code


def get_weather_emoji(API_KEY, LAT, LON):
    weather_condition_code = get_weather_condition_code(API_KEY, LAT, LON)
    conditions_file = os.path.join(os.path.dirname(__file__),
                                   'conditions.json')
    with open(conditions_file) as json_file:
        WEATHER_CONDITIONS = json.load(json_file)

    for condition in WEATHER_CONDITIONS:
        if condition["code"] == weather_condition_code:
            return condition["emoji_" + get_day_or_night()]

    return "❓"  # Default emoji if code is not found
