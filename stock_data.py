def fetch_stock_data():
    api_key = 'Nchnea48D4_2UF5ngByji3ygE5lB5fzl'
    
    # Expanded list of tickers across multiple sectors
    symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'PFE', 'JNJ', 'DUK', 'NUE', 'CVX']

    # Map of tickers to their respective sectors
    SECTOR_MAP = {
        'AAPL': 'Tech',
        'GOOG': 'Tech',
        'MSFT': 'Tech',
        'AMZN': 'Consumer Discretionary',
        'TSLA': 'Consumer Discretionary',
        'PFE': 'Healthcare',
        'JNJ': 'Healthcare',
        'DUK': 'Utilities',
        'NUE': 'Materials',
        'CVX': 'Energy'
    }

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
                "dividend_yield": 0.03,  # You can customize or fetch real data if needed
                "pe_ratio": 15.0,        # Same here — static for demo
                "sector": SECTOR_MAP.get(symbol, "Unknown")
            })

    return stocks
