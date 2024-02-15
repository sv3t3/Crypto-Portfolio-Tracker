from pybit.unified_trading import HTTP
import requests
import api_config as config
from api.coinmarketcap import get_top_coins
import os

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

# Paste the code from portfolio_manager.py here
coins = get_top_coins()  # Get the list of your coins from the coin_library

# Separate coins into two lists
my_coins = [coin[:-4] for coin in coins if coin.endswith('USDT')]
other_coins = [coin for coin in coins if not coin.endswith('USDT')]

# Function to fetch the balances of the coins
def print_balances(coin_list):
    account_types = ["CONTRACT", "UNIFIED", "FUND"]
    portfolio = {}
    for account_type in account_types:
        for coin in coin_list:
            try:
                balance_info = session.get_coins_balance(
                    accountType=account_type,
                    coin=coin
                )
                # Check if the balance list is not empty and the walletBalance is greater than 0
                if balance_info['result']['balance'] and float(balance_info['result']['balance'][0]['walletBalance']) > 0:
                    # If the coin is already in the portfolio, add the new balance to the existing balance
                    if coin in portfolio:
                        portfolio[coin] += float(balance_info['result']['balance'][0]['walletBalance'])
                    else:
                        portfolio[coin] = float(balance_info['result']['balance'][0]['walletBalance'])
            except Exception as e:
                if 'coin ' + coin + ' invalid' in str(e):
                    continue  # Skip this coin and continue with the next one
                else:
                    print(f"Failed to get balance for {coin} in {account_type} account: {e}")
    return portfolio

# Function to update the values of the coins in the portfolio
def update_portfolio_values():
    my_portfolio = print_balances(my_coins)
    portfolio_values = {}

    for coin, amount in my_portfolio.items():
        if coin == "USDT":
            price = 1
        else:
            price = fetch_bybit_ticker(coin + "USDT")  # Fetch the price of the coin
        if price is not None:
            value = amount * float(price)  # Calculate the value of the coin
            portfolio_values[coin] = {'amount': amount, 'value': value}  # Store the amount and value of the coin in the dictionary
        else:
            print(f"Error fetching price for {coin}")

    return portfolio_values

portfolio_values = update_portfolio_values() # Assuming portfolio_values is your dictionary
list_of_coins = list(portfolio_values.keys()) # Get the list of coins

# Update portfolio values and get list of coins
portfolio_values = update_portfolio_values()
list_of_coins = list(portfolio_values.keys())

# Define file paths
# Define file paths
portfolio_values_file = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'portfolio_values.txt')
list_of_coins_file = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'list_of_coins.txt')
# Save portfolio_values to a text file
with open(portfolio_values_file, 'w') as f:
    for key, value in portfolio_values.items():
        f.write(f'{key}: {value}\n')

# Save list_of_coins to a text file
with open(list_of_coins_file, 'w') as f:
    for coin in list_of_coins:
        f.write(f'{coin}\n')

# Test protocol
# # Test fetch_bybit_ticker function
# print("Testing fetch_bybit_ticker function...")
# coin_price = fetch_bybit_ticker("ETH")
# print(f"BTC price: {coin_price}")

# # Test get_bybit_historical_data function
# print("\nTesting get_bybit_historical_data function...")
# btc_data = get_bybit_historical_data("BTC")
# print(f"BTC historical data: {btc_data}")

# Test print_balances function
# print("\nTesting print_balances function...")
# balances = print_balances(my_coins)
# print(f"Balances: {balances}")

# # Test update_portfolio_values function
# print("\nTesting update_portfolio_values function...")
# portfolio_values = update_portfolio_values()
# print(f"Portfolio values: {portfolio_values}")

