import pandas as pd

def check_weather_data(df):
    df = df.copy()

    report = {
        "Total Records": len(df),
        "Duplicate Records": int(df.duplicated().sum()),
        "Missing Values": int(df.isnull().sum().sum()),
        "Missing Values by Column": df.isnull().sum().to_dict(),
        "Suspicious Temperatures": int(
            ((df["temperature_2m"] < -90) |
             (df["temperature_2m"] > 60)).sum()
        ),
        "Negative Precipitation Records": int(
            (df["precipitation"] < 0).sum()
        )
    }

    return report