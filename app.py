import pandas as pd
from processing import process_earthquakes
import requests
from datetime import timezone, date, datetime, timedelta
# import plotly.express as px
from flask import Flask, render_template
from timeline import timeline_statistics
from bearbetning import skapa_dataframe
# from api import hämta_jordskalv
from map import skapa_karta


app = Flask(__name__)

start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude=2.5"


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/magnitude', methods=['GET'])
def magnitude():
 req = requests.get(URL, timeout=10)
 data = req.json()

 grouped_df = process_earthquakes(data)

 table = grouped_df.to_dict(orient="records")

 return render_template("magnitudes.html",table=table)

@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404

@app.route("/timeline")
def timeline():
    html, html_2, chart_1, chart_2, chart_3 = timeline_statistics(URL)

    if "<table" not in html:
        return render_template(
            "timeline.html",
            fel=html,
            html = None, 
            html_2 = None,
            chart_1 = None,
            chart_2 = None,
            chart_3 = None
        ), 503
    
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
