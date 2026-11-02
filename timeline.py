from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import requests


def earthquake_data(url):
    try:
        response = requests.get(url, timeout=5)
        # response = requests.get(url, timeout=0.00000000005) #FEL: Kunde inte nå servern. Kontrollera din internetanslutning.
        # response = requests.get(url, timeout=(2.0, 0.0001))  #FEL: "Servern svarade inte i tid (Timeout)"

        response.raise_for_status()
    except requests.Timeout:
        return "Servern svarade inte i tid (Timeout)"
    except requests.HTTPError as e:
        return f"HTTP-fel! Felkod: {e.response.status_code}"
    except requests.ConnectionError:
        return "Kunde inte nå servern. Kontrollera din internetanslutning."
    except ValueError:
        return "Kunde inte tolka data från servern (ogiltig JSON)."

    data = response.json()

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