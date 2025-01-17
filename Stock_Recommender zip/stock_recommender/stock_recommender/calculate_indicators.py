import pandas as pd
import numpy as np
import os

def calculate_indicators(input_dir, output_file):
    data_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    combined_data = []

    for file in data_files:
        print(f"Processing {file}...")
        df = pd.read_csv(os.path.join(input_dir, file))

        # Ensure all numeric columns are of proper type
        numeric_columns = ['Adj Close', 'Volume', 'Open', 'High', 'Low', 'Close']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NaN values in critical columns
        df = df.dropna(subset=['Adj Close', 'Volume'])

        # Calculate indicators
        df['Daily Return'] = df['Adj Close'].pct_change()
        df['Volatility'] = df['Daily Return'].rolling(5).std()
        df['Avg Volume'] = df['Volume'].rolling(5).mean()

        # Average over the period for summary
        if 'Stock' not in df.columns:
            df['Stock'] = file.replace('.csv', '')  # Add Stock name from file
        if 'Sector' not in df.columns:
            df['Sector'] = 'Unknown'  # Add default Sector if not available

        summary = df.groupby(['Stock', 'Sector']).agg({
            'Daily Return': 'mean',
            'Volatility': 'mean',
            'Avg Volume': 'mean'
        }).reset_index()
        combined_data.append(summary)

    # Save final dataset
    combined_df = pd.concat(combined_data, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Indicators saved to {output_file}")

if __name__ == "__main__":
    calculate_indicators('sector_data', 'final_dataset.csv')
