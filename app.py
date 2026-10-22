from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests

app = Flask(__name__)

# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-09-01&minmagnitude=2.5"

@app.route('/')
def index():
    return render_template('index.html')