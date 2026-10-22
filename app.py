from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests

app = Flask(__name__)

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-03-01"

@app.route('/')
def index():
    return render_template('index.html')