from datetime import timezone, date, datetime, timedelta

import pandas as pd
import plotly.express as px
# import requests
from flask import Flask, render_template
from timeline import timeline_statistics

app = Flask(__name__)

start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude=2.5"

@app.route("/")
def index():
    return render_template("index.html")


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

