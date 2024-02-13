from portfolio_manager import update_portfolio_values, list_of_coins, portfolio_values
import requests
import os
import time
from datetime import datetime, timedelta
from api.bybit import get_bybit_historical_data

# ------------------------------
# Constants
# ------------------------------
project_folder = os.path.dirname(os.path.abspath(__file__))
database_folder = os.path.join(project_folder, '..', 'database')
filename = os.path.join(database_folder, 'portfolio_value.txt')
initial_investment_filename = os.path.join(database_folder, 'initial_investment.txt')

# ------------------------------
# Conversion Functions
# ------------------------------
def convert_eur_to_usdt(amount_in_eur):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    eur_to_usd_rate = response.json()['rates']['USD']
    amount_in_usd = amount_in_eur * eur_to_usd_rate
    return amount_in_usd

# ------------------------------
# Portfolio Value Calculation
# ------------------------------
def calculate_total_portfolio_value(portfolio_values):
    total_value = 0
    for coin, data in portfolio_values.items():
        total_value += data['value']
    return total_value

def get_portfolio_days_ago(days):
    with open(filename, 'r') as f:
        lines = f.readlines()
        now = datetime.now()
        for line in reversed(lines):
            timestamp, value = line.split(': ')
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            if now - timestamp > timedelta(days=days):
                return float(value)
    return None

def save_portfolio_value(total_value):
    with open(filename, 'a') as f:
        f.write(f'{datetime.now()}: {total_value:.2f}\n')

# ------------------------------
# Initial Investment
# ------------------------------
def get_initial_investment():
    if os.path.exists(initial_investment_filename):
        with open(initial_investment_filename, 'r') as f:
            return float(f.read())
    else:
        currency = input("Enter the currency of your initial investment (EUR, USD): ")
        initial_investment = float(input("Your initial investment: "))
        if currency.upper() == 'EUR':
            initial_investment = convert_eur_to_usdt(initial_investment)
        with open(initial_investment_filename, 'w') as f:
            f.write(str(initial_investment))
        return initial_investment

# ------------------------------
# Portfolio Allocation
# ------------------------------
def allocation():
    portfolio_values = update_portfolio_values()
    total_value = sum(coin['value'] for coin in portfolio_values.values())
    allocation = {coin: (value['value'] / total_value) * 100 for coin, value in portfolio_values.items()}
    return allocation

# ------------------------------
# Profit/Loss Calculation
# ------------------------------
def calculate_profit_loss(initial_investment, current_value):
    return current_value - initial_investment

def get_data_with_rate_limit_handling(coin):
    retries = 3
    while retries > 0:
        try:
            data = get_bybit_historical_data(coin)
            return data
        except Exception as e:
            print(f"Hit API rate limit. Error: {e}. Retrying...")
            time.sleep(3)
            retries -= 1
    print("Failed to fetch data after 3 retries due to API rate limit.")
    return None

def calculate_best_performance():
    best_coin = None
    best_performance = float('-inf')
    for coin in list_of_coins:
        data = get_data_with_rate_limit_handling(coin)
        if data is not None and len(data) > 1:
            performance = (float(data[-1]['close']) - float(data[0]['open'])) * portfolio_values.get(coin, {}).get('amount', 0)
            if performance > best_performance:
                best_coin = coin
                best_performance = performance
    return best_coin, best_performance

# ------------------------------
# Display Functions
# ------------------------------
def display_portfolio_value(initial_investment):
    portfolio_values = update_portfolio_values()
    total_value = calculate_total_portfolio_value(portfolio_values)
    value_24_hours_ago = get_portfolio_days_ago(1)
    value_30_days_ago = get_portfolio_days_ago(30)
    save_portfolio_value(total_value)
    profit_loss = calculate_profit_loss(initial_investment, total_value)
    allocations = allocation()
    best_coin, best_performance = calculate_best_performance()

    print(f"{'Coin':<10}{'Allocation':<15}{'Allocation in USDT':>20}")
    print("-" * 47)
    for coin, alloc in allocations.items():
        alloc_usdt = (alloc / 100) * total_value
        print(f"{coin:<10}{alloc:.2f}%{alloc_usdt:>20.2f} USDT")
    print("-" * 47)

    print(f"Total portfolio value: {round(total_value, 2)} USDT")
    if value_24_hours_ago is not None:
        growth_24_hours = ((total_value - value_24_hours_ago) / value_24_hours_ago) * 100
        print(f"Growth in the last 24 hours: {round(growth_24_hours, 2)}%")
    else:
        print("Growth in the last 24 hours: Not enough data")
    if value_30_days_ago is not None:
        growth_30_days = ((total_value - value_30_days_ago) / value_30_days_ago) * 100
        print(f"Growth in the last 30 days: {round(growth_30_days, 2)}%")
    else:
        print("Growth in the last 30 days: Not enough data")

    print(f"Profit/Loss: {round(profit_loss, 2)} USDT")
    print(f"Best performer in 7 days: {best_coin}: +{round(best_performance, 2)} USDT")


# ------------------------------
# Main Execution
# ------------------------------
if __name__ == "__main__":
    initial_investment = get_initial_investment()
    display_portfolio_value(initial_investment)
