import pandas as pd
from datetime import UTC, datetime

def översätt_plats(plats):
    riktningar = {
        "north of the": "norr om",
        "south of the": "söder om",
        "east of the": "öster om",
        "west of the": "väster om",
        "northeast of the": "nordost om",
        "northwest of the": "nordväst om",
        "southeast of the": "sydost om",
        "southwest of the": "sydväst om",

        #USGS förkortningar
        " NNE of ": " nordost om ",
        " NE of ": " nordost om ",
        " ENE of ": " nordost om ",
        " E of ": " öster om ",
        " ESE of ": " sydost om ",
        " SE of ": " sydost om ",
        " SSE of ": " sydost om ",
        " S of ": " söder om ",
        " SSW of ": " sydväst om ",
        " SW of ": " sydväst om ",
        " WSW of ": " sydväst om ",
        " W of ": " väster om ",
        " WNW of ": " nordväst om ",
        " NW of ": " nordväst om ",
        " NNW of ": " nordväst om ",
        " N of ": " norr om ",
    }

    for engelska, svenska in riktningar.items():
        plats = plats.replace(engelska, svenska)

    return plats

def skapa_dataframe(data):
    """Skapar en DataFrame från JSON-data som innehåller information om jordskalv."""
    kolumner = ["place", "mag", "longitude", "latitude", "depth", "time"]
    rader = []

    features = (data or {}).get("features") or []

    for skalv in features:
        egenskaper = skalv.get("properties") or {}
        tid = egenskaper.get("time")
        if tid:
            tid = datetime.fromtimestamp(tid / 1000, tz=UTC).strftime("%Y-%m-%d %H:%M")
        geometri = skalv.get("geometry") or {}
        koordinater = geometri.get("coordinates") or []

        if len(koordinater) < 3:
            continue  # Hoppa över om det inte finns tillräckligt med koordinater

        rader.append(
            {
                "place": översätt_plats(egenskaper.get("place") or "Okänd plats"),
                "mag": egenskaper.get("mag"),
                "longitude": koordinater[0],
                "latitude": koordinater[1],
                "depth": koordinater[2],
                "time": tid,
            }
        )

    return pd.DataFrame(rader, columns=kolumner)
