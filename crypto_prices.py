import ccxt
from coin_library import get_top_coins
from prettytable import PrettyTable
import requests 

def fetch_bybit_ticker(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return data['result'][0]['last_price'] if data['result'] else None

def get_exchange(exchange_id):
    try:
        exchange_class = getattr(ccxt, exchange_id)
        return exchange_class()
    except AttributeError:
        print(f"Exchange {exchange_id} not found. Please enter a valid exchange.")
        return None

exchange_ = input("Enter exchange name: ").lower()  # Convert input to lowercase

# if exchange_ == "bybit":
#     for coin_symbol in get_top_coins():
#         price = fetch_bybit_ticker(coin_symbol)
#         if price is not None:
#             print(f"{coin_symbol}: {price}")
#         else:
#             print(f"Error fetching data for {coin_symbol}")
# else:
#     exchange = get_exchange(exchange_)

#     if exchange:
#         for coin_symbol in get_top_coins():
#             try:
#                 price_data = exchange.fetch_ticker(coin_symbol)
#                 if price_data and price_data['last']:
#                     print(f"{coin_symbol}: {price_data['last']}")
#                 else:
#                     print(f"Price data for {coin_symbol} is not available")
#             except ccxt.ExchangeError:
#                 print(f"{coin_symbol} is not listed on {exchange_.capitalize()}")
#             except Exception as e:
#                 print(f"Error fetching data for {coin_symbol}: {e}")


coin_prices = {}  # Initialize an empty dictionary to store the coin prices

if exchange_ == "bybit":
    for coin_symbol in get_top_coins():
        price = fetch_bybit_ticker(coin_symbol)
        if price is not None:
            coin_prices[coin_symbol] = price  # Store the price in the dictionary
        else:
            print(f"Error fetching data for {coin_symbol}")
else:
    exchange = get_exchange(exchange_)

    if exchange:
        for coin_symbol in get_top_coins():
            try:
                price_data = exchange.fetch_ticker(coin_symbol + "USDT")
                if price_data and price_data['last']:
                    coin_prices[coin_symbol] = price_data['last']  # Store the price in the dictionary
                else:
                    print(f"Price data for {coin_symbol} is not available")
            except ccxt.ExchangeError:
                print(f"{coin_symbol} is not listed on {exchange_.capitalize()}")
            except Exception as e:
                print(f"Error fetching data for {coin_symbol}: {e}")

print(coin_prices)  # Print the dictionary of coin prices