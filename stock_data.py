import requests
import tkinter as tk
from tkinter import messagebox


# Function to fetch stock data from Polygon API
def fetch_stock_data():
    api_key = 'Nchnea48D4_2UF5ngByji3ygE5lB5fzl'
    symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']  # Add your preferred stocks here
    stocks = []
    
    for symbol in symbols:
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?apiKey={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            stock = data['results'][0]
            stocks.append({
                "ticker": stock['T'],
                "open": stock['o'],
                "close": stock['c'],
                "high": stock['h'],
                "low": stock['l'],
                "volume": stock['v'],
                "dividend_yield": 0.03,  # Example of adding a dividend yield field
                "pe_ratio": 12.5  # Example of adding a P/E ratio field
            })
    
    return stocks


# Function to select stocks based on user profile and risk tolerance
def select_stocks(profile, risk_score, stock_data):
    selected_stocks = []
    for stock in stock_data:
        if stock["pe_ratio"] < 20 and stock["dividend_yield"] >= 0.02:  # Example criteria
            selected_stocks.append(stock)
    return selected_stocks


# Portfolio generation logic
def generate_portfolio():
    profile = {
        "marital_status": "single",  # example profile info
        "children": 2,
        "retirement_age": 65,
        "debt": "no",
        "risk_tolerance": "low",
        "preferred_sectors": ["tech"]
    }

    # Fetch stock data from the API
    stock_data = fetch_stock_data()

    # For now, assuming risk_score = 5, adjust accordingly
    risk_score = 5
    portfolio = select_stocks(profile, risk_score, stock_data)

    # Display selected portfolio
    if portfolio:
        portfolio_info = "\n".join([f"- {stock['ticker']}" for stock in portfolio])
        messagebox.showinfo("Portfolio Generated", f"Your Portfolio:\n{portfolio_info}")
    else:
        messagebox.showwarning("No Stocks Selected", "No stocks match your profile criteria.")


# GUI Setup using Tkinter
def setup_gui():
    root = tk.Tk()
    root.title("Stock Portfolio Generator")

    # Setup GUI elements
    generate_button = tk.Button(root, text="Generate Portfolio", command=generate_portfolio)
    generate_button.pack(pady=20)

    # Run the GUI loop
    root.mainloop()


# Run the GUI
if __name__ == "__main__":
    setup_gui()
