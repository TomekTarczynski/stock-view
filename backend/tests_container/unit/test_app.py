import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from app import fetch_stooq_data
from unittest.mock import patch
import pandas as pd

@patch('app.requests.get')
def test_fetch_stooq_data_unit(mock_get):
    # Mock the API response with Polish column names and data
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = (
        b"Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie,Wolumen\n"
        b"2000-05-01,1452.43,1481.51,1452.43,1468.25,536833333.0\n"
        b"2000-05-02,1468.25,1468.25,1445.22,1446.29,561944444.0\n"
    )  # Mocking 'content' as bytes to simulate actual API response

    # Call the function with mock data
    data = fetch_stooq_data(symbol='^spx', start_date='20000501', end_date='20240927', interval='d')

    # Assert that the DataFrame is correct
    assert len(data) == 2  # We provided 2 rows of data in the mock
    assert list(data.columns) == ['Data', 'Otwarcie', 'Najwyzszy', 'Najnizszy', 'Zamkniecie', 'Wolumen']

    # Check if the values in the first row match the mock data
    assert data['Zamkniecie'].iloc[0] == 1468.25
    assert data['Otwarcie'].iloc[0] == 1452.43
    assert data['Wolumen'].iloc[0] == 536833333.0

    # Check if the values in the second row match the mock data
    assert data['Zamkniecie'].iloc[1] == 1446.29
    assert data['Otwarcie'].iloc[1] == 1468.25
    assert data['Wolumen'].iloc[1] == 561944444.0

def test_fetch_stooq_data_integration():
    """
    This test makes an actual HTTP request to the Stooq API and verifies
    that the returned data is valid.
    """
    # Parameters for the API request
    symbol = '^spx'
    start_date = '20230901'  # Example start date (recent to avoid too large datasets)
    end_date = '20230930'    # Example end date
    interval = 'd'           # Daily interval

    # Fetch actual data from the API
    data = fetch_stooq_data(symbol=symbol, start_date=start_date, end_date=end_date, interval=interval)

    # Check if the result is a pandas DataFrame
    assert isinstance(data, pd.DataFrame)

    # Ensure the DataFrame is not empty
    assert not data.empty

    # Check if required columns are present
    expected_columns = ['Data', 'Otwarcie', 'Najwyzszy', 'Najnizszy', 'Zamkniecie', 'Wolumen']
    assert list(data.columns) == expected_columns

    # Check if the first few rows contain valid data
    assert len(data) > 0
    assert 'Zamkniecie' in data.columns
    assert data['Zamkniecie'].iloc[0] > 0  # Ensure the 'Zamkniecie' value is greater than 0