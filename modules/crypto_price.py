import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_crypto_key")


def get_btc_price():

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}

    response = requests.get(url, headers=headers)
    response_json = response.json()

    btc = response_json["data"][0]
    eth = response_json["data"][1]

    btc_price = round(btc["quote"]["USD"]["price"], 2)
    btc_change = round(btc["quote"]["USD"]["percent_change_24h"], 2)

    eth_price = round(eth["quote"]["USD"]["price"], 2)
    eth_change = round(eth["quote"]["USD"]["percent_change_24h"], 2)

    values = [btc_price, btc_change, eth_price, eth_change]

    return values
