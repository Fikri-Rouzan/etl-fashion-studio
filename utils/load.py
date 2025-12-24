import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine


def load_data_csv(df, output_filename="products.csv"):
    print("\nStarting the loading process to CSV...")

    try:
        if df.empty:
            print("DataFrame is empty, CSV is skipped.")
            return

        df.to_csv(output_filename, index=False)

        print(f"Success: Data saved to {output_filename}")
    except PermissionError:
        print(
            f"ERROR: the '{output_filename}' file is currently open. Please close it and try again."
        )
    except Exception as e:
        print(f"ERROR While Loading CSV: {e}")


def load_data_sheets(df, json_cred_path, spreadsheet_id):
    print("\nStarting the loading process to Google Sheets...")

    try:
        if df.empty:
            print("DataFrame is empty, Google Sheets is skipped.")
            return

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        if not os.path.exists(json_cred_path):
            print(f"ERROR: The '{json_cred_path}' file was not found.")
            return

        creds = Credentials.from_service_account_file(json_cred_path, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).sheet1

        df_str = df.astype(str)
        sheet.clear()
        data_to_upload = [df_str.columns.tolist()] + df_str.values.tolist()
        sheet.update(range_name="A1", values=data_to_upload)

        print("Success: Data was successfully uploaded to Google Sheets")
    except Exception as e:
        print(f"ERROR While Loading Google Sheets: {e}")


def load_data_postgres(df, db_config):
    print("\nStarting the loading process to PostgreSQL...")

    try:
        if df.empty:
            print("DataFrame is empty, PostgreSQL is skipped.")
            return

        db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

        engine = create_engine(db_url)

        with engine.connect() as connection:
            df.to_sql(name="products", con=connection, if_exists="replace", index=False)

        print("Success: Data successfully saved to 'products' table in PostgreSQL")

    except Exception as e:
        print(f"ERROR While Loading PostgreSQL: {e}")
        print(
            "Tip: Make sure the database has been created and the credentials (username/password) are correct."
        )


def load_main(df, spreadsheet_id=None, db_config=None):
    load_data_csv(df)

    if spreadsheet_id:
        json_path = "google-sheets-api.json"
        load_data_sheets(df, json_path, spreadsheet_id)

    if db_config:
        load_data_postgres(df, db_config)
