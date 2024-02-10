import requests
from datetime import datetime, timedelta

def get_current_block_height():
    response = requests.get('https://api.blockchair.com/bitcoin/stats')
    return response.json()['data']['blocks']

def estimate_halving_date(current_block_height):
    blocks_to_next_halving = 210000 - (current_block_height % 210000)
    # On average, a new Bitcoin block is mined every 10 minutes
    time_to_next_halving = timedelta(minutes=blocks_to_next_halving * 10)
    estimated_halving_date = datetime.now() + time_to_next_halving
    return estimated_halving_date, blocks_to_next_halving

current_block_height = get_current_block_height()
estimated_halving_date, blocks_to_next_halving = estimate_halving_date(current_block_height)

def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/?limit=0"
    try:
        response = requests.get(url)
        data = response.json()
        index = data['data'][0]['value']
        return index
    except Exception as e:
        print(f"Error fetching Fear and Greed Index: {e}")
        return None

def get_top_coins(limit=100):
    url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={limit}&sortBy=market_cap&sortType=desc&convert=USD"
    try:
        response = requests.get(url)
        data = response.json()
        coins = data['data']['cryptoCurrencyList']
        symbols = [coin['symbol'].upper() + 'USDT' for coin in coins]
        return symbols
    except Exception as e:
        print(f"Error fetching top coins from CoinMarketCap: {e}")
        return None

# Testing protocol
# print(f"Current Bitcoin block height: {current_block_height}")
# print(f"Blocks until next halving: {blocks_to_next_halving}")
# print(f"Estimated next Bitcoin halving date: {estimated_halving_date.strftime('%Y-%m-%d %H:%M')}")

# fear_and_greed_index = get_fear_and_greed_index()
# if fear_and_greed_index is not None:
#     print(f"Fear and Greed Index: {fear_and_greed_index}")

# top_coins = get_top_coins()
# if top_coins:
#     for symbol in top_coins:
#         print(symbol)
