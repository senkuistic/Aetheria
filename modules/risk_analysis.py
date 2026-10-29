def calculate_weather_risk(df):
    df = df.copy()

    score = 0
    reasons = []

    maximum_temperature = df["temperature_2m"].max()
    maximum_rain_probability = df["precipitation_probability"].max()
    maximum_hourly_rain = df["precipitation"].max()
    maximum_wind = df["wind_speed_10m"].max()

    if maximum_temperature >= 40:
        score += 2
        reasons.append("Very high forecast temperature (40°C or above)")
    elif maximum_temperature >= 35:
        score += 1
        reasons.append("High forecast temperature (35°C or above)")

    if maximum_rain_probability >= 80:
        score += 1
        reasons.append("High precipitation probability (80% or above)")

    if maximum_hourly_rain >= 10:
        score += 2
        reasons.append("Heavy hourly precipitation (10 mm or more)")

    if maximum_wind >= 50:
        score += 2
        reasons.append("High forecast wind speed (50 km/h or more)")
    elif maximum_wind >= 30:
        score += 1
        reasons.append("Elevated forecast wind speed (30 km/h or more)")

    if score >= 3:
        level = "High"
        explanation = "Multiple or severe forecast conditions met the selected thresholds."
    elif score >= 1:
        level = "Moderate"
        explanation = "At least one forecast condition met a selected threshold."
    else:
        level = "Low"
        explanation = "None of the selected thresholds were reached."

    if not reasons:
        reasons.append("No selected risk thresholds were reached.")

    return {
        "Risk Level": level,
        "Risk Score": score,
        "Reasons": reasons,
        "Explanation": explanation,
        "Maximum Temperature (°C)": round(float(maximum_temperature), 2),
        "Maximum Rain Probability (%)": round(float(maximum_rain_probability), 2),
        "Maximum Hourly Precipitation (mm)": round(float(maximum_hourly_rain), 2),
        "Maximum Wind Speed (km/h)": round(float(maximum_wind), 2)
    }