import requests

def hämta_jordskalv(url):
    """Hämtar jordskalvsdata från USGS API och returnerar det som en JSON-struktur."""

    try:
        svar = requests.get(url, timeout=(2, 0.000000000000010)) #TEST - FEL: "Servern svarade inte i tid (Timeout)"
        # svar = requests.get(url, timeout=0.00000000005) #FEL: Kunde inte nå servern. Kontrollera din internetanslutning.
        # svar = requests.get(url, timeout=10)
        svar.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return svar.json()

    # except (requests.exceptions.RequestException, ValueError): # original
    except requests.exceptions.RequestException:
        return None
    except requests.Timeout:
        return "Servern svarade inte i tid (Timeout)"
    except requests.HTTPError as e:
        return f"HTTP-fel! Felkod: {e.response.status_code}"
    except requests.ConnectionError:
        return "Kunde inte nå servern. Kontrollera din internetanslutning."
    except ValueError:
        return "Kunde inte tolka data från servern (ogiltig JSON)."
