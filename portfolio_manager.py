from pybit.unified_trading import HTTP
import config
from coin_library import get_top_coins  # Assuming this function returns a list of your coins

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

coins = get_top_coins()  # Get the list of your coins from the coin_library

# Separate coins into two lists
my_coins = [coin[:-4] for coin in coins if coin.endswith('USDT')]
other_coins = [coin for coin in coins if not coin.endswith('USDT')]

# Function to print balances
def print_balances(coin_list):
    for coin in coin_list:
        try:
            balance_info = session.get_coins_balance(
                accountType="FUND",
                coin=coin
            )
            # Check if the balance list is not empty and the walletBalance is greater than 0
            if balance_info['result']['balance'] and float(balance_info['result']['balance'][0]['walletBalance']) > 0:
                print(f"Balance for {coin}: {balance_info['result']['balance'][0]['walletBalance']}")
        except Exception as e:
            if 'coin ' + coin + ' invalid' in str(e):
                continue  # Skip this coin and continue with the next one
            else:
                print(f"Failed to get balance for {coin}: {e}")

# Then print balances for your coins
print("Balances for my coins:")
print_balances(my_coins)