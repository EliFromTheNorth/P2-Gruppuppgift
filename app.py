import pandas as pd

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

 earthquake_list = []
 for quakes in data["features"]:

        magnitud = round(quakes["properties"]["mag"], 2)
        plats = quakes["properties"]["place"]

        if magnitud is None:
            continue

        if magnitud >= 5:
            kategori = "Major"
        else:
            kategori = "Minor"

        earthquake_list.append({
            "magnitud": magnitud,
            "plats": plats,
            "kategori": kategori
        })
 
 return render_template('magnitude.html', data=data, earthquake_list=earthquake_list)


if __name__ == "__main__":
    app.run(debug=True)