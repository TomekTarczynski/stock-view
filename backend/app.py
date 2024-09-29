import requests
import pandas as pd
from io import StringIO  # Import StringIO from the io module

def fetch_stooq_data(symbol: str, start_date: str, end_date: str, interval: str = 'd') -> pd.DataFrame:
    """
    Fetch stock data from the Stooq API.

    Args:
        symbol (str): The stock symbol (e.g., '^spx' for S&P 500).
        start_date (str): The start date in the format 'YYYYMMDD' (e.g., '20000501').
        end_date (str): The end date in the format 'YYYYMMDD' (e.g., '20240927').
        interval (str): The interval for the data. Defaults to 'd' (daily).
                       Options: 'd' (daily), 'w' (weekly), 'm' (monthly), 'q' (quarterly), 'y' (yearly).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the stock data.
    """
    base_url = "https://stooq.pl/q/d/l/"
    
    # Construct the full URL with parameters
    params = {
        's': symbol,
        'd1': start_date,
        'd2': end_date,
        'i': interval
    }
    
    # Make the request to the API
    response = requests.get(base_url, params=params)
    
    # Raise an exception if the request failed
    response.raise_for_status()
    
    # Parse the CSV data into a pandas DataFrame
    csv_data = response.content.decode('utf-8')
    data = pd.read_csv(StringIO(csv_data))  # Use StringIO from io to handle CSV content
    
    # Return the DataFrame
    return data


# Example usage:
start_date = '20000501'
end_date = '20240927'
symbol = '^spx'
interval = 'd'

# Fetch the data for the S&P 500 (SPX)
sp500_data = fetch_stooq_data(symbol=symbol, start_date=start_date, end_date=end_date, interval=interval)
print(sp500_data.head())  # Print the first few rows of the DataFrame
