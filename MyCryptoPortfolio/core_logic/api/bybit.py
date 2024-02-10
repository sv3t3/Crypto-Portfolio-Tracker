from pybit.unified_trading import HTTP

import requests
import api_config as config

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

def fetch_bybit_ticker(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return data['result'][0]['last_price'] if data['result'] else None
    
# Testing protocol
# print(fetch_bybit_ticker('ETHUSDT'))