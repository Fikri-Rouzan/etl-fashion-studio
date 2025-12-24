import os
from dotenv import load_dotenv
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_main

load_dotenv()

if __name__ == "__main__":
    BASE_URL = "https://fashion-studio.dicoding.dev"

    SHEET_ID = os.getenv("SHEET_ID")

    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_DATABASE"),
        "username": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
    }

    if not SHEET_ID:
        print("WARNING: SHEET_ID is not filled in .env file\n")

    required_values = [value for key, value in DB_CONFIG.items() if key != "password"]

    if not all(required_values):
        print(
            "WARNING: Database configuration (host/port/database/username) is not completely filled in .env file\n"
        )

    df_raw = extract_data(BASE_URL, total_pages=50)

    if not df_raw.empty:
        df_clean = transform_data(df_raw)

        load_main(df_clean, spreadsheet_id=SHEET_ID, db_config=DB_CONFIG)
    else:
        print("Data is empty, pipeline is stopped.\n")
