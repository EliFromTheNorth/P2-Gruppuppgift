from datetime import date, timedelta

import plotly.express as px
from flask import Flask, render_template

from api import hämta_jordskalv
from map import skapa_karta
from processing import process_earthquakes
from timeline import timeline_statistics

app = Flask(__name__)

start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude=2.5"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/magnitude")
def magnitude():
    # Hämtar jordskalvsdata från USGS API
    data = hämta_jordskalv(URL)
    # Returnerar felmeddelandet och statuskod 503
    if isinstance(data, str):
        return render_template("magnitudes.html", table=None, fel=data, graph=None), 503
    # Processar jordskalvsdata och grupperar den efter magnitud
    grouped_df = process_earthquakes(data)
    # Konverterar den grupperade DataFrame till en lista av dictionaries
    table = grouped_df.to_dict(orient="records")
    # simpelt plotly-diagram som visar medeldjupet för skalven
    fig = px.bar(
        grouped_df,
        x="Kategori",
        y="Genomsnittligt_djup",
        color="Kategori",
        title="minor <5.0, major >=5.0",
    )

    graph = fig.to_html(full_html=False)

    # Renderar magnitudes.html
    return render_template("magnitudes.html", table=table, error=None, graph=graph)


@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404


@app.route("/timeline")
def timeline():
    """Route för tidslinjesidan som visar statistik och diagram över jordbävningar."""
    # Hämtar bearbetad HTML-data och diagram från timeline-modulen
    html, html_2, chart_1, chart_2, chart_3 = timeline_statistics(URL)

    # Om funktionen returnerade ett felmeddelande istället för en tabell
    if "<table" not in html:
        return render_template(
            "timeline.html",
            fel=html,
            html=None,
            html_2=None,
            chart_1=None,
            chart_2=None,
            chart_3=None,
        ), 503

    # Om allt gick bra, skicka data och diagram till mallen
    return render_template(
        "timeline.html",
        timeline=html,
        summary=html_2,
        diagram_1=chart_1,
        diagram_2=chart_2,
        diagram_3=chart_3,
    )


@app.route("/map")
def visa_karta():
    """Visar den geografiska kartan över jordskalv."""

    # Skickar api addressen till kartfunktionen och tar emot dess resultat.
    karta, fel, statuskod = skapa_karta(URL)

    # Om ett felmeddelande finns visas det på kartans sida.
    if fel:
        return render_template(
            "map.html",
            karta=None,
            fel=fel
        ), statuskod

    # Om allt fungerar skickas kartans html till map.html.
    return render_template("map.html", karta=karta)


if __name__ == "__main__":
    app.run(debug=True)
