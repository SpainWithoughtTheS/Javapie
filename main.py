import json
from portfolio_logic import select_stocks
from stock_data import fetch_stock_data

def run_portfolio_generator():
    marital_status = marital_status_var.get()
    num_children = int(children_entry.get())
    retirement_age = int(retirement_age_entry.get())
    saving_for_retirement = saving_for_retirement_var.get()
    comfortable_with_market = comfortable_with_market_var.get()
    has_debt = has_debt_var.get()
    preferred_sectors = preferred_sectors_entry.get().split(',')
    
    # Now generate portfolio based on the input gathered from GUI
    generate_portfolio(marital_status, num_children, retirement_age, saving_for_retirement, comfortable_with_market, has_debt, preferred_sectors)

    # Calculate risk score based on answers
    risk_score = calculate_risk_score(answers)

    # Fetch stock data from Polygon.io
    stock_data = fetch_stock_data()

    # Select stocks based on user profile and risk score
    selected_stocks = select_stocks(answers, risk_score, stock_data)

    print("Selected Stocks for Your Portfolio:")
    for stock in selected_stocks:
        print(f"- {stock['ticker']}")

def calculate_risk_score(answers):
    # Simplified risk score logic for demonstration purposes
    risk_score = 10
    if answers["comfortable_with_market_ups_and_downs"]:
        risk_score -= 3
    if answers["significant_debt"]:
        risk_score -= 2
    if not answers["started_saving_for_retirement"]:
        risk_score -= 1
    if answers["marital_status"] == "widowed":
        risk_score -= 1
    return risk_score

if __name__ == "__main__":
    run_portfolio_generator()
