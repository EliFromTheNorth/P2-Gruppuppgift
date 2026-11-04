from unittest.mock import patch

from app import app


def test_map_visas():
    exempeldata = {
        "features": [
            {
                "properties": {"place": "Example city", "mag": 4.5},
                "geometry": {"coordinates": [18.0, 59.0, 12.0]},
            }
        ]
    }

    with (
        patch("app.hämta_jordskalv", return_value=exempeldata),
        app.test_client() as klient,
    ):
        svar = klient.get("/map")

        assert svar.status_code == 200
        assert "Jordskalv världen över" in svar.get_data(as_text=True)


@patch("map.hämta_jordskalv", return_value=None)
def test_map_api_fel(mock_hämta):
    with app.test_client() as klient:
        svar = klient.get("/map")

        assert svar.status_code == 503
        assert "Kunde inte hämta jordskalvsdata just nu." in svar.get_data(as_text=True)
