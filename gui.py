import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch stock data with added fallback fields
def fetch_stock_data():
    api_key = 'Nchnea48D4_2UF5ngByji3ygE5lB5fzl'

    sectors = {
        'tech': ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'AMD', 'INTC', 'CSCO', 'META', 'TSLA', 'CRM'],
        'healthcare': ['PFE', 'JNJ', 'MRK', 'ABBV', 'BMY', 'LLY', 'AMGN', 'GILD', 'ISRG', 'CVS'],
        'finance': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'AXP', 'BRK.B', 'V', 'MA'],
        'energy': ['XOM', 'CVX', 'SLB', 'COP', 'EOG', 'OXY', 'PXD', 'MRO', 'HES', 'FANG'],
        'consumer': ['DIS', 'NKE', 'KO', 'PEP', 'MCD', 'PG', 'WMT', 'CVS', 'ADBE', 'LOW'],
    }

    stocks = []
    for sector, symbols in sectors.items():
        for symbol in symbols:
            url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?apiKey={api_key}'
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if 'results' in data:
                    stock = data['results'][0]
                    stocks.append({
                        "ticker": symbol,
                        "sector": sector,
                        "open": stock.get('o', 0),
                        "close": stock.get('c', 0),
                        "high": stock.get('h', 0),
                        "low": stock.get('l', 0),
                        "volume": stock.get('v', 0),
                        "dividend_yield": round(random.uniform(0.01, 0.05), 2),
                        "pe_ratio": round(random.uniform(10, 30), 2),
                    })
            except:
                continue
    return stocks

# Scoring logic based on simple investment preferences
def score_stock(stock):
    score = 0
    # Favor lower P/E ratios
    if stock["pe_ratio"] < 20:
        score += 2
    elif stock["pe_ratio"] < 25:
        score += 1

    # Favor higher dividend yields
    if stock["dividend_yield"] > 0.03:
        score += 2
    elif stock["dividend_yield"] > 0.02:
        score += 1
    return score

# Create pie chart for sector distribution
def show_sector_distribution(stocks):
    sectors = {}
    for stock in stocks:
        sectors[stock["sector"]] = sectors.get(stock["sector"], 0) + 1

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sectors.values(), labels=sectors.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# Normalize sector names
sector_aliases = {
    'health care': 'healthcare',
    'health': 'healthcare',
    'technology': 'tech',
    'technical': 'tech',
    'consumer goods': 'consumer',
    'financial': 'finance',
    'fin': 'finance',
    'energy': 'energy',
    'tech': 'tech',
    'finance': 'finance',
    'consumer': 'consumer',
    'healthcare': 'healthcare'
}

# Main logic to generate portfolio
def generate_portfolio():
    marital_status = marital_status_var.get()
    num_children = int(children_entry.get() or 0)
    retirement_age = int(retirement_age_entry.get() or 65)
    saving_for_retirement = saving_for_retirement_var.get()
    comfortable_with_market = comfortable_with_market_var.get()
    has_debt = has_debt_var.get()
    
    # Fetch and normalize preferred sectors input
    input_sectors = preferred_sectors_var.get().strip().lower().split(',')
    normalized_sectors = [sector_aliases.get(s.strip(), s.strip()) for s in input_sectors]

    progress_bar.start()
    window.update_idletasks()
    time.sleep(1)

    stocks = fetch_stock_data()

    if normalized_sectors:
        filtered_stocks = [stock for stock in stocks if stock["sector"] in normalized_sectors]
    else:
        filtered_stocks = stocks

    if not filtered_stocks:
        messagebox.showinfo("No Matches", "No stocks found in preferred sectors. Using all sectors instead.")
        filtered_stocks = stocks

    # Score and sort
    for stock in filtered_stocks:
        stock["score"] = score_stock(stock)

    top_stocks = sorted(filtered_stocks, key=lambda x: x["score"], reverse=True)[:5]

    if not top_stocks:
        messagebox.showinfo("Error", "No valid stocks selected.")
        return

    portfolio_text = "Selected Stocks for Your Portfolio:\n\n"
    for stock in top_stocks:
        portfolio_text += (f"- {stock['ticker']} ({stock['sector'].capitalize()})\n"
                           f"   Score: {stock['score']} | P/E: {stock['pe_ratio']} | Yield: {stock['dividend_yield']} | "
                           f"Close: ${stock['close']:.2f}\n")

    portfolio_label.config(text=portfolio_text)
    show_sector_distribution(top_stocks)

    progress_bar.stop()

def on_generate_button_click():
    generate_portfolio()

# ==== Theme Logic ====
def set_theme(theme):
    style = ttk.Style()
    if theme == "dark":
        style.configure('TButton', background='#444', foreground='white', font=('Helvetica', 12))
        style.configure('TLabel', background='#333', foreground='white', font=('Helvetica', 14))
        style.configure('TFrame', background='#222')
        window.config(bg='#222')
    elif theme == "light":
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 12))
        style.configure('TLabel', background='#f7f7f7', foreground='black', font=('Helvetica', 14))
        style.configure('TFrame', background='#f7f7f7')
        window.config(bg='#f7f7f7')

def on_theme_change(selected_theme):
    set_theme(selected_theme)

# ==== UI Setup ====
window = tk.Tk()
window.title("Smart Portfolio Generator")
window.geometry("650x750")
window.config(bg="#f7f7f7")

tk.Label(window, text="Personal Financial Profile", font=("Helvetica", 18, "bold"), bg="#f7f7f7").pack(pady=20)

# Inputs
def add_labeled_input(label_text, variable=None, input_type='entry', options=None):
    tk.Label(window, text=label_text, font=("Helvetica", 12), bg="#f7f7f7").pack()
    if input_type == 'entry':
        entry = tk.Entry(window, font=("Helvetica", 12))
        entry.pack(pady=5)
        return entry
    elif input_type == 'dropdown':
        dropdown = ttk.Combobox(window, textvariable=variable, values=options, width=30)
        dropdown.pack(pady=5)
        return dropdown
    elif input_type == 'radio':
        frame = tk.Frame(window, bg="#f7f7f7")
        frame.pack()
        for val in options:
            tk.Radiobutton(frame, text=val.capitalize(), variable=variable, value=val, font=("Helvetica", 12), bg="#f7f7f7").pack(side='left')
    return None

# Personal financial profile inputs
marital_status_var = tk.StringVar(value="Single")
add_labeled_input("Marital Status", marital_status_var, 'dropdown', ["Single", "Married", "Divorced", "Widowed"])

children_entry = add_labeled_input("Number of Children/Dependents")
retirement_age_entry = add_labeled_input("Age of Retirement")

saving_for_retirement_var = tk.StringVar(value="no")
add_labeled_input("Have you started saving for retirement?", saving_for_retirement_var, 'radio', ['yes', 'no'])

comfortable_with_market_var = tk.StringVar(value="yes")
add_labeled_input("Are you comfortable with market ups and downs?", comfortable_with_market_var, 'radio', ['yes', 'no'])

has_debt_var = tk.StringVar(value="no")
add_labeled_input("Do you have significant debt?", has_debt_var, 'radio', ['yes', 'no'])

# Sector selection dropdown (updated)
preferred_sectors_var = tk.StringVar()
add_labeled_input("Preferred Sectors (e.g., tech, healthcare)", preferred_sectors_var, 'dropdown', ["tech", "healthcare", "finance", "energy", "consumer"])

# Theme selection dropdown
theme_dropdown = ttk.Combobox(window, values=["light", "dark"], state="readonly")
theme_dropdown.set("light")
theme_dropdown.bind("<<ComboboxSelected>>", lambda e: on_theme_change(theme_dropdown.get()))
theme_dropdown.pack(pady=10)

# Button and progress bar
tk.Button(window, text="Generate Portfolio", command=on_generate_button_click, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", width=25).pack(pady=20)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="indeterminate")
progress_bar.pack(pady=10)

portfolio_label = tk.Label(window, text="Selected Stocks for Your Portfolio:", font=("Helvetica", 14), bg="#f7f7f7", justify="left")
portfolio_label.pack(pady=10)

window.mainloop()
