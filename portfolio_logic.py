def select_stocks(answers, risk_score, stock_data):
    selected_stocks = []

    for stock in stock_data:
        if match_profile(stock, risk_score):
            selected_stocks.append(stock)

    return selected_stocks

def match_profile(stock, risk_score):
    try:
        # Assuming stock data has the dividend_yield key among others
        if stock["dividend_yield"] >= 0.02 and stock["pe_ratio"] < 15:
            return True
        else:
            return False
    except KeyError:
        # Handle missing 'dividend_yield' key
        return False
