import argparse
import json
import os
import sys
import requests
import openrouteservice
from openrouteservice import convert
import folium

# ---- 1. Parse args ----
parser = argparse.ArgumentParser()
parser.add_argument("--tags", type=str, default="")
args = parser.parse_args()

tags_str = args.tags.strip()
print("Selected tags string:", tags_str)

if not tags_str:
    print("No tags given. Exiting.")
    sys.exit(0)

tags_list = []
for t in tags_str.split(","):
    if "=" in t:
        key, value = t.split("=", 1)
        tags_list.append((key.strip(), value.strip()))

if not tags_list:
    print("Tags format invalid. Exiting.")
    sys.exit(0)

key, value = tags_list[0]

# ---- 2. Query Overpass ----
search_box = "35.44880977985438, 135.35154309496215,35.498076744854764, 135.44095761784553"

query = f"""
[out:json];
node[{key}={value}]({search_box});
out body;
"""

try:
    response = requests.post("http://overpass-api.de/api/interpreter", data={"data": query}, timeout=30)
    response.raise_for_status()
except requests.RequestException as e:
    print("Overpass API error:", e)
    sys.exit(1)

data = response.json()
if "elements" not in data or not data["elements"]:
    print("No matching points found.")
    sys.exit(0)

points = [(el["lat"], el["lon"]) for el in data["elements"]]

# ---- 3. Routing ----
start_point = (35.46872450002604, 135.39500977773056)
end_point = (35.474763476187924, 135.38536802589823)

client = openrouteservice.Client(key="5b3ce3597851110001cf6248b9ea1dfdfdb7416eb962ef2ad2bd129e")

coords = [tuple(reversed(start_point))]
coords.extend([tuple(reversed(p)) for p in points])
coords.append(tuple(reversed(end_point)))

route_coords = []
for i in range(len(coords) - 1):
    try:
        routes = client.directions([coords[i], coords[i+1]], profile='foot-walking')
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)
        route_coords.extend(decoded['coordinates'])
    except Exception as e:
        print("Routing failed:", e)

# ---- 4. Generate map ----
mean_lat = sum(p[0] for p in points) / len(points)
mean_lon = sum(p[1] for p in points) / len(points)

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)

folium.Marker(start_point, tooltip="Start (Higashi Maizuru Station)", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(end_point, tooltip="Goal (Red Brick Park)", icon=folium.Icon(color="green")).add_to(m)

for i, p in enumerate(points):
    folium.Marker(p, tooltip=f"Point {i}: {p}").add_to(m)

if route_coords:
    route_latlon = [(lat, lon) for lon, lat in route_coords]
    folium.PolyLine(route_latlon, color="blue", weight=4, opacity=0.7).add_to(m)

# ---- 5. Save to public/maps ----
output_dir = os.path.join(os.path.dirname(__file__), "../public/maps")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "maizuru_full_tsp_route.html")
m.save(output_path)

print("Map generated at:", output_path)
