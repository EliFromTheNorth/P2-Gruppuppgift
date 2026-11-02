import pandas as pd


def process_earthquakes(data):

    earthquake_list = []

    for earthquake in data["features"]:

        magnitude = earthquake["properties"]["mag"]
        place = earthquake["properties"]["place"]
        depth = earthquake["geometry"]["coordinates"][2]

        if magnitude is None or depth is None:
            continue

        earthquake_list.append({
            "Magnitude": magnitude,
            "Place": place,
            "Depth": depth
        })

    # Create a DataFrame
    df = pd.DataFrame(earthquake_list)

    # Create new columns
    df["Rounded magnitude"] = df["Magnitude"].round(2)
    df["Rounded depth"] = df["Depth"].round(2)

    df["Category"] = df["Magnitude"].apply(
        lambda x: "Major" if x >= 5.0 else "Minor"
    )

    # Group earthquakes by category and calculate values
    grouped_df = df.groupby("Category").agg(
        Count=("Magnitude", "count"),
        Average_magnitude=("Magnitude", "mean"),
        Highest_magnitude=("Magnitude", "max"),
        Average_depth=("Depth", "mean"),
        Greatest_depth=("Depth", "max")
    ).reset_index()

    # Round calculated values
    grouped_df["Average_magnitude"] = grouped_df["Average_magnitude"].round(2)
    grouped_df["Average_depth"] = grouped_df["Average_depth"].round(2)
    grouped_df["Greatest_depth"] = grouped_df["Greatest_depth"].round(2)

    return grouped_df