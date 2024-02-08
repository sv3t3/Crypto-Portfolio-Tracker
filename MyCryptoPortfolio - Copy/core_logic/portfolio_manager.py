from pybit.unified_trading import HTTP
import config
import requests
from MyCryptoPortfolio.api.coinmarketcap import get_top_coins  # Assuming this function returns a list of your coins
from MyCryptoPortfolio.api.bybit import session, fetch_bybit_ticker

coins = get_top_coins()  # Get the list of your coins from the coin_library

# Separate coins into two lists
my_coins = [coin[:-4] for coin in coins if coin.endswith('USDT')]
other_coins = [coin for coin in coins if not coin.endswith('USDT')]

# Function to fetch the balances of the coins
def print_balances(coin_list):
    portfolio = {}
    for coin in coin_list:
        try:
            balance_info = session.get_coins_balance(
                accountType="FUND",
                coin=coin
            )
            # Check if the balance list is not empty and the walletBalance is greater than 0
            if balance_info['result']['balance'] and float(balance_info['result']['balance'][0]['walletBalance']) > 0:
                portfolio[coin] = float(balance_info['result']['balance'][0]['walletBalance'])  # Add the balance to the portfolio
                # print(f"Balance for {coin}: {balance_info['result']['balance'][0]['walletBalance']}")
        except Exception as e:
            if 'coin ' + coin + ' invalid' in str(e):
                continue  # Skip this coin and continue with the next one
            else:
                print(f"Failed to get balance for {coin}: {e}")
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


# Test protocol
# print("List of coins:") # Print the list of coins
# print(coins)

# print("\nMy coins:") # Print the list of your coins
# print(my_coins)

# print("\nOther coins:")  #Print the list of other coins
# print(other_coins)

# print("\nFetching price for BTCUSDT:") # Test the fetch_bybit_ticker function
# print(fetch_bybit_ticker("BTCUSDT")) 

# print("\nFetching balances for my coins:") # Test the print_balances function
# balances = print_balances(my_coins)
# for coin, balance in balances.items():
#     print(f"{coin}: {balance}")

# print("\nUpdating portfolio values:") # Test the update_portfolio_values function
# portfolio_values = update_portfolio_values()
# for coin, data in portfolio_values.items():
#     print(f"{coin}: {data}")