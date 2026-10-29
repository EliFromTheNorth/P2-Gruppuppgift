from datetime import date, datetime, timedelta, timezone

import pandas as pd
import plotly.express as px
import requests

def earthquake_data(url):
    response = requests.get(url)
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
    print(table)
    return table

def summary_table(table):
    def summary_values(column):
        return ", ".join(str(e) for e in column)
    
    summary_rows = [
        {
            "name": "Max earthquakes per day",
            "filtered_data": table[table["Count"] == table["Count"].max()],
            "column": "Count",
        },
        {
            "name": "Min earthquakes per day",
            "filtered_data": table[table["Count"] == table["Count"].min()],
            "column": "Count",
        },
        {
            "name": "Strongest earthquake",
            "filtered_data": table[
                table["MaxMagnitude"] == table["MaxMagnitude"].max()
            ],
            "column": "MaxMagnitude",
        },
        {
            "name": "Mildest earthquake",
            "filtered_data": table[
                table["MaxMagnitude"] == table["MaxMagnitude"].min()
            ],
            "column": "MaxMagnitude",
        },
        {
            "name": "Highest day average",
            "filtered_data": table[
                table["AverageMagnitude"] == table["AverageMagnitude"].max()
            ],
            "column": "AverageMagnitude",
        },
        {
            "name": "Lowest day average",
            "filtered_data": table[
                table["AverageMagnitude"] == table["AverageMagnitude"].min()
            ],
            "column": "AverageMagnitude",
        },
    ]
    
    summary_table = []
    for e in summary_rows:
        summary_table.append(
            {
                "": e["name"],
                "Day": summary_values(e["filtered_data"]["Day"].values),
                "Value": str(int(e["filtered_data"][e["column"]].iloc[0]))
                if e["column"] == "Count"
                else str(e["filtered_data"][e["column"]].iloc[0]),
            }
        )

    summary_df = pd.DataFrame(summary_table)
    html_2 = summary_df.to_html(classes="table table-striped", index=False)
    return html_2

def charts(table):
    figure_1 = px.bar(
            table,
            x="Day",
            y="Count",
        )
    chart_1 = figure_1.to_html(full_html=False, include_plotlyjs="cdn")
    
    figure_2 = px.bar(
            table,
            x="Day",
            y="AverageMagnitude",
        )
    chart_2 = figure_2.to_html(full_html=False, include_plotlyjs="cdn")
    
    figure_3 = px.bar(
            table,
            x="Day",
            y="MaxMagnitude",
        )
    chart_3 = figure_3.to_html(full_html=False, include_plotlyjs="cdn")
    return chart_1, chart_2, chart_3

def timeline_statistics(url):
    table = earthquake_data(url)

    html = table.to_html(classes="table table-striped", index=False)
    html_2 = summary_table(table)
    chart_1, chart_2, chart_3 = charts(table)  

    return html, html_2, chart_1, chart_2, chart_3