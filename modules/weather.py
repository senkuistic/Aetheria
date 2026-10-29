import requests
import pandas as pd

def search_city(city_name, country_code=None):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name.strip(),
        "count": 100,
        "language": "en",
        "format": "json"
    }

    if country_code:
        params["countryCode"] = country_code.upper()

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    columns = [
        "City", "State / Region", "Country",
        "Latitude", "Longitude", "Population", "Time Zone"
    ]

    if not results:
        return pd.DataFrame(columns=columns)

    cities = pd.DataFrame(results)

    # Keep results that match the requested city name.
    exact = cities[
        cities["name"].str.casefold() == city_name.strip().casefold()
    ].copy()

    if exact.empty:
        return pd.DataFrame(columns=columns)

    for column in ["admin1", "country", "latitude", "longitude",
                   "population", "timezone"]:
        if column not in exact.columns:
            exact[column] = None

    exact = exact.rename(columns={
        "name": "City",
        "admin1": "State / Region",
        "country": "Country",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "population": "Population",
        "timezone": "Time Zone"
    })

    exact = exact[columns]

    return exact.sort_values(
        by="Population",
        ascending=False,
        na_position="last"
    ).reset_index(drop=True)


def get_weather(latitude, longitude, timezone="auto"):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m"
        ],
        "forecast_days": 7
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    current = pd.DataFrame([data["current"]])
    hourly = pd.DataFrame(data["hourly"])

    return current, hourly


def prepare_weather_data(hourly):
    hourly = hourly.copy()
    hourly["time"] = pd.to_datetime(hourly["time"])
    return hourly



def search_city_suggestions(city_name):
    city_name = city_name.strip()

    columns = [
        "City", "State / Region", "Country",
        "Latitude", "Longitude", "Population", "Time Zone"
    ]

    if len(city_name) < 2:
        return pd.DataFrame(columns=columns)

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city_name,
        "count": 20,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        return pd.DataFrame(columns=columns)

    cities = pd.DataFrame(results)

    for column in [
        "admin1", "country", "latitude",
        "longitude", "population", "timezone"
    ]:
        if column not in cities.columns:
            cities[column] = None

    cities = cities.rename(columns={
        "name": "City",
        "admin1": "State / Region",
        "country": "Country",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "population": "Population",
        "timezone": "Time Zone"
    })

    cities = cities[columns]

    return cities