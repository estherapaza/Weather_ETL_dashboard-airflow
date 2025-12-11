# import libraries
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# loading variables from .env file
load_dotenv()

# postgresql database connection
def get_db_engine():
    # parameters for database connection
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    # building the engine with sqlalchemy
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # returns an engine object to connect to the database
    return engine