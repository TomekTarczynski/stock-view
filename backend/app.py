import requests
import pandas as pd
from io import StringIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()


# Define a root route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Stock View API"}


def fetch_stooq_data(
    symbol: str, start_date: str, end_date: str, interval: str = "d"
) -> pd.DataFrame:
    base_url = "https://stooq.pl/q/d/l/"
    params = {"s": symbol, "d1": start_date, "d2": end_date, "i": interval}

    try:
        # Fetch data from Stooq API
        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            # Log or print the error for debugging
            print(f"Error fetching data: {response.status_code}, {response.text}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch data from Stooq API"
            )

        csv_data = response.content.decode("utf-8")
        data = pd.read_csv(StringIO(csv_data))

        if data.empty:
            raise HTTPException(
                status_code=400, detail="Invalid stock symbol or no data available"
            )

        return data

    except Exception as e:
        # Print the error to help debug the issue
        print(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while fetching stock data.",
        )


# Pydantic model to define request parameters
class StooqRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    interval: str = "d"


# Route to fetch stock data
@app.post("/fetch-data/")
async def get_stooq_data(request: StooqRequest):
    try:
        data = fetch_stooq_data(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            interval=request.interval,
        )
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
