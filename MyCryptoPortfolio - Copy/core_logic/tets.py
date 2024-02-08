import requests

def convert_eur_to_usdt(amount_in_eur):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    eur_to_usd_rate = response.json()['rates']['USD']
    amount_in_usd = amount_in_eur * eur_to_usd_rate

    # Since USDT is a stablecoin pegged to the value of the USD, its value is almost always equal to 1 USD.
    return amount_in_usd

amount_in_eur = float(input("Enter the amount in EUR: "))
amount_in_usdt = convert_eur_to_usdt(amount_in_eur)

print(f"{amount_in_eur} EUR is approximately equal to {amount_in_usdt} USDT.")