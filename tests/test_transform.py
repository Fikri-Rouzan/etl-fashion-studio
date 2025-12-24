import pandas as pd
from utils.transform import transform_data


def test_transform_success():
    data = {
        "Title": ["Nice Jacket", "Unknown Product"],
        "Price": ["$10.00", None],
        "Rating": ["Rating: ⭐ 4.5 / 5", "Invalid"],
        "Colors": ["3 Colors", None],
        "Size": ["Size: M", "Size: L"],
        "Gender": ["Gender: Men", "Gender: Women"],
        "timestamp": ["2024-01-01", "2024-01-01"],
    }
    df_raw = pd.DataFrame(data)
    df_clean = transform_data(df_raw)

    assert len(df_clean) == 1
    assert df_clean.iloc[0]["Title"] == "Nice Jacket"
    assert df_clean.iloc[0]["Price"] == 160000.0
    assert df_clean.iloc[0]["Size"] == "M"


def test_transform_empty():
    res = transform_data(pd.DataFrame())
    assert res.empty


def test_transform_error_input():
    res = transform_data(None)
    assert res.empty


def test_transform_weird_values():
    data = {
        "Title": ["Test Product"],
        "Price": [object()],
        "Rating": [object()],
        "Colors": ["Not A Number Colors"],
        "Size": [123],
        "Gender": [123],
        "timestamp": ["2024"],
    }
    df = pd.DataFrame(data)
    res = transform_data(df)
    assert res.empty
