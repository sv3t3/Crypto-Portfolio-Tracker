from portfolio_manager import fetch_bybit_ticker, update_portfolio_values
import sys
import requests

# Define the conversion function
def convert_eur_to_usdt(amount_in_eur):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    eur_to_usd_rate = response.json()['rates']['USD']
    amount_in_usd = amount_in_eur * eur_to_usd_rate
    return amount_in_usd

# Function to calculate the total value of the portfolio
def calculate_total_portfolio_value(portfolio_values):
    total_value = 0
    for coin, data in portfolio_values.items():
        total_value += data['value']
    return total_value

# Get allocation for each coin in the portfolio
def allocation():
    portfolio_values = update_portfolio_values()
    total_value = sum(coin['value'] for coin in portfolio_values.values())
    allocation = {coin: (value['value'] / total_value) * 100 for coin, value in portfolio_values.items()}
    return allocation

def display_portfolio_value(initial_investment):
    portfolio_values = update_portfolio_values()
    total_value = calculate_total_portfolio_value(portfolio_values)
    profit_loss = calculate_profit_loss(initial_investment, total_value)

    allocations = allocation()
    for coin, alloc in allocations.items():
        print(f'{coin}: {alloc:.2f}%')

    # Print portfolio value and profit/loss
    print(f"Total portfolio value: {round(total_value, 2)} USDT")
    print(f"Profit/Loss: {round(profit_loss, 2)} USDT")

def calculate_profit_loss(initial_investment, current_value):
    return current_value - initial_investment

# Get the initial investment and its currency
currency = input("Enter the currency of your initial investment (EUR, USD): ")
initial_investment = float(input("Your initial investment: "))  # Use float() instead of int()

# Convert the initial investment to USDT if the currency is EUR
if currency.upper() == 'EUR':
    initial_investment = convert_eur_to_usdt(initial_investment)

if __name__ == "__main__":
    display_portfolio_value(initial_investment)