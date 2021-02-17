import requests
from datetime import datetime, timezone

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_weather_key")


def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)
    response_json = response.json()

    weather_state = response_json["weather"][0]["main"]
    temp_cur = str(round((response_json["main"]["temp"] - 273.15), 2)) + " °C"
    temp_feels_like = (
        str(round((response_json["main"]["feels_like"] - 273.15), 2)) + " °C"
    )
    humidity = str(response_json["main"]["humidity"]) + " %"
    wind = str(response_json["wind"]["speed"]) + " m/s"
    sunrise = (
        datetime.utcfromtimestamp(response_json["sys"]["sunrise"])
        .replace(tzinfo=timezone.utc)
        .astimezone(tz=None)
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    sunset = (
        datetime.utcfromtimestamp(response_json["sys"]["sunset"])
        .replace(tzinfo=timezone.utc)
        .astimezone(tz=None)
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    daylight_hours = (
        str(
            round(
                (response_json["sys"]["sunset"] - response_json["sys"]["sunrise"])
                / 3600,
                1,
            )
        )
        + " hours"
    )

    weather = [
        weather_state,
        temp_cur,
        temp_feels_like,
        humidity,
        wind,
        sunrise,
        sunset,
        daylight_hours,
    ]

    weather_string = (
        f"\n{weather[0]}. \nTemperature is {weather[1]}, but feels like {weather[2]}. \nHumidity is {weather[3]} and "
        f"wind {weather[4]}. \nDaylight hours from {weather[5]} to {weather[6]} for {weather[7]}."
    )

    return weather_string


# get_weather(53.9006, 27.5590)
