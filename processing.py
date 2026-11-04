import pandas as pd


def process_earthquakes(stats):

    earthquake_list = []
    # loopar igenom varje jordskalv i stats och hämtar magnitud och djup
    for earthquake in stats["features"]:
        magnitud = earthquake["properties"]["mag"]
        djup = earthquake["geometry"]["coordinates"][2]
        # lägger till magnitud och djup i en lista med dictionaries
        earthquake_list.append({
            "magnitud": magnitud,
            "djup": djup
        })

    df = pd.DataFrame(earthquake_list)

    # avrunda magnitud och djup till två decimaler
    df["Rounded magnitude"] = df["magnitud"].round(2)
    df["Rounded depth"] = df["djup"].round(2)


# kategorisera jordskalven baserat på magnitud till major eller minor med hjälp av lambda-funktion
    df["Kategori"] = df["magnitud"].apply(
        lambda x: "Major" if x >= 5.0 else "Minor"
    )

# skapar en ny DataFrame,beräknar average magnitud och djup
#samt räknar magnitud för major och minor
    grouped_df = (
        df.groupby("Kategori").agg(Antal=("magnitud", "count"),
        Genomsnittlig_magnitud=("magnitud", "mean"),
        Genomsnittligt_djup=("djup", "mean"))
        .reset_index()
    )
    # avrundar medelvärdena till två decimaler
    grouped_df["Genomsnittlig_magnitud"] = grouped_df["Genomsnittlig_magnitud"].round(2)
    grouped_df["Genomsnittligt_djup"] = grouped_df["Genomsnittligt_djup"].round(2)

    return grouped_df
