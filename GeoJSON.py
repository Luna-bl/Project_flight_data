import pandas as pd
import json

df = pd.read_csv("flight_sample.csv")
coords = df[['lon', 'lat']].values.tolist()  # GeoJSON = [lon, lat]

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
