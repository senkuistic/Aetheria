import pandas as pd


def calculate_weather_summary(df):
    summary = {
        "Average Temperature (°C)": round(float(df["temperature_2m"].mean()), 2),
        "Maximum Temperature (°C)": round(float(df["temperature_2m"].max()), 2),
        "Minimum Temperature (°C)": round(float(df["temperature_2m"].min()), 2),
        "Average Humidity (%)": round(float(df["relative_humidity_2m"].mean()), 2),
        "Maximum Precipitation Probability (%)": int(
            df["precipitation_probability"].max()
        ),
        "Total Precipitation (mm)": round(float(df["precipitation"].sum()), 2),
        "Average Wind Speed (km/h)": round(float(df["wind_speed_10m"].mean()), 2)
    }

    return summary


def calculate_temperature_change(df):
    df = df.sort_values("time")

    first_temperature = df["temperature_2m"].iloc[0]
    last_temperature = df["temperature_2m"].iloc[-1]

    change = last_temperature - first_temperature

    return {
        "First Forecast Temperature (°C)": round(first_temperature, 2),
        "Last Forecast Temperature (°C)": round(last_temperature, 2),
        "Temperature Change (°C)": round(change, 2)
    }