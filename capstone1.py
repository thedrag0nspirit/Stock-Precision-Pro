# -*- coding: utf-8 -*-
"""capstone1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kTsgAZb4fwS645raFK-Wf5rH3yRSw1Tt
"""

!pip install mplfinance
!pip install yfinance
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pytz

import pandas as pd

# Read the input CSV file
input_csv = '/content/sector_symbols_modified-2.csv'
df = pd.read_csv(input_csv)

# Get the unique sectors
sectors = df['Sector'].unique()

# Create a new CSV file for each sector
for sector in sectors:
    sector_df = df[df['Sector'] == sector]
    output_csv = f'{sector}.csv'
    sector_df.to_csv(output_csv, index=False)
    print(f'Created {output_csv}')

import yfinance as yf
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta
import os

# Define the file paths for the 12 CSV files and their corresponding folder names
sector_file_paths = {
    "Consumer_Cyclical": "/content/Consumer Cyclical.csv",
    "Real_Estate": "/content/Real Estate.csv",
    "Technology": "/content/Technology.csv",
    "Healthcare": "/content/Healthcare.csv",
    "Energy": "/content/Energy.csv",
    "Communication_Services": "/content/Communication Services.csv",
    "Utilities": "/content/Utilities.csv",
    "Consumer_Defensive": "/content/Consumer Defensive.csv",
    "Basic_Materials": "/content/Basic Materials.csv",
    "Industrials": "/content/Industrials.csv",
    "Financial_Services": "/content/Financial Services.csv",
    "Other": "/content/nan.csv"  # Replace with actual path
}

# Define the base output directory where all charts will be saved
base_output_dir = "/content/candlestick_charts"
os.makedirs(base_output_dir, exist_ok=True)

# Calculate the start and end dates (1 year from today)
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

# Function to fetch data and save candlestick charts
def fetch_and_save_candlestick(symbol, output_dir):
    try:
        # Fetch historical data from yfinance
        data = yf.download(symbol, start=start_date, end=end_date)

        # Skip symbols with insufficient data
        if data.empty:
            print(f"No data found for {symbol}. Skipping.")
            return

        # Plot and save the candlestick chart
        chart_path = os.path.join(output_dir, f"{symbol}_candlestick.png")
        mpf.plot(data, type='candle', style='charles', title=symbol, savefig=chart_path)
        print(f"Saved candlestick chart for {symbol} at {chart_path}")

    except Exception as e:
        print(f"An error occurred for {symbol}: {e}. Skipping.")

# Loop through each sector and corresponding file path
for sector, csv_file_path in sector_file_paths.items():
    if os.path.exists(csv_file_path):
        # Create a subfolder for each sector
        sector_output_dir = os.path.join(base_output_dir, sector.replace(" ", "_"))
        os.makedirs(sector_output_dir, exist_ok=True)

        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Iterate over the rows
        for _, row in df.iterrows():
            symbols = row['Symbols'].split(',')  # Split the symbols by comma

            # Fetch data and save charts for each symbol
            for symbol in symbols:
                fetch_and_save_candlestick(symbol.strip(), sector_output_dir)
    else:
        print(f"File not found: {csv_file_path}")

