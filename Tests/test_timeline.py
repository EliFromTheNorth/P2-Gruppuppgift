from unittest.mock import patch, Mock
from timeline import timeline_statistics, earthquake_data

fake_earthquake_data = {
    "features": [
        {"properties": {"time": 1774915200000, "mag": 3.0}},
        {"properties": {"time": 1774958400000, "mag": 5.0}},
        {"properties": {"time": 1775001600000, "mag": 2.5}},
    ]
}

@patch("timeline.requests.get")
def test_earthquake_data(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: fake_earthquake_data,
    )
    table = earthquake_data("url")
    assert len(table) == 2

    row_day_1 = table.iloc[0]
    assert row_day_1["Count"] == 2
    assert row_day_1["AverageMagnitude"] == 4.0
    assert row_day_1["MaxMagnitude"] == 5.0
    
    row_day_2 = table.iloc[1]
    assert row_day_2["Count"] == 1
    assert row_day_2["AverageMagnitude"] == 2.5
    assert row_day_2["MaxMagnitude"] == 2.5