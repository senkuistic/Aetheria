import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import importlib

import modules.weather
import modules.analytics
import modules.data_quality
import modules.database
import modules.risk_analysis
import modules.insights

importlib.reload(modules.weather)
importlib.reload(modules.analytics)
importlib.reload(modules.data_quality)
importlib.reload(modules.database)
importlib.reload(modules.risk_analysis)
importlib.reload(modules.insights)

search_city = modules.weather.search_city
get_weather = modules.weather.get_weather
prepare_weather_data = modules.weather.prepare_weather_data
search_city_suggestions = modules.weather.search_city_suggestions

calculate_weather_summary = modules.analytics.calculate_weather_summary
calculate_temperature_change = modules.analytics.calculate_temperature_change

check_weather_data = modules.data_quality.check_weather_data
calculate_weather_risk = modules.risk_analysis.calculate_weather_risk
generate_weather_insights = modules.insights.generate_weather_insights

create_database = modules.database.create_database
save_analysis = modules.database.save_analysis
get_saved_analyses = modules.database.get_saved_analyses


st.set_page_config(
    page_title="Aetheria | Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Force the entire application background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    section[data-testid="stMain"] {
        background-color: #eaf4f7 !important;
    }

    /* Main content area */
    [data-testid="stMain"] > div,
    [data-testid="stMain"] > div > div,
    .main .block-container {
        background-color: #eaf4f7 !important;
    }

    /* Top toolbar */
    [data-testid="stHeader"] {
        background-color: #eaf4f7 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #dcebf1 !important;
        border-right: 1px solid #c7dce5;
    }

    /* Text */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #123b52 !important;
    }

    .stApp p,
    .stApp li,
    .stApp label,
    .stApp small {
        color: #263b4a !important;
    }

    [data-testid="stSidebar"] * {
        color: #123b52 !important;
    }

    [data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #123b52 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #dce8ef !important;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(25, 70, 90, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #496779 !important;
    }

    [data-testid="stMetricValue"] {
        color: #126782 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #d9f0ec !important;
        color: #164e50 !important;
        border: 1px solid #a8d8cf !important;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #bce5dc !important;
        color: #123b52 !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #dce8ef !important;
        border-radius: 10px;
    }

    /* Captions */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #496779 !important;
    }

    /* Layout */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    hr {
        border-color: #d5e3ec;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="background:linear-gradient(120deg,#dff3f3,#e8f5f8,#d9f0e8);
                padding:30px;border-radius:16px;margin-bottom:20px;">
        <p style="color:#ffffff !important;font-size:13px;letter-spacing:3px;font-weight:700;">
            ENVIRONMENTAL INTELLIGENCE PLATFORM
        </p>
        <h1 style="color:#ffffff !important;font-size:40px;margin:5px 0;">
            🌦️ Aetheria
        </h1>
        <p style="color:#ffffff !important;font-size:18px;">
            Environmental Data Analytics &amp; Weather Intelligence
        </p>
        <p style="color:#ffffff !important;font-size:14px;">
            Explore global forecasts, compare locations, assess data quality,
            and discover meaningful weather patterns.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#294f63;font-size:13px;margin:0 0 8px 0;'>"
    "DATA SOURCE · Open-Meteo | ANALYTICS · Python, Pandas & NumPy | STORAGE · SQLite"
    "</p>",
    unsafe_allow_html=True
)

create_database()

st.sidebar.header("Location Settings")
city_name = st.sidebar.text_input("Enter a city", value="Kochi")

if st.sidebar.button("Find City"):
    if not city_name.strip():
        st.sidebar.warning("Please enter a city name.")
    else:
        try:
            cities = search_city(city_name)

            if cities.empty:
                st.session_state.pop("cities", None)
                st.session_state.pop("hourly_clean", None)
                st.error("No exact city match found. Check the spelling.")
            else:
                st.session_state["cities"] = cities
                st.session_state["city_name"] = city_name.strip()
        except Exception as error:
            st.error(f"City search failed: {error}")

if "cities" in st.session_state:
    cities = st.session_state["cities"]

    selected_index = st.selectbox(
        "Choose your location",
        options=list(range(len(cities))),
        format_func=lambda i: (
            f"{cities.iloc[i]['City']}, "
            f"{cities.iloc[i]['State / Region'] or 'Region unavailable'}, "
            f"{cities.iloc[i]['Country']}"
        ),
        key="main_city_selection"
    )

    selected_city = cities.iloc[selected_index]

    if st.button("Analyze Weather"):
        with st.spinner("Retrieving weather forecast..."):
            try:
                current, hourly = get_weather(
                    selected_city["Latitude"],
                    selected_city["Longitude"],
                    selected_city["Time Zone"]
                )

                hourly_clean = prepare_weather_data(hourly)
                summary = calculate_weather_summary(hourly_clean)
                change = calculate_temperature_change(hourly_clean)
                quality = check_weather_data(hourly_clean)
                risk = calculate_weather_risk(hourly_clean)

                st.session_state["current"] = current
                st.session_state["hourly_clean"] = hourly_clean
                st.session_state["summary"] = summary
                st.session_state["change"] = change
                st.session_state["quality"] = quality
                st.session_state["selected_city"] = selected_city
                st.session_state["risk"] = risk

            except Exception as error:
                st.error(f"Could not analyse weather: {error}")


st.markdown("<hr style='margin:8px 0 14px 0;border-color:#d5e3ec;'>", unsafe_allow_html=True)
st.header("Saved Analyses")

saved = get_saved_analyses()

if saved.empty:
    st.info("No saved analyses yet. Analyze a city and save the results.")
else:
    st.write(
        "Review previous weather analyses stored in Aetheria's SQLite database."
    )

    st.dataframe(saved, hide_index=True, width="stretch")

    st.subheader("Explore a Saved Analysis")

    saved_options = list(range(len(saved)))

    selected_saved_index = st.selectbox(
        "Choose a saved record",
        options=saved_options,
        format_func=lambda i: (
            f"{saved.iloc[i]['city']}, "
            f"{saved.iloc[i]['country']} — "
            f"{saved.iloc[i]['analysis_time']}"
        ),
        key="saved_analysis_selection"
    )

    selected_saved = saved.iloc[selected_saved_index]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Temperature",
        f"{selected_saved['average_temperature']} °C"
    )

    col2.metric(
        "Maximum Temperature",
        f"{selected_saved['maximum_temperature']} °C"
    )

    col3.metric(
        "Minimum Temperature",
        f"{selected_saved['minimum_temperature']} °C"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Average Humidity",
        f"{selected_saved['average_humidity']}%"
    )

    col5.metric(
        "Total Precipitation",
        f"{selected_saved['total_precipitation']} mm"
    )

    col6.metric(
        "Average Wind Speed",
        f"{selected_saved['average_wind_speed']} km/h"
    )


if "hourly_clean" in st.session_state:
    hourly_clean = st.session_state["hourly_clean"]
    summary = st.session_state["summary"]
    insights = generate_weather_insights(hourly_clean, summary)
    change = st.session_state["change"]
    quality = st.session_state["quality"]
    selected_city = st.session_state["selected_city"]
    current = st.session_state["current"]

    st.header(
        f"Weather Analysis: {selected_city['City']}, "
        f"{selected_city['Country']}"
    )

    st.subheader("Current Weather")
    st.dataframe(current, width="stretch")

    st.subheader("Weather Summary")

    columns = st.columns(4)

    columns[0].metric(
        "🌡️ Average Temperature",
        f"{summary['Average Temperature (°C)']} °C",
        help="Average temperature across the 7-day hourly forecast."
    )

    columns[1].metric(
        "💧 Average Humidity",
        f"{summary['Average Humidity (%)']}%",
        help="Average relative humidity across the forecast."
    )

    columns[2].metric(
        "🌧️ Total Forecast Precipitation",
        f"{summary['Total Precipitation (mm)']} mm",
        help="Sum of hourly precipitation values over the forecast period."
    )

    columns[3].metric(
        "💨 Average Wind Speed",
        f"{summary['Average Wind Speed (km/h)']} km/h",
        help="Average wind speed across the forecast."
    )

    st.subheader("Weather Insights")

    for insight in insights:
        st.write(f"• {insight}")

    risk = st.session_state["risk"]

    st.subheader("Environmental Weather Risk Indicator")

    st.caption(
        "Aetheria's experimental rule-based indicator. "
        "Not an official weather warning."
    )

    risk_columns = st.columns(2)

    risk_columns[0].metric(
        "Risk Level",
        risk["Risk Level"]
    )

    risk_columns[1].metric(
        "Risk Score",
        f"{risk['Risk Score']} points"
    )

    st.write(risk["Explanation"])

    st.write("**Conditions identified:**")

    for reason in risk["Reasons"]:
        st.write(f"- {reason}")

    with st.expander("View risk assessment details"):
        st.write(
            f"Maximum temperature: "
            f"{risk['Maximum Temperature (°C)']} °C"
        )
        st.write(
            f"Maximum precipitation probability: "
            f"{risk['Maximum Rain Probability (%)']}%"
        )
        st.write(
            f"Maximum hourly precipitation: "
            f"{risk['Maximum Hourly Precipitation (mm)']} mm"
        )
        st.write(
            f"Maximum wind speed: "
            f"{risk['Maximum Wind Speed (km/h)']} km/h"
        )

    st.subheader("7-Day Temperature Forecast")

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        hourly_clean["time"],
        hourly_clean["temperature_2m"],
        linewidth=2,
        label="Temperature"
    )

    ax.fill_between(
        hourly_clean["time"],
        hourly_clean["temperature_2m"],
        alpha=0.15
    )

    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Hourly Temperature Across the Forecast Period")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


    st.subheader("Precipitation Probability Forecast")

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        hourly_clean["time"],
        hourly_clean["precipitation_probability"],
        linewidth=2,
        label="Precipitation Probability"
    )

    ax.fill_between(
        hourly_clean["time"],
        hourly_clean["precipitation_probability"],
        alpha=0.15
    )

    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Probability (%)")
    ax.set_title("Hourly Chance of Precipitation")
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


    st.subheader("Temperature Change Across Forecast")

    for name, value in change.items():
        st.write(f"**{name}:** {value}")

    st.subheader("Data Quality Report")

    quality_columns = st.columns(3)
    quality_columns[0].metric("Records", quality["Total Records"])
    quality_columns[1].metric("Duplicates", quality["Duplicate Records"])
    quality_columns[2].metric("Missing Values", quality["Missing Values"])

    with st.expander("View full quality report"):
        st.write("**Total Records:**", quality["Total Records"])
        st.write("**Duplicate Records:**", quality["Duplicate Records"])
        st.write("**Missing Values:**", quality["Missing Values"])

        st.write("**Missing Values by Column**")
        missing_df = pd.DataFrame(
            list(quality["Missing Values by Column"].items()),
            columns=["Column", "Missing Values"]
        )
        st.dataframe(missing_df, hide_index=True, width="stretch")

        st.write("**Suspicious Temperatures:**", quality["Suspicious Temperatures"])
        st.write("**Negative Precipitation Records:**", quality["Negative Precipitation Records"])

    st.subheader("Download Results")

    st.download_button(
        "Download Hourly Weather CSV",
        data=hourly_clean.to_csv(index=False).encode("utf-8"),
        file_name="aetheria_hourly_weather.csv",
        mime="text/csv"
    )

    summary_df = pd.DataFrame(
        list(summary.items()),
        columns=["Metric", "Value"]
    )

    st.download_button(
        "Download Weather Summary CSV",
        data=summary_df.to_csv(index=False).encode("utf-8"),
        file_name="aetheria_weather_summary.csv",
        mime="text/csv"
    )

    if st.button("Save Analysis to Database"):
        save_analysis(
            selected_city["City"],
            selected_city["Country"],
            summary
        )
        st.success("Analysis saved successfully!")

else:
    st.info("Enter a city in the sidebar and click Search and Analyze to begin.")

st.divider()

st.header("Compare Cities")
st.write("Type a city name and select its location from the suggestions.")

if "comparison_choices" not in st.session_state:
    st.session_state["comparison_choices"] = [None, None, None]

selected_locations = []

for i in range(3):
    city_query = st.text_input(
        f"City {i + 1}" + (" (required)" if i < 2 else " (optional)"),
        placeholder="Start typing a city name...",
        key=f"compare_query_{i}"
    )

    if city_query.strip() and len(city_query.strip()) >= 2:
        try:
            suggestions = search_city_suggestions(city_query)

            if not suggestions.empty:
                options = list(range(len(suggestions)))

                selected_index = st.selectbox(
                    f"Choose location for City {i + 1}",
                    options=options,
                    format_func=lambda j, df=suggestions: (
                        f"{df.iloc[j]['City']}, "
                        f"{df.iloc[j]['State / Region'] or 'Region unavailable'}, "
                        f"{df.iloc[j]['Country']}"
                    ),
                    key=f"compare_location_{i}_{city_query.strip().casefold()}"
                )

                selected_locations.append(suggestions.iloc[selected_index])

            else:
                st.info(f"No locations found for '{city_query}'.")

        except Exception as error:
            st.warning(f"Location search failed for '{city_query}': {error}")

    else:
        selected_locations.append(None)

if st.button("Compare Selected Cities"):
    valid_locations = [
        location for location in selected_locations
        if location is not None
    ]

    if len(valid_locations) < 2:
        st.warning("Select at least two valid city locations.")
    else:
        comparison_results = []

        with st.spinner("Loading weather forecasts..."):
            for location in valid_locations:
                try:
                    current, hourly = get_weather(
                        location["Latitude"],
                        location["Longitude"],
                        location["Time Zone"]
                    )

                    hourly_clean = prepare_weather_data(hourly)
                    summary = calculate_weather_summary(hourly_clean)

                    comparison_results.append({
                        "City": location["City"],
                        "State / Region": location["State / Region"],
                        "Country": location["Country"],
                        **summary
                    })

                except Exception as error:
                    st.warning(
                        f"Could not load weather for {location['City']}: {error}"
                    )

        if len(comparison_results) >= 2:
            comparison_df = pd.DataFrame(comparison_results)
            st.session_state["comparison_results"] = comparison_df

if "comparison_results" in st.session_state:
    comparison_df = st.session_state["comparison_results"]

    st.subheader("Weather Comparison Table")
    st.dataframe(comparison_df, width="stretch")

    st.subheader("Average Forecast Temperature")

    fig, ax = plt.subplots(figsize=(10, 5))
    labels = comparison_df["City"] + ", " + comparison_df["Country"]
    ax.bar(labels, comparison_df["Average Temperature (°C)"])
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_title("Forecast Temperature Comparison")
    ax.grid(axis="y")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Other Weather Conditions")

    chart_metrics = [
        ("Average Humidity (%)", "Average Humidity (%)"),
        ("Total Precipitation (mm)", "Total Forecast Precipitation (mm)"),
        ("Average Wind Speed (km/h)", "Average Wind Speed (km/h)")
    ]

    for column_name, chart_title in chart_metrics:
        fig, ax = plt.subplots(figsize=(10, 4))

        labels = (
            comparison_df["City"] + ", " + comparison_df["Country"]
        )

        ax.bar(labels, comparison_df[column_name])
        ax.set_title(chart_title)
        ax.set_ylabel(column_name)
        ax.grid(axis="y")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


    st.subheader("Comparison Findings")

    warmest = comparison_df.loc[
        comparison_df["Average Temperature (°C)"].idxmax()
    ]

    most_humid = comparison_df.loc[
        comparison_df["Average Humidity (%)"].idxmax()
    ]

    wettest = comparison_df.loc[
        comparison_df["Total Precipitation (mm)"].idxmax()
    ]

    windiest = comparison_df.loc[
        comparison_df["Average Wind Speed (km/h)"].idxmax()
    ]

    st.write(
        f"**Highest average temperature:** "
        f"{warmest['City']}, {warmest['Country']} "
        f"({warmest['Average Temperature (°C)']:.2f} °C)"
    )

    st.write(
        f"**Highest average humidity:** "
        f"{most_humid['City']}, {most_humid['Country']} "
        f"({most_humid['Average Humidity (%)']:.2f}%)"
    )

    st.write(
        f"**Highest total forecast precipitation:** "
        f"{wettest['City']}, {wettest['Country']} "
        f"({wettest['Total Precipitation (mm)']:.2f} mm)"
    )

    st.write(
        f"**Highest average wind speed:** "
        f"{windiest['City']}, {windiest['Country']} "
        f"({windiest['Average Wind Speed (km/h)']:.2f} km/h)"
    )

    st.info(
        "These findings summarize the available 7-day hourly weather "
        "forecasts. They should not be interpreted as long-term climate trends."
    )


    st.download_button(
        "Download Comparison CSV",
        data=comparison_df.to_csv(index=False).encode("utf-8"),
        file_name="aetheria_city_comparison.csv",
        mime="text/csv"
    )