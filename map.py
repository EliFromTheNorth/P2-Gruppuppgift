import plotly.express as px

from api import hämta_jordskalv
from bearbetning import skapa_dataframe


def skapa_karta(data):
    data = hämta_jordskalv(data)

    if isinstance(data, str):
        return None, data, 503  # Returnerar felmeddelandet och statuskod 503
    
    if data is None:
        return None, "Kunde inte hämta jordskalvsdata just nu.", 503

    df = skapa_dataframe(data)

    if df.empty:
        return None, "Inga jordskalv hittades för det valda urvalet.", 200

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

    karta_html = figur.to_html(
        full_html=False,
        include_plotlyjs="cdn",
    )

    return karta_html, None, 200
