from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, date, timedelta

app = Flask(__name__)

# start_date = date.today() - timedelta(days=30)
# # Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
# URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&minmagnitude=2.5"

# short test url:
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-10-22&minmagnitude=2.5"
# URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={date.today()}&minmagnitude=2.5"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline():
    response = requests.get(URL)
    data = response.json()
    table_data = []
    for entry in data['features']:
        e = entry['properties']
        timestamp = e.get("time", "")
        event_date = datetime.fromtimestamp(timestamp/1000)
        table_data.append({
            "Day": event_date.date(),
            "Location": e.get("place", ""), 
            "Magnitude": e.get("mag", ""),
        })
    df = pd.DataFrame(table_data)
    html = df.to_html(classes="table table-striped", index=False)

    table_2 = df.groupby("Day").agg(
        Count=("Day", "size"),
        AverageMagnitude =("Magnitude", "mean"),
        MaxMagnitude = ("Magnitude", "max")
    ).reset_index()
    
    print(table_2)

    
    return render_template("timeline.html", timeline=html)
