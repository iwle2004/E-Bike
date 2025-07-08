import argparse
import json
import os
import requests
import sys
import math
import random
import folium
from itertools import permutations
import openrouteservice
from openrouteservice import convert

# ------------------------- 引数解析 ------------------------- #
parser = argparse.ArgumentParser()
parser.add_argument("--tags", type=str, default="")
parser.add_argument("--output", type=str, required=True, help="出力するHTMLファイルパス")
parser.add_argument("--currentLocation", type=str, required=True)
parser.add_argument("--endLocation", type=str, required=True)
parser.add_argument("--random_route", action="store_true", help="ジャンル無視で目的地までのルートをランダムに曲げる")
args = parser.parse_args()

# ------------------------- 入力座標の解析 ------------------------- #
start_dict = json.loads(args.currentLocation)
start_point = (start_dict["lat"], start_dict["lon"])  # 現在地

end_dict = json.loads(args.endLocation)
end_point = (end_dict["lat"], end_dict["lon"])  # 目的地

Xs, Ys = start_point
Xe, Ye = end_point

# ------------------------- 地球距離計算 ------------------------- #
def distance(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球半径[m]
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

# ------------------------- 検索範囲設定 ------------------------- #
mid_x = (Xs + Xe) / 2
mid_y = (Ys + Ye) / 2
dist = distance(Xs, Ys, Xe, Ye)
lim_range = 4000  # 最大検索範囲半径 [m]
center_x, center_y = mid_x, mid_y
serch_range = lim_range

# ------------------------- タグ抽出 ------------------------- #
tags_str = args.tags.strip()
tags_list = []
if tags_str:
    for t in tags_str.split(","):
        if "=" in t:
            key, value = t.split("=", 1)
            tags_list.append((key.strip(), value.strip()))

# ------------------------- ジャンルによる地点検索 ------------------------- #
points = []
if tags_list and not args.random_route:
    key, value = tags_list[0]
    query = f"""
    [out:json];
    node[{key}="{value}"](around:{serch_range},{center_x},{center_y});
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
        for element in data.get("elements", []):
            lat = element["lat"]
            lon = element["lon"]
            points.append((lat, lon))
    except requests.RequestException as e:
        print("Overpass APIリクエスト失敗:", e)
        sys.exit(1)

# ------------------------- OpenRouteService APIキー ------------------------- #
# 🔒 適宜自分のAPIキーに差し替えてください
client = openrouteservice.Client(key="5b3ce3597851110001cf6248b9ea1dfdfdb7416eb962ef2ad2bd129e")

# ------------------------- ランダムな道上の経由地生成 ------------------------- #
def generate_random_waypoints_on_roads(start, end, count=2, radius=0.01):
    waypoints = []
    for _ in range(count):
        ratio = random.random()
        lat = start[0] + (end[0] - start[0]) * ratio + random.uniform(-radius, radius)
        lon = start[1] + (end[1] - start[1]) * ratio + random.uniform(-radius, radius)

        # 道路にスナップ（nearestを使用）
        try:
            nearest = client.nearest(coords=(lon, lat), profile='foot-walking')
            snapped_coord = nearest['coordinates']
            snapped_latlon = (snapped_coord[1], snapped_coord[0])
            waypoints.append(snapped_latlon)
        except Exception as e:
            print(f"スナップ失敗: ({lat}, {lon}) → {e}")
            waypoints.append((lat, lon))  # スナップ失敗時は元の位置を使う
    return waypoints

# ------------------------- 経由地点の決定 ------------------------- #
if args.random_route:
    selected_points = generate_random_waypoints_on_roads(start_point, end_point, count=3, radius=0.01)
else:
    selected_points = points

# ------------------------- ルート取得 ------------------------- #
coords = [tuple(reversed(start_point))]  # lon, lat
coords.extend([tuple(reversed(p)) for p in selected_points])
coords.append(tuple(reversed(end_point)))

route_coords = []
for i in range(len(coords) - 1):
    try:
        routes = client.directions([coords[i], coords[i + 1]], profile='foot-walking')
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)
        route_coords.extend(decoded['coordinates'])
    except Exception as e:
        print(f"ルート取得失敗: {coords[i]} → {coords[i + 1]}:", e)

# ------------------------- foliumマップ生成 ------------------------- #
if selected_points:
    mean_lat = sum(p[0] for p in selected_points) / len(selected_points)
    mean_lon = sum(p[1] for p in selected_points) / len(selected_points)
else:
    mean_lat, mean_lon = start_point

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)

# 出発・目的地マーカー
folium.Marker(start_point, tooltip="出発点", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(end_point, tooltip="目的地", icon=folium.Icon(color="green")).add_to(m)

# 経由地マーカー
for i, p in enumerate(selected_points):
    folium.Marker(p, tooltip=f"経由地{i+1}", icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)

# 経路描画（lon,lat→lat,lonに変換）
if route_coords:
    route_latlon = [(lat, lon) for lon, lat in route_coords]
    folium.PolyLine(route_latlon, color="blue", weight=4, opacity=0.7).add_to(m)

# 検索範囲の円
folium.Circle(
    location=(mid_x, mid_y),
    radius=serch_range,
    color="blue",
    opacity=0.5,
    fill=True,
    fill_color="blue",
    fill_opacity=0.1,
).add_to(m)

# ------------------------- 保存 ------------------------- #
m.save(args.output)
print(f"地図作成完了: {args.output}")
