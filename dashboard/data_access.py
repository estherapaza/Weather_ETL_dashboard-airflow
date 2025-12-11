# import libraries
import pandas as pd

# auxiliary function to load data from the database
def load_table_with_datetime(engine, table_name, date_col="Data", time_col="Ora", datetime_col="datetime", fmt="%d/%m/%Y %H:%M"):
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    df.columns = [c.strip() for c in df.columns]
    df[datetime_col] = pd.to_datetime(df[date_col] + " " + df[time_col], format=fmt)
    return df

# loads temperature data
def load_temperature_hourly(engine):
    return load_table_with_datetime(engine, "temperature_hourly")

# loads precipitation data
def load_precipitation_hourly(engine):
    return load_table_with_datetime(engine, "precipitation_hourly")

# loads humidity data
def load_humidity_hourly(engine):
    return load_table_with_datetime(engine, "humidity_hourly")

# loads wind data
def load_wind_hourly(engine):
    return load_table_with_datetime(engine, "wind_hourly")

# loads temperature data
def load_temperature_daily(engine):
    # executes a query to load the entire table
    df = pd.read_sql("SELECT * FROM temperature_daily_summary", engine)

    # removes any leading/trailing whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # converts the 'data' column to a datetime object (format: day/month/year)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

    return df

# loads weather alert data
def load_weather_alerts(engine):
    df = pd.read_sql("SELECT * FROM weather_alerts", engine)
    df.columns = [c.strip() for c in df.columns]

    return df
