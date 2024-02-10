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

print(f"Current Bitcoin block height: {current_block_height}")
print(f"Blocks until next halving: {blocks_to_next_halving}")
print(f"Estimated next Bitcoin halving date: {estimated_halving_date.strftime('%Y-%m-%d %H:%M')}")
























# from portfolio_manager import update_portfolio_values
# import sys
# import requests
# import os
# from datetime import datetime

# def get_fear_and_greed_index():
#     url = "https://api.alternative.me/fng/?limit=0"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         index = data['data'][0]['value']
#         return index
#     except Exception as e:
#         print(f"Error fetching Fear and Greed Index: {e}")
#         return None

# def get_top_coins(limit=100):
#     url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={limit}&sortBy=market_cap&sortType=desc&convert=USD"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         coins = data['data']['cryptoCurrencyList']
#         symbols = [coin['symbol'].upper() + 'USDT' for coin in coins]
#         return symbols
#     except Exception as e:
#         print(f"Error fetching top coins from CoinMarketCap: {e}")
#         return None

# # Testing protocol
# fear_and_greed_index = get_fear_and_greed_index()
# if fear_and_greed_index is not None:
#     print(f"Fear and Greed Index: {fear_and_greed_index}")
# top_coins = get_top_coins()
# if top_coins:
#     for symbol in top_coins:
#         print(symbol)


# # Define the conversion function - which currency to convert to USDT
# def convert_eur_to_usdt(amount_in_eur):
#     response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
#     eur_to_usd_rate = response.json()['rates']['USD']
#     amount_in_usd = amount_in_eur * eur_to_usd_rate
#     return amount_in_usd

# # Function for total portfolio value
# def calculate_total_portfolio_value(portfolio_values):
#     total_value = 0
#     for coin, data in portfolio_values.items():
#         total_value += data['value']
#     return total_value

# # Store portfolio value ina file for growth display
# def save_portfolio_value(total_value):
#     with open('portfolio_value.txt', 'a') as f:
#         f.write(f'{datetime.now()}: {total_value}\n')

# # Retrieve from history log
# def get_last_portfolio_value():
#     if not os.path.exists('portfolio_value.txt'):
#         return None
#     with open('portfolio_value.txt', 'r') as f:
#         return float(f.read())

# # Get allocation for each coin in the portfolio
# def allocation():
#     portfolio_values = update_portfolio_values()
#     total_value = sum(coin['value'] for coin in portfolio_values.values())
#     allocation = {coin: (value['value'] / total_value) * 100 for coin, value in portfolio_values.items()} # Percentage allocation
#     return allocation

# # Portfolios p/l
# def calculate_profit_loss(initial_investment, current_value):
#     return current_value - initial_investment

# # Terminal display of info
# def display_portfolio_value(initial_investment):
#     portfolio_values = update_portfolio_values()
#     total_value = calculate_total_portfolio_value(portfolio_values)

#     last_total_value = get_last_portfolio_value()
#     if last_total_value is not None:
#         growth_since_last_run = ((total_value - last_total_value) / last_total_value) * 100
#         print(f"Growth since last run: {growth_since_last_run:.2f}%")

#     save_portfolio_value(total_value)
#     profit_loss = calculate_profit_loss(initial_investment, total_value)

#     # Better display of the portfolio allocation
#     allocations = allocation()
#     print(f"{'Coin':<10}{'Allocxation':<15}{'Allocation in USDT':>20}")
#     print("-" * 47)
#     for coin, alloc in allocations.items():
#         alloc_usdt = (alloc / 100) * total_value
#         print(f"{coin:<10}{alloc:.2f}%{alloc_usdt:>20.2f} USDT") # More of a chart
#     print("-" * 47)

#     # Print portfolio value and profit/loss
#     print(f"Total portfolio value: {round(total_value, 2)} USDT")
#     print(f"Profit/Loss: {round(profit_loss, 2)} USDT")

# # Get the initial investment and its currency - user interaction
# currency = input("Enter the currency of your initial investment (EUR, USD): ")
# initial_investment = float(input("Your initial investment: "))  # Use float() instead of int()

# # Convert the initial investment to USDT if the currency is EUR
# if currency.upper() == 'EUR':
#     initial_investment = convert_eur_to_usdt(initial_investment)

# if __name__ == "__main__":
#     display_portfolio_value(initial_investment)