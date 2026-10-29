import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"
DATABASE_PATH = DATA_FOLDER / "aetheria.db"


def create_database():
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS weather_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            analysis_time TEXT,
            average_temperature REAL,
            maximum_temperature REAL,
            minimum_temperature REAL,
            average_humidity REAL,
            total_precipitation REAL,
            average_wind_speed REAL
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(city, country, summary):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT INTO weather_analyses (
            city, country, analysis_time,
            average_temperature, maximum_temperature,
            minimum_temperature, average_humidity,
            total_precipitation, average_wind_speed
        )
        VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?, ?)
    """, (
        city,
        country,
        summary["Average Temperature (°C)"],
        summary["Maximum Temperature (°C)"],
        summary["Minimum Temperature (°C)"],
        summary["Average Humidity (%)"],
        summary["Total Precipitation (mm)"],
        summary["Average Wind Speed (km/h)"]
    ))

    connection.commit()
    connection.close()

def get_saved_analyses():
    connection = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM weather_analyses ORDER BY id DESC",
        connection
    )

    connection.close()
    return df