import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import requests
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Stock Fetching ===
def fetch_stock_data():
    api_key = 'Nchnea48D4_2UF5ngByji3ygE5lB5fzl'
    sectors = {
        'tech': ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'AMD'],
        'healthcare': ['PFE', 'JNJ', 'MRK', 'ABBV', 'BMY'],
        'finance': ['JPM', 'BAC', 'WFC', 'C', 'GS'],
        'energy': ['XOM', 'CVX', 'SLB', 'COP', 'EOG'],
        'consumer': ['DIS', 'NKE', 'KO', 'PEP', 'MCD'],
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

def score_stock(stock):
    score = 0
    if stock["pe_ratio"] < 20:
        score += 2
    elif stock["pe_ratio"] < 25:
        score += 1
    if stock["dividend_yield"] > 0.03:
        score += 2
    elif stock["dividend_yield"] > 0.02:
        score += 1
    return score

def show_sector_distribution(stocks):
    sectors = {}
    for stock in stocks:
        sectors[stock["sector"]] = sectors.get(stock["sector"], 0) + 1

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sectors.values(), labels=sectors.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def save_portfolio_to_csv(stocks):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Ticker", "Sector", "Score", "P/E Ratio", "Dividend Yield", "Close"])
            for stock in stocks:
                writer.writerow([stock['ticker'], stock['sector'], stock['score'],
                                 stock['pe_ratio'], stock['dividend_yield'], stock['close']])
        messagebox.showinfo("Saved", f"Portfolio saved to:\n{file_path}")

def generate_portfolio():
    marital_status = marital_status_var.get()
    num_children = int(children_entry.get() or 0)
    retirement_age = int(retirement_age_entry.get() or 65)
    saving_for_retirement = saving_for_retirement_var.get()
    comfortable_with_market = comfortable_with_market_var.get()
    has_debt = has_debt_var.get()

    try:
        debt_amount = float(debt_amount_entry.get()) if has_debt == "yes" else 0
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid debt amount.")
        return

    input_sectors = preferred_sectors_var.get().strip().lower().split(',')
    normalized_sectors = [sector_aliases.get(s.strip(), s.strip()) for s in input_sectors]

    risk_score = 5
    risk_score += 1 if marital_status.lower() == "single" else -1
    risk_score -= 1 if num_children > 0 else 0
    risk_score += 1 if retirement_age > 60 else 0
    risk_score += 2 if comfortable_with_market == "yes" else -1
    risk_score += -2 if debt_amount > 50000 else -1 if debt_amount > 10000 else -0.5 if debt_amount > 0 else 1
    risk_score += -1 if saving_for_retirement == "no" else 0
    risk_score = max(1, min(10, round(risk_score)))

    progress_bar.start()
    window.update_idletasks()
    time.sleep(1)

    stocks = fetch_stock_data()
    filtered_stocks = [stock for stock in stocks if stock["sector"] in normalized_sectors] or stocks

    for stock in filtered_stocks:
        stock["score"] = score_stock(stock)

    top_stocks = sorted(filtered_stocks, key=lambda x: x["score"], reverse=True)[:5]

    if not top_stocks:
        messagebox.showinfo("Error", "No valid stocks selected.")
        return

    portfolio_text = f"Your Risk Score: {risk_score}/10\n\nTop Stocks:\n\n"
    for stock in top_stocks:
        portfolio_text += (f"{stock['ticker']} ({stock['sector'].capitalize()})\n"
                           f"  Score: {stock['score']} | P/E: {stock['pe_ratio']} | Yield: {stock['dividend_yield']} | "
                           f"Close: ${stock['close']:.2f}\n\n")

    portfolio_label.config(text=portfolio_text)
    save_button.config(command=lambda: save_portfolio_to_csv(top_stocks))
    save_button.pack(pady=10)
    chart_frame.pack()
    show_sector_distribution(top_stocks)
    progress_bar.stop()

# === Theme ===
def set_theme(theme):
    bg = "#f7f7f7" if theme == "light" else "#2e2e2e"
    fg = "#000000" if theme == "light" else "#ffffff"
    entry_bg = "white" if theme == "light" else "#3a3a3a"
    entry_fg = "black" if theme == "light" else "#ffffff"

    window.config(bg=bg)
    input_frame.config(bg=bg)
    chart_frame.config(bg=bg)
    portfolio_label.config(bg=bg, fg=fg)

    for widget in window.winfo_children() + input_frame.winfo_children():
        cls = widget.__class__.__name__
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass

        # Entry and Text widgets
        if isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.config(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)

        # Buttons
        if isinstance(widget, tk.Button):
            widget.config(bg="#555555" if theme == "dark" else "#e0e0e0",
                          fg=fg, activebackground="#777777" if theme == "dark" else "#d0d0d0")

    # Update ttk styles
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TCombobox",
                    fieldbackground=entry_bg,
                    background=entry_bg,
                    foreground=entry_fg)

    style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)

    style.configure("TButton",
                    background=entry_bg,
                    foreground=entry_fg)

    style.configure("TLabel", background=bg, foreground=fg)

    style.configure("TProgressbar", troughcolor=bg, background="#4CAF50")

    debt_amount_label.config(bg=bg, fg=fg)

# === UI ===
window = tk.Tk()
window.title("Smart Portfolio Generator")
window.geometry("700x900")
window.config(bg="#f7f7f7")

input_frame = tk.Frame(window, bg="#f7f7f7")
input_frame.pack(pady=10)

def add_labeled_input(text, variable=None, type='entry', options=None):
    tk.Label(input_frame, text=text, font=("Helvetica", 12), bg="#f7f7f7", fg="#000000").pack()
    
    if type == 'entry':
        entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="white", fg="black")
        entry.pack(pady=5)
        return entry

    elif type == 'dropdown':
        cb = ttk.Combobox(input_frame, textvariable=variable, values=options, width=30)
        cb.pack(pady=5)
        return cb

    elif type == 'radio':
        frame = tk.Frame(input_frame, bg="#f7f7f7")
        frame.pack(pady=5)

        buttons = []

        for opt in options:
            btn = tk.Radiobutton(frame,
                                 text=opt.capitalize(),
                                 variable=variable,
                                 value=opt,
                                 indicatoron=0,
                                 width=10,
                                 font=("Helvetica", 12, "bold"),
                                 bg="#cccccc",
                                 fg="black",
                                 selectcolor="#4CAF50",
                                 relief="raised",
                                 bd=2,
                                 padx=10,
                                 pady=5,
                                 activebackground="#4CAF50")

            btn.variable = variable
            btn.pack(side="left", padx=5)
            buttons.append(btn)

        frame.radio_buttons = buttons
        return frame

sector_aliases = {
    'health care': 'healthcare', 'health': 'healthcare',
    'technology': 'tech', 'technical': 'tech',
    'consumer goods': 'consumer', 'financial': 'finance',
    'fin': 'finance', 'energy': 'energy',
    'tech': 'tech', 'finance': 'finance',
    'consumer': 'consumer', 'healthcare': 'healthcare'
}

marital_status_var = tk.StringVar(value="Single")
add_labeled_input("Marital Status", marital_status_var, 'dropdown', ["Single", "Married", "Divorced"])

children_entry = add_labeled_input("Number of Children/Dependents")
retirement_age_entry = add_labeled_input("Retirement Age")

saving_for_retirement_var = tk.StringVar(value="no")
add_labeled_input("Saving for Retirement?", saving_for_retirement_var, 'radio', ['yes', 'no'])

comfortable_with_market_var = tk.StringVar(value="yes")
add_labeled_input("Comfortable with Market Fluctuations?", comfortable_with_market_var, 'radio', ['yes', 'no'])

has_debt_var = tk.StringVar(value="no")
add_labeled_input("Do you have debt?", has_debt_var, 'radio', ['yes', 'no'])

debt_amount_label = tk.Label(input_frame, text="How much debt (USD)?", font=("Helvetica", 12), bg="#f7f7f7")
debt_amount_entry = tk.Entry(input_frame, font=("Helvetica", 12))

def toggle_debt_amount(*_):
    if has_debt_var.get() == "yes":
        debt_amount_label.pack()
        debt_amount_entry.pack(pady=5)
    else:
        debt_amount_label.pack_forget()
        debt_amount_entry.pack_forget()

has_debt_var.trace_add("write", toggle_debt_amount)

preferred_sectors_var = tk.StringVar()
add_labeled_input("Preferred Sectors (comma-separated)", preferred_sectors_var, 'entry')

portfolio_label = tk.Label(window, text="Your Generated Portfolio will appear here.", font=("Helvetica", 12), bg="#f7f7f7", fg="#000000")
portfolio_label.pack(pady=10)

save_button = tk.Button(window, text="Save Portfolio", font=("Helvetica", 12), command=save_portfolio_to_csv)
chart_frame = tk.Frame(window)

generate_button = tk.Button(window, text="Generate Portfolio", font=("Helvetica", 12), command=generate_portfolio)
generate_button.pack(pady=10)

progress_bar = ttk.Progressbar(window, mode="indeterminate")
progress_bar.pack(pady=10)

# === Theme Toggle ===
current_theme = tk.StringVar(value="light")

def toggle_theme():
    new_theme = "dark" if current_theme.get() == "light" else "light"
    current_theme.set(new_theme)
    theme_toggle_button.config(text=f"Switch to {'Light' if new_theme == 'dark' else 'Dark'} Mode")
    set_theme(new_theme)

theme_toggle_button = tk.Button(window, text="Switch to Dark Mode", font=("Helvetica", 12), command=toggle_theme)
theme_toggle_button.pack(pady=5)

window.mainloop()
