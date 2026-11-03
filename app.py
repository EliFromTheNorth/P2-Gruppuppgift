from datetime import date, timedelta

import plotly.express as px
from flask import Flask, render_template

from bearbetning import skapa_dataframe
from api import hämta_jordskalv
from map import skapa_karta

app = Flask(__name__)

start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude=2.5"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def visa_karta():
    karta, fel, statuskod = skapa_karta(URL)

    if fel:
        return render_template(
            "map.html",
            karta=None,
            fel=fel
        ),statuskod

    return render_template("map.html", karta=karta)



if __name__ == "__main__":
    app.run(debug=True)
