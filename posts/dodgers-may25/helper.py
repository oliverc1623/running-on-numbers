# --- Function to process data ---

import pandas as pd
import io

def process_baseball_data(csv_data, year_filter=None, end_date_str=None):
    """Reads CSV data, processes dates and XWOBA, sorts, filters by date, and calculates rolling average."""
    df = pd.read_csv(io.StringIO(csv_data))
    # Convert 'Game Date' to datetime objects
    df['Game Date'] = pd.to_datetime(df['Game Date'])
    # Convert 'XWOBA' to numeric, handling potential errors
    df['XWOBA'] = pd.to_numeric(df['XWOBA'], errors='coerce')
    # Sort by date for correct rolling calculation
    df = df.sort_values(by='Game Date')

    # Filter by year if specified
    if year_filter:
        df = df[df['Game Date'].dt.year == year_filter]

    # Filter by end date if specified
    if end_date_str:
        end_date = pd.to_datetime(end_date_str)
        df = df[df['Game Date'] <= end_date]

    # Drop rows where XWOBA could not be converted (NaN) before rolling calculation
    df = df.dropna(subset=['XWOBA'])

    # Calculate rolling average
    rolling_window = 7
    df[f'Rolling XWOBA_{rolling_window}'] = df['XWOBA'].rolling(window=rolling_window, min_periods=1).mean()
    return df, rolling_window
