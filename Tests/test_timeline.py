from unittest.mock import patch, Mock
from timeline import timeline_statistics


fake_earthquake_data = {
    "features": [
        {"properties": {"time": 1774915200000, "mag": 3.0}},
        {"properties": {"time": 1774958400000, "mag": 5.0}},
        {"properties": {"time": 1775001600000, "mag": 2.5}},
    ]
}




@patch("timeline.requests.get")
def test_timeline_statistics(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: fake_earthquake_data,
    )
    html, html_2, chart_1, chart_2, chart_3 = timeline_statistics("mock_url")
    assert "<table" in html