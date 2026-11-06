from unittest.mock import patch

import requests

from api import hämta_jordskalv


@patch("api.requests.get")
def test_hämta_jordskalv_nätverksfel(mock_get):
    """Kontrollerar att timeout ger rätt felmeddelande."""

    # Simulera att api servern inte svarar i tid.
    mock_get.side_effect = requests.exceptions.Timeout

    result = hämta_jordskalv("test-url")

    assert result == "Servern svarade inte i tid (Timeout)"
    mock_get.assert_called_once()


@patch("api.requests.get")
def test_hämta_jordskalv_lyckas(mock_get):
    """Kontrollerar att api data returneras när anropet lyckas."""

    # Skapar ett simulerat json svar från api.
    förväntat_data = {"features": []}
    mock_svar = mock_get.return_value
    mock_svar.json.return_value = förväntat_data

    resultat = hämta_jordskalv("test-url")

    assert resultat == förväntat_data
    mock_svar.raise_for_status.assert_called_once()


@patch("api.requests.get")
def test_hämta_jordskalv_http_fel(mock_get):
    """Kontrollerar att http fel ger rätt statuskod i felmeddelandet."""

    # Simulerar ett http fel.
    mock_svar = mock_get.return_value
    mock_svar.raise_for_status.side_effect = requests.exceptions.HTTPError("Serverfel")

    resultat = hämta_jordskalv("test-url")

    assert resultat == "HTTP-fel! Felkod: okänd"
    mock_svar.raise_for_status.assert_called_once()
