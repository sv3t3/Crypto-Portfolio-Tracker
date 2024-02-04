
import requests

def get_top_coins(limit=50):
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
#Testing if the function works
# top_coins = get_top_coins()
# if top_coins:
#     for symbol in top_coins:
#         print(symbol)
