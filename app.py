from datetime import date, datetime, timedelta, timezone
import pandas as pd
import requests
from flask import Flask, render_template
import plotly.express as px

app = Flask(__name__)

start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
# Vi sätter en tidsgräns och minmagnitude för att inte överskrida USGS API-gränsen på 20 000 händelser (Error 400).
URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude=2.5"

# short test url:
# URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-10-22&minmagnitude=2.5"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/timeline")
def timeline():
    response = requests.get(URL)
    data = response.json()
    table_data = []
    for entry in data["features"]:
        e = entry["properties"]
        timestamp = e.get("time", "")
        event_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        table_data.append(
            {
                "Day": event_date.date(),
                "Location": e.get("place", ""),
                "Magnitude": e.get("mag", ""),
            }
        )
    df = pd.DataFrame(table_data)
    # data_by_day = df.to_html(index=False)

    table = (
        df.groupby("Day")
        .agg(
            Count=("Day", "size"),
            AverageMagnitude=("Magnitude", "mean"),
            MaxMagnitude=("Magnitude", "max"),
        )
        .reset_index()
        .round(1)
    )

    df_2 = pd.DataFrame(table)

    html = df_2.to_html(classes="table table-striped", index=False)

    figure_1 = px.bar(
        table, 
        x="Day", 
        y="Count",
    )
    chart_1 = figure_1.to_html(full_html = False, include_plotlyjs="cdn")

    figure_2 = px.bar(
        table, 
        x="Day", 
        y="AverageMagnitude",
    )
    chart_2 = figure_2.to_html(full_html = False, include_plotlyjs="cdn")

    figure_3 = px.bar(
        table, 
        x="Day", 
        y="MaxMagnitude",
    )
    chart_3 = figure_3.to_html(full_html = False, include_plotlyjs="cdn")
 
    # max_count = table[table["Count"] == table["Count"].max()]
    # strongest_day = table[table["MaxMagnitude"] == table["MaxMagnitude"].max()]
    # highest_average = table[table["AverageMagnitude"] == table["AverageMagnitude"].max()]
    # lowest_average = table[table["AverageMagnitude"] == table["AverageMagnitude"].min()]
    # min_count = table[table["Count"] == table["Count"].min()]
    # mildest_day = table[table["MaxMagnitude"] == table["MaxMagnitude"].min()]
  
    def summary_values(column):
            return ", ".join(str(e) for e in column)

    # summary_df = pd.DataFrame(
    #     {
    #         "": [
    #             "Max earthquakes per day",
    #             "Min earthquakes per day",
    #             "Strongest earthquake",
    #             "Mildest earthquake",
    #             "Highest day average",
    #             "Lowest day average",
    #         ],
    #         "Day": [
    #             summary_values(max_count["Day"].values),
    #             summary_values(min_count["Day"].values),
    #             summary_values(strongest_day["Day"].values),
    #             summary_values(mildest_day["Day"].values),
    #             summary_values(highest_average["Day"].values),
    #             summary_values(lowest_average["Day"].values),
    #         ],
    #         "Value": [
    #             max_count["Count"].iloc[0],
    #             min_count["Count"].iloc[0],
    #             strongest_day["MaxMagnitude"].iloc[0],
    #             mildest_day["MaxMagnitude"].iloc[0],
    #             highest_average["AverageMagnitude"].iloc[0],
    #             lowest_average["AverageMagnitude"].iloc[0],
    #         ],
    #     }
    # )

    summary_rows = [     
        {"name":"Max earthquakes per day",
         "filtered_data": table[table["Count"] == table["Count"].max()],
         "column": "Count"             
         },
        {"name":"Min earthquakes per day",
         "filtered_data": table[table["Count"] == table["Count"].min()],
         "column": "Count"              
         },
        {"name":"Strongest earthquake",
         "filtered_data": table[table["MaxMagnitude"] == table["MaxMagnitude"].max()],
         "column": "MaxMagnitude"              
         },
        {"name":"Mildest earthquake",
         "filtered_data": table[table["MaxMagnitude"] == table["MaxMagnitude"].min()],
         "column": "MaxMagnitude"              
         },
        {"name":"Highest day average",
         "filtered_data": table[table["AverageMagnitude"] == table["AverageMagnitude"].max()],
         "column": "AverageMagnitude"              
         },
        {"name":"Lowest day average",
         "filtered_data": table[table["AverageMagnitude"] == table["AverageMagnitude"].min()],
         "column": "AverageMagnitude"              
         }
    ]

    summary_table = []
    for e in summary_rows:
         summary_table.append({
            "": e["name"],
            "Day": summary_values(e["filtered_data"]["Day"].values),
            "Value": e["filtered_data"][e["column"]].iloc[0]
         })

    summary_df = pd.DataFrame(summary_table)

    html_2 = summary_df.to_html(classes="table table-striped", index=False)

    return render_template("timeline.html", timeline=html, summary=html_2, diagram_1=chart_1, diagram_2=chart_2, diagram_3=chart_3 )
