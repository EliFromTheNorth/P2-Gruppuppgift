from datetime import date
from unittest.mock import Mock, patch

import pandas as pd

from timeline import earthquake_data, summary_table

# Skapar mockad jordbävningsdata för testning
fake_earthquake_data = {
    "features": [
        {"properties": {"time": 1774915200000, "mag": 3.0}},
        {"properties": {"time": 1774958400000, "mag": 5.0}},
        {"properties": {"time": 1775001600000, "mag": 2.5}},
    ]
}


@patch("api.requests.get")
def test_earthquake_data(mock_get):
    """Testar att earthquake_data bearbetar JSON-datan korrekt per dag."""
    # Mockar API-anropet så att det returnerar simulerade data
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: fake_earthquake_data,
    )
    table = earthquake_data("url")
    assert len(table) == 2

    # Kontrollerar statistiken för första dagen
    row_day_1 = table.iloc[0]
    assert row_day_1["Count"] == 2
    assert row_day_1["AverageMagnitude"] == 4.0
    assert row_day_1["MaxMagnitude"] == 5.0

    # Kontrollerar statistiken för andra dagen
    row_day_2 = table.iloc[1]
    assert row_day_2["Count"] == 1
    assert row_day_2["AverageMagnitude"] == 2.5
    assert row_day_2["MaxMagnitude"] == 2.5


def test_summary_table():
    """Testar att summary_table genererar rätt extremer (högst/lägst/flest)."""
    # Skapar en mockad tabell att testa sammanfattningsfunktionen på
    mock_table = pd.DataFrame(
        [
            {
                "Day": date(2026, 3, 31),
                "Count": 2,
                "AverageMagnitude": 4.0,
                "MaxMagnitude": 5.0,
            },
            {
                "Day": date(2026, 4, 1),
                "Count": 1,
                "AverageMagnitude": 2.5,
                "MaxMagnitude": 2.5,
            },
        ]
    )

    # Det förväntade resultatet från sammanfattningen
    expected_data = [
        {"": "Flest jordbävningar per dag", "Datum": "2026-03-31", "Värde": "2"},
        {"": "Färst jordbävningar per dag", "Datum": "2026-04-01", "Värde": "1"},
        {"": "Kraftigaste jordbävningen", "Datum": "2026-03-31", "Värde": "5.0"},
        {"": "Svagaste jordbävningen", "Datum": "2026-04-01", "Värde": "2.5"},
        {"": "Högsta dagsgenomsnitt", "Datum": "2026-03-31", "Värde": "4.0"},
        {"": "Lägsta dagsgenomsnitt", "Datum": "2026-04-01", "Värde": "2.5"},
    ]

    # Kör funktionen och jämför att det genererade matchar förväntat resultat
    generated_summary = summary_table(mock_table)
    assert generated_summary.to_dict("records") == expected_data
