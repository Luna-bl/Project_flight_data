import pandas as pd
import json

#https://raw.githubusercontent.com/Luna-bl/Project_flight_data/refs/heads/master/flight_way.geojson?token=GHSAT0AAAAAADIZOC3DIUEDNZU6AVWREZSY2FEJC7A


df = pd.read_csv("flight_sample.csv")
coords = df[['lon', 'lat']].values.tolist()  #

geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString", # ligne, points relies entre eux 
                "coordinates": coords # coordonnees qui forment la ligne 
            }
        }
    ]
}


with open("flight_way.geojson", "w") as f:
    json.dump(geojson_data, f, indent=2)

print("Fichier GeoJSON created : flight_way.geojson")
