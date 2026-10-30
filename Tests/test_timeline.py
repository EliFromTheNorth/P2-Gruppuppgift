from unittest.mock import patch, Mock
from timeline import timeline_statistics, earthquake_data, summary_table
from datetime import date
import pandas as pd

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

    # test for summary_table():

def test_summary_table():
    mock_table = pd.DataFrame([
    {"Day": date(2026, 3, 31), "Count": 2, "AverageMagnitude": 4.0, "MaxMagnitude": 5.0},
    {"Day": date(2026, 4, 1), "Count": 1, "AverageMagnitude": 2.5, "MaxMagnitude": 2.5} ])

    expected_data = {
        "Max earthquakes per day": {"Day": "2026-03-31", "Value": "2"},
        "Min earthquakes per day": {"Day": "2026-04-01", "Value": "1"},
        "Strongest earthquake": {"Day": "2026-03-31", "Value": "5.0"},
        "Mildest earthquake": {"Day": "2026-04-01", "Value": "2.5"},
        "Highest day average": {"Day": "2026-03-31", "Value": "4.0"},
        "Lowest day average": {"Day": "2026-04-01", "Value": "2.5"},
    }

    result = summary_table(mock_table)
    assert result.notnull().all().all()
    for name, expected in expected_data.items():
        row = result[result.iloc[:, 0] == name].iloc[0]
        assert row["Day"] == expected["Day"]
        assert row["Value"] == expected["Value"]





    # test for charts()?
    # integration test for timeline_statistics()?

