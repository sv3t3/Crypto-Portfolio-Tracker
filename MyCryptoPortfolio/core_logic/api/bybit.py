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

from datetime import datetime

def get_bybit_historical_data(coin, interval='D', from_timestamp=None, limit=200):
    url = 'https://api.bybit.com/public/linear/kline'
    params = {
        'symbol': coin + 'USDT',
        'interval': interval,
        'from': from_timestamp or int(datetime.now().timestamp()) - 7 * 24 * 60 * 60,  # 7 days ago
        'limit': limit,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['ret_code'] == 0:
        return data['result']
    else:
        print(f"Error for coin {coin}: {data['ret_msg']}")
        return None
    
# Testing protocol
# print(fetch_bybit_ticker('ETHUSDT'))
