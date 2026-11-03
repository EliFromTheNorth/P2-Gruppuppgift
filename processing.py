
import pandas as pd


def process_earthquakes(stats):

    earthquake_list = []

    for earthquake in stats["features"]:
        magnitude = earthquake["properties"]["mag"]
        depth = earthquake["geometry"]["coordinates"][2]

        earthquake_list.append({
            "Magnitude": magnitude,
            "Depth": depth
        })

    df = pd.DataFrame(earthquake_list)

  
    df["Rounded magnitude"] = df["Magnitude"].round(2)
    df["Rounded depth"] = df["Depth"].round(2)

   
    df["Category"] = df["Magnitude"].apply(
        lambda x: "Major" if x >= 5.0 else "Minor"
    )

   
    grouped_df = (
        df.groupby("Category").agg(Count=("Magnitude", "count"),Average_magnitude=("Magnitude", "mean"),
        Average_depth=("Depth", "mean"))
        .reset_index()
    )

    return grouped_df
