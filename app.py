from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, date, timedelta

app = Flask(__name__)

start_date = date.today() - timedelta(days=30)
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&minmagnitude=2.5"


@app.route('/')
def index():
    return render_template('index.html')