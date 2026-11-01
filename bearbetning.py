import pandas as pd
from datetime import datetime

def skapa_dataframe(data):
    """Skapar en DataFrame från JSON-data som innehåller information om jordskalv."""
    kolumner = ["place", "mag", "longitude", "latitude", "depth", "time"]
    rader = []

    features = (data or {}).get("features") or []

    for skalv in features:
        egenskaper = skalv.get("properties") or {}
        tid = egenskaper.get("time")
        if tid:
            tid = datetime.utcfromtimestamp(tid / 1000).strftime("%Y-%m-%d %H:%M")
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
                "time": tid,
            }
        )

    return pd.DataFrame(rader, columns=kolumner)
