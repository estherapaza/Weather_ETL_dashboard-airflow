# import libraries
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# database credentials from environment variables
load_dotenv()

db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]

# loads data into the database
def load_data_to_postgres():
    # generated csv directory
    data_dir = "/opt/airflow/data"

    # maps file names to table names
    files_to_tables = {
        "weather_weekly_transformed.csv": "weather_hourly_one_week",
        "daily_temperature_summary.csv": "temperature_daily_summary",
        "temperature_hourly.csv": "temperature_hourly",
        "precipitation_hourly.csv": "precipitation_hourly",
        "humidity_hourly.csv": "humidity_hourly",
        "wind_hourly.csv": "wind_hourly",
        "weather_alerts.csv": "weather_alerts"
    }

    # database connection
    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

    # loading and writing each file to the database
    for filename, table_name in files_to_tables.items():
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists="replace", index=False)