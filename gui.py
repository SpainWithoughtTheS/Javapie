import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import requests

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

# Stock selection logic using real data (e.g., API data)
def generate_portfolio():
    marital_status = marital_status_var.get()
    num_children = int(children_entry.get())
    retirement_age = int(retirement_age_entry.get())
    saving_for_retirement = saving_for_retirement_var.get()
    comfortable_with_market = comfortable_with_market_var.get()
    has_debt = has_debt_var.get()
    preferred_sectors = preferred_sectors_entry.get().split(',')

    # Display progress bar during portfolio generation
    progress_bar.start()
    window.update_idletasks()

    # Simulate a delay for the portfolio generation (use actual logic here)
    time.sleep(2)

    # Fetch stock data (from API)
    stocks = fetch_stock_data()

    # Select a few random stocks from the list
    selected_stocks = random.sample(stocks, min(5, len(stocks)))

    # If no stocks match (which shouldn't happen now), show a message
    if not selected_stocks:
        messagebox.showinfo("No Matches", "No stocks were selected.")
    else:
        # Display selected stocks with their financial metrics
        portfolio_text = "Selected Stocks for Your Portfolio:\n"
        for stock in selected_stocks:
            portfolio_text += (f"- {stock['ticker']} | P/E: {stock['pe_ratio']} | "
                               f"Dividend Yield: {stock['dividend_yield']} | "
                               f"Close Price: {stock['close']}\n")
        portfolio_label.config(text=portfolio_text)

    # Stop the progress bar
    progress_bar.stop()

# Button click event handler
def on_generate_button_click():
    generate_portfolio()

# Set up the main window
window = tk.Tk()
window.title("Portfolio Generator")
window.geometry("600x500")
window.config(bg="#f7f7f7")

# Title and user inputs for financial questionnaire
title_label = tk.Label(window, text="Personal Financial Profile", font=("Helvetica", 18, "bold"), fg="#333", bg="#f7f7f7")
title_label.pack(pady=20)

# Marital Status Dropdown
marital_status_label = tk.Label(window, text="Marital Status", font=("Helvetica", 12), bg="#f7f7f7")
marital_status_label.pack()
marital_status_var = tk.StringVar(value="Single")
marital_status_dropdown = ttk.Combobox(window, textvariable=marital_status_var, values=["Single", "Married", "Divorced", "Widowed"], width=30)
marital_status_dropdown.pack(pady=5)

# Number of Children
children_label = tk.Label(window, text="Number of Children/Dependents", font=("Helvetica", 12), bg="#f7f7f7")
children_label.pack()
children_entry = tk.Entry(window, font=("Helvetica", 12))
children_entry.pack(pady=5)

# Retirement Age
retirement_age_label = tk.Label(window, text="Age of Retirement", font=("Helvetica", 12), bg="#f7f7f7")
retirement_age_label.pack()
retirement_age_entry = tk.Entry(window, font=("Helvetica", 12))
retirement_age_entry.pack(pady=5)

# Have you started saving for retirement?
saving_for_retirement_label = tk.Label(window, text="Have you started saving for retirement? (yes/no)", font=("Helvetica", 12), bg="#f7f7f7")
saving_for_retirement_label.pack()
saving_for_retirement_var = tk.StringVar(value="no")
saving_for_retirement_yes = tk.Radiobutton(window, text="Yes", variable=saving_for_retirement_var, value="yes", font=("Helvetica", 12), bg="#f7f7f7")
saving_for_retirement_no = tk.Radiobutton(window, text="No", variable=saving_for_retirement_var, value="no", font=("Helvetica", 12), bg="#f7f7f7")
saving_for_retirement_yes.pack()
saving_for_retirement_no.pack()

# Comfortable with market ups and downs?
comfortable_with_market_label = tk.Label(window, text="Are you comfortable with market ups and downs? (yes/no)", font=("Helvetica", 12), bg="#f7f7f7")
comfortable_with_market_label.pack()
comfortable_with_market_var = tk.StringVar(value="yes")
comfortable_with_market_yes = tk.Radiobutton(window, text="Yes", variable=comfortable_with_market_var, value="yes", font=("Helvetica", 12), bg="#f7f7f7")
comfortable_with_market_no = tk.Radiobutton(window, text="No", variable=comfortable_with_market_var, value="no", font=("Helvetica", 12), bg="#f7f7f7")
comfortable_with_market_yes.pack()
comfortable_with_market_no.pack()

# Do you have significant debt?
has_debt_label = tk.Label(window, text="Do you have significant debt? (yes/no)", font=("Helvetica", 12), bg="#f7f7f7")
has_debt_label.pack()
has_debt_var = tk.StringVar(value="no")
has_debt_yes = tk.Radiobutton(window, text="Yes", variable=has_debt_var, value="yes", font=("Helvetica", 12), bg="#f7f7f7")
has_debt_no = tk.Radiobutton(window, text="No", variable=has_debt_var, value="no", font=("Helvetica", 12), bg="#f7f7f7")
has_debt_yes.pack()
has_debt_no.pack()

# Preferred sectors
preferred_sectors_label = tk.Label(window, text="Preferred Sectors (comma-separated, e.g., tech, healthcare)", font=("Helvetica", 12), bg="#f7f7f7")
preferred_sectors_label.pack()
preferred_sectors_entry = tk.Entry(window, font=("Helvetica", 12))
preferred_sectors_entry.pack(pady=5)

# Generate Portfolio Button
generate_button = tk.Button(window, text="Generate Portfolio", command=on_generate_button_click, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", width=20)
generate_button.pack(pady=20)

# Progress Bar for Animation
progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="indeterminate")
progress_bar.pack(pady=10)

# Label to display selected stocks
portfolio_label = tk.Label(window, text="Selected Stocks for Your Portfolio:", font=("Helvetica", 14, "bold"), bg="#f7f7f7")
portfolio_label.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
