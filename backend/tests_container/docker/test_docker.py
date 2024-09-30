import requests

API_URL = "http://localhost:8000"


def test_api_root():
    """Test the root '/' endpoint."""
    response = requests.get(f"{API_URL}/")

    # Ensure the response is OK (status code 200)
    assert response.status_code == 200

    # Check the expected response from the root endpoint
    assert response.json() == {"message": "Welcome to the Stock View API"}


def test_api_fetch_data_valid():
    """Test the /fetch-data/ endpoint with valid input."""
    # Define the request payload
    request_payload = {
        "symbol": "^spx",
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = requests.post(f"{API_URL}/fetch-data/", json=request_payload)

    # Ensure the response is OK (status code 200)
    assert response.status_code == 200

    # Ensure the response contains a list of data
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure the list is not empty


def test_api_fetch_data_invalid_symbol():
    """Test the /fetch-data/ endpoint with an invalid stock symbol."""
    # Define the request payload with an invalid symbol
    request_payload = {
        "symbol": "INVALID_SYMBOL",
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = requests.post(f"{API_URL}/fetch-data/", json=request_payload)

    # Ensure the API returns a 400 error for invalid stock symbol
    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "500: An internal server error occurred while fetching stock data."
    )


def test_api_fetch_data_missing_field():
    """Test the /fetch-data/ endpoint with a missing required field."""
    # Define the request payload with a missing 'symbol' field
    request_payload = {
        "start_date": "20220101",
        "end_date": "20220131",
        "interval": "d",
    }

    # Send a POST request to the /fetch-data/ endpoint
    response = requests.post(f"{API_URL}/fetch-data/", json=request_payload)

    # Ensure the API returns a 422 Unprocessable Entity error for missing field
    assert response.status_code == 422
    assert "Field required" in response.json()["detail"][0]["msg"]
