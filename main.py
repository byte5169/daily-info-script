import os
import requests

from retrying import retry
from dotenv import load_dotenv
from datetime import datetime
from modules.crypto_price import get_btc_price
from modules.exchange_rates import get_exchange_rates
from modules.weather import get_weather
from modules.recipe import get_recipe
from modules.google_calendar import get_event_list

load_dotenv()
bot_token = os.getenv("bot_token")
chat_ids = os.getenv("chat_id")


@retry(wait_fixed=20000)
def get_values():
    date = datetime.today().strftime("%d-%m-%Y")
    btc_list = get_btc_price()
    weather_list = get_weather(53.9006, 27.5590)
    exchange_list = get_exchange_rates()
    recipe_url = get_recipe()
    event_list = get_event_list()

    return date, weather_list, event_list, exchange_list, btc_list, recipe_url


# variables
date, weather, event, exchange, btc, recipe = get_values()


def message():
    return (
        f"Today is {date}."
        f"\n{weather[0]}. \nTemperature is {weather[1]}, but feels like {weather[2]}. \nHumidity is {weather[3]} and "
        f"wind {weather[4]}. \nDaylight hours from {weather[5]} to {weather[6]} for {weather[7]}."
        f"\n\nExchange rates are: \nUSD: {exchange[0]} \nEUR: {exchange[1]} \nRUB: {exchange[2]}"
        f"\n\nCrypto rates are: \nBTC: {btc[0]} USD with change {btc[1]} %\nETH: {btc[2]} USD with change {btc[3]} %"
        # f"\n\nClosest events are: \n{event[0]}\n{event[1]}\n{event[2]}\n{event[3]}\n{event[4]}"
        f"\n\nFor breakfast you can try this:\n{recipe}\n"
    )


def send_message(msg):
    for chat_id in chat_ids.split(" "):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
        requests.get(url)


def main():
    send_message(message())


if __name__ == "__main__":
    main()
