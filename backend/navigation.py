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
args = parser.parse_args()

tags_str = args.tags.strip()
print("Selected tags string:", tags_str)

if not tags_str:
    print("タグが選択されていません。終了します。")
    sys.exit(0)

# "key=value,key=value" 形式を確実にパース
tags_list = []
for t in tags_str.split(","):
    if "=" in t:
        key, value = t.split("=", 1)
        tags_list.append((key.strip(), value.strip()))

print("Parsed tags:", tags_list)

if not tags_list:
    print("タグが正しく解析できません。終了します。")
    sys.exit(0)

# 今は最初のタグだけ使う（複数対応は今後拡張可能）
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

# 東舞鶴駅を起点に設定
start_point = (35.46872450002604, 135.39500977773056)

# OpenRouteServiceクライアント初期化（APIキーをあなたのものに置き換えてください）
client = openrouteservice.Client(key="あなたのAPIキー")

# 経路計算用座標リスト（lon, latの順）
coords = [tuple(reversed(start_point))]
coords.extend([tuple(reversed(p)) for p in points])

route_coords = []

for i in range(len(coords) - 1):
    try:
        routes = client.directions([coords[i], coords[i+1]], profile='foot-walking')
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)
        route_coords.extend(decoded['coordinates'])
    except Exception as e:
        print(f"ルート取得失敗: {coords[i]} → {coords[i+1]}:", e)

# 地図中心の平均値
mean_lat = sum(p[0] for p in points) / len(points)
mean_lon = sum(p[1] for p in points) / len(points)

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)

# 出発点マーカー
folium.Marker(start_point, tooltip="出発点（東舞鶴駅）", icon=folium.Icon(color="red")).add_to(m)

# 目的地マーカー
for i, p in enumerate(points):
    folium.Marker(p, tooltip=f"地点{i}: {p}").add_to(m)

# ルート線を描画（lon,lat→lat,lonに変換）
if route_coords:
    route_latlon = [(lat, lon) for lon, lat in route_coords]
    folium.PolyLine(route_latlon, color="blue", weight=4, opacity=0.7).add_to(m)

# 保存先のパス（適宜変更してください）
m.save("backend/maizuru_full_tsp_route.html")

print("地図作成完了: backend/maizuru_full_tsp_route.html")
