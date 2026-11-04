
import pandas as pd


def process_earthquakes(stats):

    earthquake_list = []
    # loopar igenom varje jordskalv i stats och hämtar magnitud och djup
    for earthquake in stats["features"]:
        magnitude = earthquake["properties"]["mag"]
        depth = earthquake["geometry"]["coordinates"][2]
        # lägger till magnitud och djup i en lista med dictionaries
        earthquake_list.append({
            "Magnitude": magnitude,
            "Depth": depth
        })

    df = pd.DataFrame(earthquake_list)

    # avrunda magnitud och djup till två decimaler
    df["Rounded magnitude"] = df["Magnitude"].round(2)
    df["Rounded depth"] = df["Depth"].round(2)


# kategorisera jordskalven baserat på magnitud till major eller minor med hjälp av lambda-funktion
    df["Category"] = df["Magnitude"].apply(
        lambda x: "Major" if x >= 5.0 else "Minor"
    )

# skapar en ny DataFrame,beräknar average magnitud och djup
#samt räknar magnitud för major och minor
    grouped_df = (
        df.groupby("Category").agg(Count=("Magnitude", "count"),
        Average_magnitude=("Magnitude", "mean"),
        Average_depth=("Depth", "mean"))
        .reset_index()
    )
    # avrundar medelvärdena till två decimaler
    grouped_df["Average_magnitude"] = grouped_df["Average_magnitude"].round(2)
    grouped_df["Average_depth"] = grouped_df["Average_depth"].round(2)

    return grouped_df
