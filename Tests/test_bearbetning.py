from bearbetning import skapa_dataframe


def test_skapa_dataframe():
    data = {
        "features": [
            {
                "properties": {"place": "10 km north of example city", "mag": 4.5},
                "geometry": {"coordinates": [18.0, 59.0, 12.0]},
            }
        ]
    }

    df = skapa_dataframe(data)

    assert len(df) == 1
    assert df.iloc[0]["place"] == "10 km north of example city"
    assert df.iloc[0]["mag"] == 4.5
    assert df.iloc[0]["longitude"] == 18.0
    assert df.iloc[0]["latitude"] == 59.0
    assert df.iloc[0]["depth"] == 12.0
