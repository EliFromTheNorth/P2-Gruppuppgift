from unittest.mock import patch

from app import app


def test_map_visas():
    """Kontrollerar att kartan visas när api data hämtas korrekt."""

    #Skapar exempeldata som liknar ett svar från USGS api.
    exempeldata = {
        "features": [
            {
                "properties": {"place": "Example city", "mag": 4.5},
                "geometry": {"coordinates": [18.0, 59.0, 12.0]},
            }
        ]
    }

    #Ersätter api anropet med exempeldata och skapar en testklient för Flask.
    with (
        patch("map.hämta_jordskalv", return_value=exempeldata),
        app.test_client() as klient,
    ):
        #Skickar en Get förfrågan till kartans route.
        svar = klient.get("/map")

        #Kontrollerar att sidan returnerar hhtp statuskod 200.
        assert svar.status_code == 200

        #Kontrollerar att kartans rubruk finns i html svaret.
        assert "Jordskalv världen över" in svar.get_data(as_text=True)


@patch("map.hämta_jordskalv", return_value=None)
def test_map_api_fel(mock_hämta):
    """Kontrollerar att kartan visar ett fel när api data saknas."""

    #Skapar en testklient för att kunna skicka en förfrågan till Flask.
    with app.test_client() as klient:
        
        #Skickar en Get förfrågan till kartans route.
        svar = klient.get("/map")

        #Kontrollerar att sidan returnerar html statuskod 503.
        assert svar.status_code == 503

        #Kontrollerar att rätt felmeddelande visas på sidan.
        assert "Kunde inte hämta jordskalvsdata just nu." in svar.get_data(as_text=True)
