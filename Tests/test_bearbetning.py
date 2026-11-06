from bearbetning import skapa_dataframe


def test_skapa_dataframe():
    """Kontrollerar att JSON-data omvandlas korrekt till en DataFrame."""

    # Skapar exempeldata som efterliknar ett svar från USGS API.
    data = {
        "features": [
            {
                "properties": {"place": "10 km north of example city", "mag": 4.5},
                "geometry": {"coordinates": [18.0, 59.0, 12.0]},
            }
        ]
    }

    # Skapar en DataFrame från den simulerade API-datan.
    df = skapa_dataframe(data)

    # Kontrollerar att DataFrame innehåller ett jordskalv.
    assert len(df) == 1

    # Kontrollerar att platsen har hämtats korrekt.
    assert df.iloc[0]["place"] == "10 km north of example city"

    # Kontrollerar att magnituden har hämtats korrekt.
    assert df.iloc[0]["mag"] == 4.5

    # Kontrollerar att longituden har hämtats korrekt.
    assert df.iloc[0]["longitude"] == 18.0

    # Kontrollerar att latituden har hämtats korrekt.
    assert df.iloc[0]["latitude"] == 59.0

    # Kontrollerar att djupet har hämtats korrekt.
    assert df.iloc[0]["depth"] == 12.0
