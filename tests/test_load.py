import warnings
import pandas as pd
from unittest.mock import patch
from utils.load import load_main, load_data_csv, load_data_sheets, load_data_postgres

df_dummy = pd.DataFrame({"Title": ["Test"], "Price": [1000]})


@patch("utils.load.pd.DataFrame.to_csv")
def test_load_csv_success(mock_to_csv):
    load_data_csv(df_dummy, "test.csv")
    mock_to_csv.assert_called_once()


def test_load_csv_permission_error():
    with patch(
        "utils.load.pd.DataFrame.to_csv", side_effect=PermissionError("Open file")
    ):
        load_data_csv(df_dummy, "test.csv")


def test_load_csv_empty():
    load_data_csv(pd.DataFrame(), "test.csv")


@patch("utils.load.os.path.exists")
@patch("utils.load.Credentials.from_service_account_file")
@patch("utils.load.gspread.authorize")
def test_load_sheets_success(mock_auth, mock_sheets, mock_exists):
    mock_client = mock_auth.return_value
    mock_sheet = mock_client.open_by_key.return_value.sheet1
    mock_exists.return_value = True
    load_data_sheets(df_dummy, "dummy.json", "dummy_id")
    mock_sheet.update.assert_called()


def test_load_sheets_empty():
    load_data_sheets(pd.DataFrame(), "dummy.json", "dummy_id")


@patch("utils.load.os.path.exists")
def test_load_sheets_no_file(mock_exists):
    mock_exists.return_value = False
    load_data_sheets(df_dummy, "dummy.json", "dummy_id")


@patch("utils.load.create_engine")
def test_load_postgres_success(mock_engine):
    mock_conn = mock_engine.return_value.connect.return_value.__enter__.return_value
    db_config = {
        "host": "h",
        "port": "1",
        "database": "db",
        "username": "u",
        "password": "p",
    }

    warnings.filterwarnings(
        "ignore", message=".*pandas only supports SQLAlchemy connectable.*"
    )

    load_data_postgres(df_dummy, db_config)
    mock_engine.assert_called_once()


def test_load_postgres_empty():
    load_data_postgres(pd.DataFrame(), {})


@patch("utils.load.create_engine")
def test_load_postgres_error(mock_engine):
    mock_engine.side_effect = Exception("DB Connection Failed")

    db_config = {
        "host": "h",
        "port": "1",
        "database": "db",
        "username": "u",
        "password": "p",
    }
    load_data_postgres(df_dummy, db_config)


@patch("utils.load.load_data_postgres")
@patch("utils.load.load_data_sheets")
@patch("utils.load.load_data_csv")
def test_load_main(mock_csv, mock_sheets, mock_pg):
    dummy_db_config = {"host": "localhost"}
    load_main(df_dummy, spreadsheet_id="abc", db_config=dummy_db_config)

    mock_csv.assert_called_once()
    mock_sheets.assert_called_once()
    mock_pg.assert_called_once()
