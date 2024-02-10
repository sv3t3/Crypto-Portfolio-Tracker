MyCryptoPortfolio

MyCryptoPortfolio is a Python application for managing your cryptocurrency portfolio. It interacts with the Bybit API to fetch the latest prices of your coins and calculate the total value of your portfolio.

Features:
    Fetches the latest prices of your coins from the Bybit API
    Calculates the total value of your portfolio in USDT
    Separates your coins into two lists: those that end with 'USDT' and those that don't

Setup
    1. Clone the repository:
        git clone https://github.com/yourusername/MyCryptoPortfolio.git
    2. Install the required Python packages:
        pip install -r requirements.txt
    3. Set your Bybit API key and secret as environment variables:
        export BYBIT_API_KEY=yourapikey 
        export BYBIT_API_SECRET=yoursecret
        
    Replace yourapikey and yoursecret with your actual Bybit API key and secret.

Usage
    Run the portfolio_manager.py script to fetch the latest prices and calculate the value of your portfolio:
        python portfolio_manager.py

Please replace https://github.com/yourusername/MyCryptoPortfolio.git with the actual URL of your repository, and update the setup and usage instructions as necessary based on your project's requirements.