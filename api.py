import requests


def hämta_jordskalv(url):
    """Hämtar jordskalvsdata från USGS API."""

    try:
        svar = requests.get(url, timeout=10)
        svar.raise_for_status()
        return svar.json()

    except requests.Timeout:
        return "Servern svarade inte i tid (Timeout)."

    except requests.HTTPError as e:
        return f"HTTP-fel! Felkod: {e.response.status_code}"

    except requests.ConnectionError:
        return "Kunde inte nå servern. Kontrollera din internetanslutning."

    except ValueError:
        return "Kunde inte tolka data från servern (ogiltigt JSON)."

    except requests.exceptions.RequestException:
        return "Ett nätverksfel uppstod vid hämtning av data."
