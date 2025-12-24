import pandas as pd
from unittest.mock import patch, MagicMock
from utils.extract import extract_data

MOCK_HTML = """
<html>
    <body>
        <div class="collection-card">
            <h3 class="product-title">Hoodie Test</h3>
            <span class="price">$50.00</span>
            <div class="product-details">
                <p>Rating: ⭐ 4.0 / 5</p>
                <p>2 Colors</p>
                <p>Size: L</p>
                <p>Gender: Men</p>
            </div>
        </div>
    </body>
</html>
"""

MOCK_HTML_EMPTY = "<html><body><div>No Products Here</div></body></html>"


@patch("utils.extract.requests.get")
def test_extract_success_pagination(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML
    mock_get.return_value = mock_response

    df = extract_data("http://dummy-url.com", total_pages=2)

    assert not df.empty
    assert len(df) == 2
    assert df.iloc[0]["Title"] == "Hoodie Test"


@patch("utils.extract.requests.get")
def test_extract_fallback_logic(mock_get):
    response_fail = MagicMock()
    response_fail.status_code = 404
    response_ok = MagicMock()
    response_ok.status_code = 200
    response_ok.content = MOCK_HTML
    mock_get.side_effect = [response_fail, response_ok]

    df = extract_data("http://dummy-url.com", total_pages=1)

    assert not df.empty
    assert len(df) == 1
    assert mock_get.call_count == 2


@patch("utils.extract.requests.get")
def test_extract_no_products(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = MOCK_HTML_EMPTY
    mock_get.return_value = mock_response

    df = extract_data("http://dummy-url.com", total_pages=1)

    assert df.empty
    assert "Title" not in df.columns


@patch("utils.extract.requests.get")
def test_extract_parsing_error(mock_get):
    BAD_HTML = """
    <div class="collection-card">
        </div>
    """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = BAD_HTML
    mock_get.return_value = mock_response

    df = extract_data("http://dummy-url.com", total_pages=1)

    assert not df.empty
    assert df.iloc[0]["Title"] == "Unknown Product"


@patch("utils.extract.requests.get")
def test_extract_connection_error(mock_get):
    mock_get.side_effect = Exception("Connection Refused")
    df = extract_data("http://dummy-url.com", total_pages=1)

    assert df.empty
    assert isinstance(df, pd.DataFrame)
