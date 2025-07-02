import argparse
import json
import os
import requests
import sys
from itertools import permutations
import openrouteservice
from openrouteservice import convert
import folium

parser = argparse.ArgumentParser()
parser.add_argument("--tags", type=str, default="")
parser.add_argument("--output", type=str, required=True, help="出力するHTMLファイルパス")
parser.add_argument("--currentLocation", type=str, required=True)
args = parser.parse_args()

tags_str = args.tags.strip()
print("Selected tags string:", tags_str)

if not tags_str:
    print("タグが選択されていません。終了します。")
    sys.exit(0)

tags_list = []
for t in tags_str.split(","):
    if "=" in t:
        key, value = t.split("=", 1)
        tags_list.append((key.strip(), value.strip()))

print("Parsed tags:", tags_list)

if not tags_list:
    print("タグが正しく解析できません。終了します。")
    sys.exit(0)

key, value = tags_list[0]

search_box = "35.44880977985438, 135.35154309496215,35.498076744854764, 135.44095761784553"

query = f"""
[out:json];
node[{key}={value}]({search_box});
out body;
"""

url = "http://overpass-api.de/api/interpreter"

try:
    response = requests.post(url, data={"data": query}, timeout=30)
    response.raise_for_status()
except requests.RequestException as e:
    print("Overpass APIリクエスト失敗:", e)
    sys.exit(1)

data = response.json()

if "elements" not in data or len(data["elements"]) == 0:
    print("該当する地点が見つかりませんでした。")
    sys.exit(0)

points = []
for element in data["elements"]:
    lat = element["lat"]
    lon = element["lon"]
    name = element.get("tags", {}).get("name", "(名前なし)")
    print(f"{name}: {lat}, {lon}")
    points.append((lat, lon))

# JSON文字列 → dict → (lat, lon) タプル
start_dict = json.loads(args.currentLocation)
start_point = (start_dict["lat"], start_dict["lon"])
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
        print(f"ルート取得失敗: {coords[i]} → {coords[i+1]}:", e)

if not points:
    mean_lat, mean_lon = start_point
else:
    mean_lat = sum(p[0] for p in points) / len(points)
    mean_lon = sum(p[1] for p in points) / len(points)

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)

folium.Marker(start_point, tooltip="出発点（東舞鶴駅）", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(end_point, tooltip="目的地（赤レンガパーク）", icon=folium.Icon(color="green")).add_to(m)

for i, p in enumerate(points):
    folium.Marker(p, tooltip=f"地点{i}: {p}").add_to(m)

if route_coords:
    route_latlon = [(lat, lon) for lon, lat in route_coords]
    folium.PolyLine(route_latlon, color="blue", weight=4, opacity=0.7).add_to(m)

output_path = args.output
m.save(output_path)
print(f"地図作成完了: {output_path}")