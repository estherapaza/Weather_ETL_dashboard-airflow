# import libraries
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# api configuration
load_dotenv()

lat = os.getenv("lat", "41.8919")
lon = os.getenv("lon", "12.5113")
timezone = os.getenv("timezone", "europe/rome")

base_url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": lat,
    "longitude": lon,
    "hourly": "temperature_2m,apparent_temperature",
    "timezone": timezone
}

# fetch for temperature data
def fetch_temperature():
    # api call
    response = requests.get(base_url, params=params)
    response.raise_for_status() # raises exception in case of error

    # data parsing and selection
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["datetime"] = pd.to_datetime(df["time"])
    df = df[["datetime", "temperature_2m", "apparent_temperature"]]

    # saving to csv file
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "temperature.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
