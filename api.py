import requests


def hämta_jordskalv(url):
    """Hämtar jordskalvsdata från USGS API och returnerar det som en JSON-struktur."""

    try:
        svar = requests.get(url, timeout=10)
        svar.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return svar.json()

    except (requests.exceptions.RequestException, ValueError):
        return None
