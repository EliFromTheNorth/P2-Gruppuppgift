import plotly.express as px

from api import hämta_jordskalv
from bearbetning import skapa_dataframe


def skapa_karta(url):
    """Hämtar jordskalvsdata och skapar en interaktiv karta med plotly"""

    # Hämta jordskalvdata från USGS med URL som skickas in.
    data = hämta_jordskalv(url)

    # Kontrollera om API funktionen har returnerat ett felmedelande.
    if isinstance(data, str):
        return None, data, 503  # Returnerar felmeddelandet och statuskod 503

    # Kontrollera om data saknas helt.
    if data is None:
        return None, "Kunde inte hämta jordskalvsdata just nu.", 503

    df = skapa_dataframe(data)

    # Kontrollera om DataFrame saknar jordskalv.
    if df.empty:
        return None, "Inga jordskalv hittades för det valda urvalet.", 200

    # Skapa en geografisk karta där varje punkt representerar ett jordskalv.
    figur = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="place",
        color="mag",
        hover_data={
            "mag": True,
            "depth": True,
            "time": True,
            "latitude": False,
            "longitude": False,
        },
        labels={
            "mag": "Magnitud",
            "depth": "Djup (km)",
            "time": "Tid (UTC)",
        },
        title=None,
        projection="natural earth",
        height=750,
    )

    # Omvandla plotly figuren till html så att den kan visas i flask.
    karta_html = figur.to_html(
        full_html=False,
        include_plotlyjs="cdn",
    )

    # Returnerar kartans html, inget felmeddelande och http statuskod 200.
    return karta_html, None, 200
