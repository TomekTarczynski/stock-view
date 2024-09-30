import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from app import fetch_stooq_data
from app import app  # Import your FastAPI app
from unittest.mock import patch
import pandas as pd
from fastapi.testclient import TestClient


# Create a TestClient to simulate HTTP requests to the FastAPI app
client = TestClient(app)


def test_fetch_stooq_data_integration():
    """
    This test makes an actual HTTP request to the Stooq API and verifies
    that the returned data is valid.
    """
    # Parameters for the API request
    symbol = "^spx"
    start_date = "20230901"  # Example start date (recent to avoid too large datasets)
    end_date = "20230930"  # Example end date
    interval = "d"  # Daily interval

    # Fetch actual data from the API
    data = fetch_stooq_data(
        symbol=symbol, start_date=start_date, end_date=end_date, interval=interval
    )

    # Check if the result is a pandas DataFrame
    assert isinstance(data, pd.DataFrame)

    # Ensure the DataFrame is not empty
    assert not data.empty

    # Check if required columns are present
    expected_columns = [
        "Data",
        "Otwarcie",
        "Najwyzszy",
        "Najnizszy",
        "Zamkniecie",
        "Wolumen",
    ]
    assert list(data.columns) == expected_columns

    # Check if the first few rows contain valid data
    assert len(data) > 0
    assert "Zamkniecie" in data.columns
    assert (
        data["Zamkniecie"].iloc[0] > 0
    )  # Ensure the 'Zamkniecie' value is greater than 0


def test_read_root():
    """
    Test the root endpoint.
    This ensures that the root '/' endpoint works and returns the expected response.
    """
    response = client.get("/")  # Send a GET request to the root endpoint
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Stock View API"}


def test_fetch_data_valid():
    """
    Test the /fetch-data/ endpoint with valid data.
    This ensures that the endpoint returns valid stock data for a valid request.
    """
    # Define valid JSON input
    request_payload = {
        "symbol": "^spx",
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = client.post("/fetch-data/", json=request_payload)

    # Ensure the response is OK (status code 200)
    assert response.status_code == 200

    # Ensure the response contains the expected fields
    json_response = response.json()

    # Check if the response is a non-empty list of dictionaries
    assert isinstance(json_response, list)
    assert len(json_response) > 0

    # Check if the required fields are in the response data
    required_fields = [
        "Data",
        "Otwarcie",
        "Najwyzszy",
        "Najnizszy",
        "Zamkniecie",
        "Wolumen",
    ]
    for row in json_response:
        for field in required_fields:
            assert field in row


def test_fetch_data_invalid_symbol():
    """
    Test the /fetch-data/ endpoint with an invalid stock symbol.
    This ensures that the API handles invalid symbols properly.
    """
    # Define a request with an invalid stock symbol
    request_payload = {
        "symbol": "INVALID",
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = client.post("/fetch-data/", json=request_payload)

    # Ensure the API returns a 500 error when fetching invalid symbol data
    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "500: An internal server error occurred while fetching stock data."
    )


def test_fetch_data_missing_field():
    """
    Test the /fetch-data/ endpoint with a missing required field.
    This ensures that the API handles requests with missing fields appropriately.
    """
    # Define a request with missing 'symbol' field
    request_payload = {
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = client.post("/fetch-data/", json=request_payload)

    # Ensure the API returns a 422 Unprocessable Entity status for missing fields
    assert response.status_code == 422

    # Assert the correct validation error
    assert "Field required" in response.json()["detail"][0]["msg"]
