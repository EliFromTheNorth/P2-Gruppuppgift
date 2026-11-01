import pandas as pd


def skapa_dataframe(data):
    """Skapar en DataFrame från JSON-data som innehåller information om jordskalv."""
    kolumner = ["place", "mag", "longitude", "latitude", "depth"]
    rader = []

    features = (data or {}).get("features") or []

    for skalv in features:
        egenskaper = skalv.get("properties") or {}
        geometri = skalv.get("geometry") or {}
        koordinater = geometri.get("coordinates") or []

        if len(koordinater) < 3:
            continue  # Hoppa över om det inte finns tillräckligt med koordinater

        rader.append(
            {
                "place": egenskaper.get("place") or "Okänd plats",
                "mag": egenskaper.get("mag"),
                "longitude": koordinater[0],
                "latitude": koordinater[1],
                "depth": koordinater[2],
            }
        )

    return pd.DataFrame(rader, columns=kolumner)
