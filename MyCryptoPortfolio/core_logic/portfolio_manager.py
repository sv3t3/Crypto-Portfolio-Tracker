from api.coinmarketcap import get_top_coins
from api.bybit import fetch_bybit_ticker, session

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


# Test protocol
# Test get_top_coins function
# print("Testing get_top_coins function...")
# coins = get_top_coins()
# print(coins)

# Test print_balances function
# print("Testing print_balances function...")
# balances = print_balances(my_coins)
# print(balances)
#print(list_of_coins)

# Test update_portfolio_values function
# print("Testing update_portfolio_values function...")
# portfolio_values = update_portfolio_values()
# print(portfolio_values)
