import yfinance as yf
import pandas as pd

def fetch_stock_data(stock_symbol, start_date, end_date):
    # Download historical data
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    if data.empty:
        print(f"No data found for {stock_symbol}")
        return None

    # Calculate Technical Indicators
    data['MA_20'] = data['Close'].rolling(window=20).mean()  # 20-day Moving Average
    data['RSI'] = calculate_rsi(data['Close'])              # Relative Strength Index
    data['MACD'], data['Signal_Line'] = calculate_macd(data['Close'])  # MACD

    # Keep relevant columns
    data = data[['Close', 'MA_20', 'RSI', 'MACD', 'Signal_Line']]
    return data

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    short_ema = prices.ewm(span=short_window, adjust=False).mean()
    long_ema = prices.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# Save dataset
if __name__ == "__main__":
    stock_symbol = "AAPL"  # Apple stock as an example
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    
    data = fetch_stock_data(stock_symbol, start_date, end_date)
    if data is not None:
        data.to_csv(f"{stock_symbol}_dataset.csv")
        print(f"Dataset saved as {stock_symbol}_dataset.csv")

