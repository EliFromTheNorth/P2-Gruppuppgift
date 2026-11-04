from datetime import date, timedelta

import plotly.express as px

# import requests
from flask import Flask, render_template

from api import hämta_jordskalv
from bearbetning import skapa_dataframe
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
    # Processar jordskalvsdata och grupperar den efter magnitud
    grouped_df = process_earthquakes(data)
    # Konverterar den grupperade DataFrame till en lista av dictionaries 
    table = grouped_df.to_dict(orient="records")
    # simpelt plotly-diagram som visar medeldjupet för skalven
    fig = px.bar(
        grouped_df,
        x="Category",
        y="Average_depth",
        color="Category",
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
    html, html_2, chart_1, chart_2, chart_3 = timeline_statistics(URL)
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
    data = hämta_jordskalv(URL)

    if data is None:
        return render_template(
            "map.html",
            karta=None,
            fel="Kunde inte hämta jordskalvsdata just nu.",
        ), 503

    df = skapa_dataframe(data)

    if df.empty:
        return render_template(
            "map.html",
            karta=None,
            fel="Inga jordskalv hittades för det valda urvalet.",
        )

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

    return render_template("map.html", karta=karta_html)


if __name__ == "__main__":
    app.run(debug=True)
