import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.shortcuts import render


# Create your views here.


def index(request):
    global active_cryptocurrencies,market_cap_change_percentage_24h_usd
    market_cap_value = 0
    d_list = {}
    api_baseData = requests.get("https://api.coingecko.com/api/v3/global")
    api_data = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h")
    data = json.loads(api_data.content)
    baseData = json.loads(api_baseData.content)

    for key, values in baseData.items():
        for inner_Key, inner_val in values.items():
            d_list[inner_Key] = inner_val
    active_cryptocurrencies = d_list['active_cryptocurrencies']
    market_cap_change_percentage_24h_usd=d_list['market_cap_change_percentage_24h_usd']

    for key, value in d_list['total_market_cap'].items():
        market_cap_value += value

    return render(request, 'index.html', {'api_data': data, 'active_cryptocurrencies': active_cryptocurrencies,
                                          'market_cap_change_percentage_24h_usd': market_cap_change_percentage_24h_usd,
                                          'total_market_cap':market_cap_value})
