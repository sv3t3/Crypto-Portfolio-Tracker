from portfolio_manager import update_portfolio_values
import sys
import requests
import os
from datetime import datetime

project_folder = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script file
database_folder = os.path.join(project_folder, '..', 'database') # Go up one level to the MyCryptoPortfolio folder and then into the database folder
filename = os.path.join(database_folder, 'portfolio_value.txt') # The filename is portfolio_value.txt in the database folder

# The filename for the initial investment is initial_investment.txt in the database folder
initial_investment_filename = os.path.join(database_folder, 'initial_investment.txt')


# Define the conversion function - which currency to convert to USDT
def convert_eur_to_usdt(amount_in_eur):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    eur_to_usd_rate = response.json()['rates']['USD']
    amount_in_usd = amount_in_eur * eur_to_usd_rate
    return amount_in_usd

# Function for total portfolio value
def calculate_total_portfolio_value(portfolio_values):
    total_value = 0
    for coin, data in portfolio_values.items():
        total_value += data['value']
    return total_value

def save_portfolio_value(total_value):
    with open(filename, 'a') as f:
        f.write(f'{datetime.now()}: {total_value:.2f}\n')

# Live growth wanna be
def get_last_portfolio_value():
    print(f'File path: {filename}')  # Print the file path
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        print(f'Last line: {last_line}')
        last_value = last_line.split(": ")[1].strip()  # Strip whitespace characters from last_value
        print(f'Last value: {last_value}')
        return float(last_value)

def get_initial_investment():
    # If the initial investment file exists, read the initial investment from it
    if os.path.exists(initial_investment_filename):
        with open(initial_investment_filename, 'r') as f:
            return float(f.read())
    # Otherwise, ask the user for the initial investment - REMEMBER TO CHANGE CODE TO MAKE HISTORY LOG FOR INVESTMENT
    else:
        currency = input("Enter the currency of your initial investment (EUR, USD): ")
        initial_investment = float(input("Your initial investment: "))  # Use float() instead of int() - 1635.08
        # Convert the initial investment to USDT if the currency is EUR
        if currency.upper() == 'EUR':
            initial_investment = convert_eur_to_usdt(initial_investment)
        # Save the initial investment to the file
        with open(initial_investment_filename, 'w') as f:
            f.write(str(initial_investment))
        return initial_investment

# Get allocation for each coin in the portfolio
def allocation():
    portfolio_values = update_portfolio_values()
    total_value = sum(coin['value'] for coin in portfolio_values.values())
    allocation = {coin: (value['value'] / total_value) * 100 for coin, value in portfolio_values.items()} # Percentage allocation
    return allocation

# Portfolios p/l
def calculate_profit_loss(initial_investment, current_value):
    return current_value - initial_investment

# Terminal display of info
def display_portfolio_value(initial_investment):
    portfolio_values = update_portfolio_values()
    print(f'Portfolio values: {portfolio_values}')  # Print the portfolio values
    total_value = calculate_total_portfolio_value(portfolio_values)
    print(f'Total value: {total_value}')  # Print the total value

    save_portfolio_value(total_value)
    profit_loss = calculate_profit_loss(initial_investment, total_value)

    # Better display of the portfolio allocation
    allocations = allocation()
    print(f"{'Coin':<10}{'Allocation':<15}{'Allocation in USDT':>20}")
    print("-" * 47)
    for coin, alloc in allocations.items():
        alloc_usdt = (alloc / 100) * total_value
        print(f"{coin:<10}{alloc:.2f}%{alloc_usdt:>20.2f} USDT") # More of a chart
    print("-" * 47)

    last_total_value = get_last_portfolio_value()
    if last_total_value is not None:
        growth_since_last_run = ((total_value - last_total_value) / last_total_value) * 100
        print(f"Growth since last run: {growth_since_last_run:.2f}%")

    # Print portfolio value and profit/loss
    print(f"Total portfolio value: {round(total_value, 2)} USDT")
    print(f"Profit/Loss: {round(profit_loss, 2)} USDT")

if __name__ == "__main__":
    initial_investment = get_initial_investment()
    display_portfolio_value(initial_investment)