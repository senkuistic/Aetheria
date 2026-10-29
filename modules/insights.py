def generate_weather_insights(df, summary):
    insights = []

    average_temp = summary["Average Temperature (°C)"]
    maximum_temp = summary["Maximum Temperature (°C)"]
    average_humidity = summary["Average Humidity (%)"]
    total_rain = summary["Total Precipitation (mm)"]
    average_wind = summary["Average Wind Speed (km/h)"]

    if maximum_temp >= 35:
        insights.append(
            "High temperatures are expected during the forecast period. "
            "Consider limiting strenuous outdoor activity during the hottest hours."
        )
    elif average_temp <= 10:
        insights.append(
            "The forecast period is relatively cold. "
            "Consider appropriate clothing for outdoor activities."
        )
    else:
        insights.append(
            "The forecast temperatures do not meet Aetheria's selected "
            "high-heat or cold-weather thresholds."
        )

    if average_humidity >= 80:
        insights.append(
            "Average humidity is high. Conditions may feel more humid "
            "than the temperature alone suggests."
        )
    elif average_humidity <= 30:
        insights.append(
            "Average humidity is low. The air may feel relatively dry."
        )
    else:
        insights.append(
            "Average humidity is between Aetheria's selected low and high "
            "humidity thresholds."
        )

    if total_rain >= 50:
        insights.append(
            "The forecast indicates substantial accumulated precipitation. "
            "Review the hourly forecast when planning outdoor activities."
        )
    elif total_rain > 0:
        insights.append(
            "Some precipitation is forecast. Check hourly rainfall probabilities "
            "to understand when rain may occur."
        )
    else:
        insights.append(
            "No accumulated precipitation is forecast in the retrieved hourly data."
        )

    if average_wind >= 30:
        insights.append(
            "Average forecast wind speed is elevated. "
            "Check local weather updates before wind-sensitive activities."
        )
    else:
        insights.append(
            "Average forecast wind speed is below Aetheria's selected "
            "elevated-wind threshold."
        )

    return insights