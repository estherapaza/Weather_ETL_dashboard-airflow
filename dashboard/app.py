import streamlit as st
from config import get_db_engine
from data_access import (
    load_temperature_daily,
    load_temperature_hourly,
    load_precipitation_hourly,
    load_humidity_hourly,
    load_wind_hourly,
    load_weather_alerts
)
from charts import (
    temperature_hourly_chart,
    temperature_weekly_chart,
    temperature_daily_min_max_chart,
    precipitation_daily_chart,
    precipitation_weekly_chart,
    humidity_daily_chart,
    humidity_weekly_chart,
    wind_daily_chart,
    wind_weekly_chart,
)

# page configuration
st.set_page_config(page_title="weather dashboard", layout="wide")

# function to load data into cache
@st.cache_data(ttl=600)
def load_all_data(_engine):
    return (
        load_temperature_daily(_engine),
        load_temperature_hourly(_engine),
        load_precipitation_hourly(_engine),
        load_humidity_hourly(_engine),
        load_wind_hourly(_engine),
    )

# removes datetime columns from dataframe
def hide_datetime_columns(df):
    datetime_cols = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
    return df.drop(columns=datetime_cols)

# main function
def main():
    # central title
    st.markdown(
        "<h1 style='text-align: center;'>🌤️ weather dashboard 🌦️</h1>",
        unsafe_allow_html=True
    )

    # loading data from the database
    engine = get_db_engine()
    temp_daily, temp_hourly, prec_hourly, humidity_hourly, wind_hourly = load_all_data(engine)

    # sidebar: navigation and date selection
    st.sidebar.title("navigation")
    page = st.sidebar.selectbox(
        "select section",
        [
            "temperature 🌡️",
            "precipitation 🌧️",
            "humidity 💧",
            "wind 🌬️"
        ]
    )

    available_dates = sorted(temp_hourly["Data"].unique(), reverse=True)
    selected_date = st.sidebar.selectbox("select date", available_dates)

    # selected page title
    st.markdown(
        f"<h2 style='text-align: center;'>{page}</h2>",
        unsafe_allow_html=True
    )

    # temperature
    if "temperature" in page:
        filtered_temp = temp_hourly[temp_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌡️ hourly temperature - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_temp), width=1000)
            st.altair_chart(temperature_hourly_chart(filtered_temp), use_container_width=True)

        with col2:
            st.subheader("📅 weekly temperature")
            st.altair_chart(temperature_weekly_chart(temp_hourly), use_container_width=True)

        with col2:
            st.subheader("🌡️ daily minimum and maximums")
            st.altair_chart(temperature_daily_min_max_chart(temp_daily), use_container_width=True)

    # precipitation
    elif "precipitation" in page:
        filtered_prec = prec_hourly[prec_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌧️ hourly precipitation - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_prec), width=1000)
            st.altair_chart(precipitation_daily_chart(filtered_prec), use_container_width=True)

        with col2:
            st.subheader("📅 weekly precipitation")
            st.altair_chart(precipitation_weekly_chart(prec_hourly), use_container_width=True)

    # humidity
    elif "humidity" in page:
        filtered_humidity = humidity_hourly[humidity_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"💧 hourly humidity - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_humidity), width=1000)
            st.altair_chart(humidity_daily_chart(filtered_humidity), use_container_width=True)

        with col2:
            st.subheader("📅 weekly humidity")
            st.altair_chart(humidity_weekly_chart(humidity_hourly), use_container_width=True)

    # wind
    elif "wind" in page:
        filtered_wind = wind_hourly[wind_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌬️ hourly wind - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_wind), width=1000)
            st.altair_chart(wind_daily_chart(filtered_wind), use_container_width=True)

        with col2:
            st.subheader("📅 weekly wind")
            st.altair_chart(wind_weekly_chart(wind_hourly), use_container_width=True)

    # weather alert
    alerts_df = load_weather_alerts(engine)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if alerts_df.empty:
            st.markdown("## ✅ weather alert")
            st.info("no active weather alerts.")
        else:
            st.markdown("## ⚠️ weather alert")
            st.dataframe(alerts_df, use_container_width=True)

# entry point
if __name__ == "__main__":
    main()