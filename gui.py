import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import requests
import csv
import json
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

def save_profile_to_json(profile_data):
    # Ask for a filename to save the JSON file
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(profile_data, f, indent=4)
            messagebox.showinfo("Success", "Profile saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving profile: {e}")


def load_profile_from_json():
    # Ask for a file to load the JSON profile
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                profile_data = json.load(f)
                display_profile(profile_data)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")


def display_profile(profile_data):
    # Clear any existing widgets
    for widget in profile_frame.winfo_children():
        widget.destroy()

    # Display profile information
    name_label = tk.Label(profile_frame, text=f"Name: {profile_data.get('name', 'N/A')}")
    name_label.pack(pady=5)
    
    age_label = tk.Label(profile_frame, text=f"Age: {profile_data.get('age', 'N/A')}")
    age_label.pack(pady=5)

    email_label = tk.Label(profile_frame, text=f"Email: {profile_data.get('email', 'N/A')}")
    email_label.pack(pady=5)


def generate_sample_profile():
    profile_data = {
        "name": name_entry.get(),
        "age": age_entry.get(),
        "email": email_entry.get()
    }
    save_profile_to_json(profile_data)


root = tk.Tk()
root.title("Profile Manager")
root.geometry("400x300")

name_label = tk.Label(root, text="Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

age_label = tk.Label(root, text="Age:")
age_label.pack(pady=5)
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

email_label = tk.Label(root, text="Email:")
email_label.pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

# Create a frame to display loaded profile data
profile_frame = tk.Frame(root)
profile_frame.pack(pady=20)

# Button to generate and save JSON profile
generate_button = tk.Button(root, text="Generate JSON", command=generate_sample_profile)
generate_button.pack(pady=10)

# Button to load and display JSON profile
load_button = tk.Button(root, text="Load JSON Profile", command=load_profile_from_json)
load_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

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

    # Get age and adjust risk score
    try:
        age = int(age_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid age.")
        return

    risk_score = 5
    risk_score += 1 if marital_status.lower() == "single" else -1
    risk_score -= 1 if num_children > 0 else 0
    risk_score += 1 if retirement_age > 60 else 0
    risk_score += 2 if comfortable_with_market == "yes" else -1
    risk_score += -2 if debt_amount > 50000 else -1 if debt_amount > 10000 else -0.5 if debt_amount > 0 else 1
    risk_score += -1 if saving_for_retirement == "no" else 0

    # Adjust risk score based on age
    if age < 30:
        risk_score += 2  # Higher risk tolerance for younger people
    elif age > 50:
        risk_score -= 2  # Lower risk tolerance for older people

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
    chart_frame.pack(side="top", padx=20, pady=20)
    show_sector_distribution(top_stocks)
    progress_bar.stop()

# === Theme ===
def set_theme(theme):
    style = ttk.Style()
    
    if theme == "light":
        bg = "#f7f7f7"
        fg = "#000000"
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground=bg, background=bg, foreground=fg)
        style.configure("TProgressbar", troughcolor=bg, background="#4CAF50")
    else:
        bg = "#2e2e2e"
        fg = "#ffffff"
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=bg, background=bg, foreground=fg)
        style.configure("TProgressbar", troughcolor=bg, background="#4CAF50")

    window.config(bg=bg)
    chart_frame.config(bg=bg)
    portfolio_label.config(bg=bg, fg=fg)
    input_frame.config(bg=bg)
    
    for widget in input_frame.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
            try:
                widget.config(bg=bg, fg=fg)
            except:
                pass

    debt_amount_label.config(bg=bg, fg=fg)

# === Placeholder Chart ===
def show_example_stock_graph():
    symbols = ['AAPL', 'GOOG', 'PFE']
    api_key = 'Nchnea48D4_2UF5ngByji3ygE5lB5fzl'
    fig, ax = plt.subplots(figsize=(6, 4))

    for symbol in symbols:
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-04-10/2024-04-17?apiKey={api_key}'
        try:
            response = requests.get(url)
            data = response.json()
            if 'results' in data:
                closes = [day['c'] for day in data['results']]
                dates = [day['t'] for day in data['results']]
                readable_dates = [time.strftime('%m-%d', time.gmtime(ts / 1000)) for ts in dates]
                ax.plot(readable_dates, closes, label=symbol)
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")

    ax.set_title("Recent Stock Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# === UI ===
window = tk.Tk()
window.title("Smart Portfolio Generator")
window.geometry("900x900")
window.config(bg="#f7f7f7")

canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas, bg="#f7f7f7")

canvas.create_window((0, 0), window=frame, anchor="nw")
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

input_frame = tk.Frame(frame, bg="#f7f7f7")
input_frame.pack(pady=10)

def add_labeled_input(text, variable=None, type='entry', options=None):
    tk.Label(input_frame, text=text, font=("Helvetica", 12),
             bg=window["bg"], fg="#000000" if window["bg"] == "#f7f7f7" else "#ffffff").pack()
    
    if type == 'entry':
        entry = tk.Entry(input_frame, font=("Helvetica", 12))
        entry.pack(pady=5)
        return entry

    elif type == 'dropdown':
        cb = ttk.Combobox(input_frame, textvariable=variable, values=options, width=30)
        cb.pack(pady=5)
        return cb

    elif type == 'radio':
        bg = window["bg"]
        fg = "#000000" if bg == "#f7f7f7" else "#ffffff"

        frame = tk.Frame(input_frame, bg=bg)
        frame.pack()
        buttons = []
        for opt in options:
            rb = tk.Radiobutton(frame, text=opt.capitalize(), variable=variable, value=opt,
                                font=("Helvetica", 12), bg=bg, fg=fg,
                                selectcolor=bg, activebackground=bg, activeforeground=fg)
            rb.pack(side='left')
            buttons.append(rb)
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

# Age input
age_entry = add_labeled_input("Age")

theme_dropdown = ttk.Combobox(window, values=["light", "dark"], state="readonly")
theme_dropdown.set("light")
theme_dropdown.bind("<<ComboboxSelected>>", lambda e: set_theme(theme_dropdown.get()))
theme_dropdown.pack(pady=10)

tk.Button(frame, text="Generate Portfolio", command=generate_portfolio, font=("Helvetica", 14, "bold"),
          bg="#4CAF50", fg="white", width=25).pack(pady=15)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="indeterminate")
progress_bar.pack(pady=10)

portfolio_label = tk.Label(frame, text="", font=("Helvetica", 11), bg="#f7f7f7", justify="left")
portfolio_label.pack(pady=10)

save_button = tk.Button(frame, text="Save Portfolio to CSV", font=("Helvetica", 12), bg="#2196F3", fg="white")

chart_frame = tk.Frame(frame, bg="#f7f7f7")
show_example_stock_graph() # Show placeholder chart here
chart_frame.pack(side="top", padx=20, pady=20)

set_theme("light")
window.mainloop()