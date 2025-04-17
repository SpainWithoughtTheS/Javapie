import random
import pandas as pd

# Sample dataset of stocks (real values can be pulled from APIs later)
STOCK_DATA = [
    {"name": "Apple Inc.", "ticker": "AAPL", "sector": "Tech", "growth_rate": 0.12, "momentum": 0.8, "pe_ratio": 25, "market_cap": "Large", "dividend_yield": 0.006, "de_ratio": 1.5, "high_52": 190},
    {"name": "Microsoft", "ticker": "MSFT", "sector": "Tech", "growth_rate": 0.10, "momentum": 0.75, "pe_ratio": 30, "market_cap": "Large", "dividend_yield": 0.009, "de_ratio": 0.6, "high_52": 330},
    {"name": "Pfizer", "ticker": "PFE", "sector": "Healthcare", "growth_rate": 0.05, "momentum": 0.3, "pe_ratio": 15, "market_cap": "Large", "dividend_yield": 0.045, "de_ratio": 0.5, "high_52": 55},
    {"name": "Tesla", "ticker": "TSLA", "sector": "Consumer Discretionary", "growth_rate": 0.25, "momentum": 0.9, "pe_ratio": 90, "market_cap": "Large", "dividend_yield": 0.0, "de_ratio": 1.2, "high_52": 300},
    {"name": "Duke Energy", "ticker": "DUK", "sector": "Utilities", "growth_rate": 0.03, "momentum": 0.2, "pe_ratio": 18, "market_cap": "Large", "dividend_yield": 0.04, "de_ratio": 1.0, "high_52": 105},
    # Add more for each sector...
]

SECTORS = ["Tech", "Healthcare", "Consumer Discretionary", "Utilities", "Materials"]

def get_user_input():
    print("Welcome to the Portfolio Builder!\n")
    marital_status = input("Are you married, single, divorced, or widowed? ").lower()
    has_dependents = input("Do you have children or dependents? (yes/no) ").lower() == "yes"
    retirement_age = int(input("At what age do you plan to retire? "))
    current_age = int(input("What is your current age? "))
    risk_pref = input("How do you feel about risk? (low, medium, high): ").lower()
    has_debt = input("Do you currently have significant debt? (yes/no) ").lower() == "yes"
    sector_preference = input("Which sector(s) are you most interested in? (comma-separated): ").title().split(",")
    invest_years = int(input("How many years do you plan to invest? (e.g., 1, 5, 10): "))
    
    return {
        "marital_status": marital_status,
        "has_dependents": has_dependents,
        "retirement_age": retirement_age,
        "current_age": current_age,
        "risk_pref": risk_pref,
        "has_debt": has_debt,
        "sector_preference": [s.strip() for s in sector_preference],
        "invest_years": invest_years
    }

def calculate_risk_score(user):
    score = 5
    if user["risk_pref"] == "low": score -= 2
    elif user["risk_pref"] == "high": score += 2

    if user["has_dependents"]: score -= 1
    if user["has_debt"]: score -= 1
    if user["retirement_age"] - user["current_age"] > 20: score += 1
    if user["marital_status"] == "single": score += 1

    return max(1, min(score, 10))

def select_stocks(risk_score, sector_preference):
    df = pd.DataFrame(STOCK_DATA)
    
    if sector_preference:
        df = df[df["sector"].isin(sector_preference)]
    
    if risk_score >= 8:
        df = df[df["growth_rate"] > 0.1]
    elif risk_score >= 5:
        df = df[df["pe_ratio"] < 35]
    else:
        df = df[(df["dividend_yield"] > 0.03) & (df["de_ratio"] < 1.5)]

    selected = []
    for sector in SECTORS:
        sector_stocks = df[df["sector"] == sector]
        picks = sector_stocks.sample(min(5, len(sector_stocks)), replace=False)
        selected.extend(picks.to_dict(orient="records"))
    
    return selected[:25]

def explain_stock(stock, risk_score):
    reasons = []
    if risk_score >= 8 and stock["growth_rate"] > 0.15:
        reasons.append("high growth potential")
    if risk_score <= 4 and stock["dividend_yield"] > 0.03:
        reasons.append("stable income through dividends")
    if stock["pe_ratio"] < 20:
        reasons.append("undervalued based on P/E ratio")
    if stock["momentum"] > 0.7:
        reasons.append("strong recent performance")
    if stock["market_cap"] == "Large":
        reasons.append("more stability due to size")
    return ", ".join(reasons)

def display_portfolio(stocks, invest_years, risk_score):
    print("\nYour Personalized Portfolio:\n")
    for stock in stocks:
        explanation = explain_stock(stock, risk_score)
        print(f"{stock['name']} ({stock['ticker']}) - Sector: {stock['sector']}")
        print(f"  Growth: {stock['growth_rate']*100:.1f}% | Momentum: {stock['momentum']}")
        print(f"  P/E: {stock['pe_ratio']} | Market Cap: {stock['market_cap']} | Div. Yield: {stock['dividend_yield']*100:.2f}%")
        print(f"  52-Week High: ${stock['high_52']} | Reason: {explanation}\n")

    print(f"Estimated Return over {invest_years} year(s):")
    estimated_return = round(1 + (0.05 + risk_score * 0.01) * invest_years, 2)
    print(f"Your portfolio could grow approximately {estimated_return * 100:.1f}% over {invest_years} years.\n")

def main():
    user_data = get_user_input()
    risk_score = calculate_risk_score(user_data)
    print(f"\nCalculated Risk Tolerance Score: {risk_score}/10")

    portfolio = select_stocks(risk_score, user_data["sector_preference"])
    display_portfolio(portfolio, user_data["invest_years"], risk_score)

if __name__ == "__main__":
    main()
