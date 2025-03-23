import os
import json
import datetime
import requests
import random


def get_day_or_night() -> str:
    current_time = datetime.datetime.now().time()
    sunrise_time = datetime.time(6, 0)  # 6:00 AM
    sunset_time = datetime.time(18, 0)  # 6:00 PM
    if sunrise_time <= current_time <= sunset_time:
        return "day"
    else:
        return "night"


def get_weather_condition_code(API_KEY, LAT, LON) -> int:
    querystring = f"key={API_KEY}&q={LAT},{LON}"
    url = f"http://api.weatherapi.com/v1/current.json?{querystring}"

    response = requests.get(url)
    data = response.json()
    weather_condition_code = data['current']['condition']['code']

    return weather_condition_code


def get_weather_emoji(LAT: str, LON: str, API_KEY: str) -> str:

    conditions_file = os.path.join(
        os.path.dirname(__file__),
        'conditions.json'
    )

    with open(conditions_file) as json_file:
        WEATHER_CONDITIONS = json.load(json_file)

    weather_condition_code = get_weather_condition_code(API_KEY, LAT, LON)

    for condition in WEATHER_CONDITIONS:
        if condition["code"] == weather_condition_code:
            return condition["emoji_" + get_day_or_night()]

    return "❓"  # Default emoji if code is not found


def get_random_emoji() -> str:
    conditions_file = os.path.join(
        os.path.dirname(__file__),
        'conditions.json'
    )

    with open(conditions_file) as json_file:
        WEATHER_CONDITIONS = json.load(json_file)

    random_index = random.randint(0, len(WEATHER_CONDITIONS) - 1)

    return WEATHER_CONDITIONS[random_index]["emoji_" + get_day_or_night()]


if __name__ == "__main__":
    emoji = get_random_emoji()
    print(f"Random emoji: {emoji}")
