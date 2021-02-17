import requests


def get_exchange_rates():
    url = "https://belarusbank.by/api/kursExchange?city=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA"
    response = requests.get(url)
    response_json = response.json()
    exchange_list = [
        response_json[0]["USD_in"],
        response_json[0]["EUR_in"],
        response_json[0]["RUB_in"],
    ]
    exchange_string = f"\n\nExchange rates are: \nUSD: {exchange_list[0]} \nEUR: {exchange_list[1]} \nRUB: {exchange_list[2]}"

    return exchange_string
