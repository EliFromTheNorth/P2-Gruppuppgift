from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import requests
from api import hämta_jordskalv


def earthquake_data(url):
    data = hämta_jordskalv(url)
    if type(data) == str:
        return data
    elif not data:
        return "Kunde inte hämta data."

    table_data = []
    for entry in data["features"]:
        e = entry["properties"]
        timestamp = e.get("time", "")
        event_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        table_data.append({"Day": event_date.date(), "Magnitude": e.get("mag", "")})
   
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
    table["Day"] = pd.to_datetime(table["Day"]).dt.strftime('%d %b')
    return table

def summary_table(table):
    summary_rows = [
        ("Flest jordbävningar per dag", "Count", max),
        ("Färst jordbävningar per dag", "Count", min),
        ("Kraftigaste jordbävningen", "MaxMagnitude", max),
        ("Svagaste jordbävningen", "MaxMagnitude", min),
        ("Högsta dagsgenomsnitt", "AverageMagnitude", max),
        ("Lägsta dagsgenomsnitt", "AverageMagnitude", min),
    ]
   
    summary_table = []
    for name, column, func in summary_rows:
        value = func(table[column])
        filtered_data = table[table[column] == value]
        dates = ", ".join(str(date) for date in filtered_data["Day"].values)
        value_format = str(int(value)) if column == "Count" else str(value)

        summary_table.append(
            {
                "": name,
                "Datum": dates,
                "Värde": value_format
            }
        )

    summary_df = pd.DataFrame(summary_table)
    return summary_df

def charts(table):
    chart_configs = [
        ("Count", "#5c1360", "Antal"),
        ("AverageMagnitude", "#0c6565", "Genomsnittlig magnitud"),
        ("MaxMagnitude", "#20afcc", "Maximal magnitud"),
    ]

    charts_list = []
    for column, color, label in chart_configs:
        fig = px.bar(
            table,
            x="Day",
            y=column,
            color_discrete_sequence=[color],
            labels={"Day": "Datum", column: label}
        )
        chart = fig.to_html(full_html=False, include_plotlyjs="cdn")
        charts_list.append(chart)
    
    return charts_list

def timeline_statistics(url):
    table = earthquake_data(url)

    if type(table) == str:
        return table, "", "", "", ""

    html_2 = (
        summary_table(table)
        .to_html(classes="table table-striped", index=False)
    )
    chart_1, chart_2, chart_3 = charts(table) 

    html = (
        table.rename(columns={"Day": "Datum", "Count": "Antal", "AverageMagnitude": "Genomsnittlig magnitud", "MaxMagnitude": "Maximal magnitud"})
        .to_html(classes="table table-striped", index=False)
    )

    return html, html_2, chart_1, chart_2, chart_3