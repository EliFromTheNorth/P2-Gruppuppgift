import requests


def hämta_jordskalv(url):
    """Hämtar jordskalvsdata från USGS API och returnerar det som en JSON-struktur"""

    try:
        ### Tests:
        # svar = requests.get(url, timeout=(2, 0.000000000000010)) #TEST - FEL: "Servern svarade inte i tid (Timeout)"
        # svar = requests.get(url, timeout=0.00000000005) #TEST - FEL: Kunde inte nå servern. Kontrollera din internetanslutning.
        # svar = requests.get("https://httpbin.org/status/401") #TEST - FEL: HTTP-fel! Felkod: {e.response.status_code}
        # svar = requests.get("https://httpbin.org/html") #TEST - FEL: Kunde inte tolka data från servern (ogiltig JSON).
        # svar = requests.get("invalid-adress-12345") #TEST - FEL: return "Ett nätverksfel uppstod vid hämtning av data."

        svar = requests.get(url, timeout=10)
        svar.raise_for_status()  # Kontrollerar om servern svarade med ett HTTP-fel
        return svar.json() #Omvandlar json svaret till python data.

    except requests.Timeout:
        return "Servern svarade inte i tid (Timeout)"
    except requests.HTTPError as e:
        status = e.response.status_code if e.response else "okänd"
        return f"HTTP-fel! Felkod: {status}"
    except requests.ConnectionError:
        return "Kunde inte nå servern. Kontrollera din internetanslutning."
    except ValueError:
        return "Kunde inte tolka data från servern (ogiltig JSON)."
    except requests.exceptions.RequestException:
        return "Ett nätverksfel uppstod vid hämtning av data."
