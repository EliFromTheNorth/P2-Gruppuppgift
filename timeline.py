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
    table["Day"] = pd.to_datetime(table["Day"]).dt.strftime('%d %b')
    return table

def summary_table(table):
    def summary_values(column):
        return ", ".join(str(e) for e in column)
    
    summary_rows = [
        {
            "name": "Flest jordbävningar per dag",
            "filtered_data": table[table["Count"] == table["Count"].max()],
            "column": "Count",
        },
        {
            "name": "Färst jordbävningar per dag",
            "filtered_data": table[table["Count"] == table["Count"].min()],
            "column": "Count",
        },
        {
            "name": "Kraftigaste jordbävningen",
            "filtered_data": table[
                table["MaxMagnitude"] == table["MaxMagnitude"].max()
            ],
            "column": "MaxMagnitude",
        },
        {
            "name": "Svagaste jordbävningen",
            "filtered_data": table[
                table["MaxMagnitude"] == table["MaxMagnitude"].min()
            ],
            "column": "MaxMagnitude",
        },
        {
            "name": "Högsta dagsgenomsnitt",
            "filtered_data": table[
                table["AverageMagnitude"] == table["AverageMagnitude"].max()
            ],
            "column": "AverageMagnitude",
        },
        {
            "name": "Lägsta dagsgenomsnitt",
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
                "Datum": summary_values(e["filtered_data"]["Day"].values),
                "Värde": str(int(e["filtered_data"][e["column"]].iloc[0]))
                if e["column"] == "Count"
                else str(e["filtered_data"][e["column"]].iloc[0]),
            }
        )

    summary_df = pd.DataFrame(summary_table)
    return summary_df

def charts(table):
    figure_1 = px.bar(
            table,
            x="Day",
            y="Count",
            color_discrete_sequence=["#5c1360"],
            labels={"Day": "Datum", "Count": "Antal"}
        )
    chart_1 = figure_1.to_html(full_html=False, include_plotlyjs="cdn")
    
    figure_2 = px.bar(
            table,
            x="Day",
            y="AverageMagnitude",
            color_discrete_sequence=["#0c6565"],                
            labels={"Day": "Datum", "AverageMagnitude": "Genomsnittlig magnitud"}
        )
    chart_2 = figure_2.to_html(full_html=False, include_plotlyjs="cdn")
    
    figure_3 = px.bar(
            table,
            x="Day",
            y="MaxMagnitude",
            color_discrete_sequence=["#20afcc"],
            labels={"Day": "Datum", "MaxMagnitude": "Maximal magnitud"}
        )
    chart_3 = figure_3.to_html(full_html=False, include_plotlyjs="cdn")
    return chart_1, chart_2, chart_3

def format_date(series):
    return pd.to_datetime(series).dt.strftime('%d %b')

def timeline_statistics(url):
    table = earthquake_data(url)
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