import pandas as pd
from processing import process_earthquakes
import requests
from datetime import date, timedelta
from flask import Flask, render_template

app = Flask(__name__)

start_date = date.today() - timedelta(days=30)
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&minmagnitude=2.5"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/magnitude', methods=['GET'])
def magnitude():
 req = requests.get(URL, timeout=10)
 data = req.json()

 grouped_df = process_earthquakes(data)

 table = grouped_df.to_dict(orient="records")

 return render_template("magnitudes.html",table=table)


if __name__ == "__main__":
    app.run(debug=True)