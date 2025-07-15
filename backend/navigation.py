import argparse
import json
import requests
import sys
import random
import folium
from folium import Popup
import openrouteservice
from openrouteservice import convert

# ------------------------- 引数解析 ------------------------- #
parser = argparse.ArgumentParser()
parser.add_argument("--tags", type=str, default="", help="例: amenity=cafe")
parser.add_argument("--output", type=str, required=True, help="出力するHTMLファイルパス")
parser.add_argument("--currentLocation", type=str, required=True)
parser.add_argument("--endLocation", type=str, required=True)
parser.add_argument("--random_route", action="store_true", help="ルート上にランダム寄り道ピンを追加する")
args = parser.parse_args()

# ------------------------- 入力座標の解析 ------------------------- #
start_dict = json.loads(args.currentLocation)
start_point = (start_dict["lat"], start_dict["lon"])  # (lat, lon)

end_dict = json.loads(args.endLocation)
end_point = (end_dict["lat"], end_dict["lon"])  # (lat, lon)

start_lonlat = (start_point[1], start_point[0])
end_lonlat = (end_point[1], end_point[0])

# ------------------------- OpenRouteService API ------------------------- #
client = openrouteservice.Client(key="5b3ce3597851110001cf6248b9ea1dfdfdb7416eb962ef2ad2bd129e")
ORS_PROFILE = "cycling-regular"  # または "driving-car"

# ------------------------- タグパース ------------------------- #
tags_str = args.tags.strip()
tags_list = []
if tags_str:
    for t in tags_str.split(","):
        if "=" in t:
            key, value = t.split("=", 1)
            tags_list.append((key.strip(), value.strip()))

# ------------------------- ユーティリティ：ジッター＆スナップ ------------------------- #
def generate_waypoints_from_route(route_coords, count=3, jitter=0.0005):
    if len(route_coords) == 0:
        return []

    if len(route_coords) < count:
        sampled_points = random.choices(route_coords, k=count)
    else:
        sampled_points = random.sample(route_coords, count)

    def jitter_point(p):
        return (
            p[0] + random.uniform(-jitter, jitter),
            p[1] + random.uniform(-jitter, jitter)
        )

    def snap_to_road(point):
        lon, lat = point[1], point[0]
        try:
            nearest = client.nearest(coords=(lon, lat), profile=ORS_PROFILE)
            return (nearest["coordinates"][1], nearest["coordinates"][0])
        except:
            return point

    jittered = [jitter_point(p) for p in sampled_points]
    snapped = [snap_to_road(p) for p in jittered]
    return snapped

# ------------------------- ユーティリティ：ルート取得 ------------------------- #
def get_route_segments_with_waypoints(points):
    all_coords = []
    for i in range(len(points) - 1):
        try:
            res = client.directions([points[i], points[i + 1]], profile=ORS_PROFILE)
            geometry = res['routes'][0]['geometry']
            decoded = convert.decode_polyline(geometry)['coordinates']  # lon, lat
            all_coords.extend(decoded)
        except Exception as e:
            print(f"ルート取得失敗: {points[i]} → {points[i+1]}: {e}")
    return all_coords

# ------------------------- ① 一旦直行ルートを取得 ------------------------- #
try:
    base_route = client.directions([start_lonlat, end_lonlat], profile=ORS_PROFILE)
    base_geometry = base_route['routes'][0]['geometry']
    decoded_route = convert.decode_polyline(base_geometry)['coordinates']  # (lon, lat)
    base_route_latlon = [(lat, lon) for lon, lat in decoded_route]
except Exception as e:
    print("基礎ルートの取得に失敗しました:", e)
    sys.exit(1)

# ------------------------- ② 経由地決定（random_route または tags） ------------------------- #
# ------------------------- ② 経由地決定（random_route または tags） ------------------------- #
selected_points = []

if args.random_route:
    selected_points = generate_waypoints_from_route(base_route_latlon, count=3, jitter=0.0005)

elif tags_list:
    key, value = tags_list[0]
    center_lat = (start_point[0] + end_point[0]) / 2
    center_lon = (start_point[1] + end_point[1]) / 2
    radius = 3000  # meters

    query = f"""
    [out:json][timeout:25];
    node[{key}="{value}"](around:{radius},{center_lat},{center_lon});
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={"data": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
        points = []
        for el in data["elements"]:
            if "lat" in el and "lon" in el:
                name = el.get("tags", {}).get("name", "名前なし")
                points.append({"lat": el["lat"], "lon": el["lon"], "name": name})
        selected_points = points  # ⭐ 修正済：ランダム抽出せず全件表示
    except Exception as e:
        print("Overpassジャンル検索失敗:", e)

# 🔽 fallback：どちらにも該当しない場合、自動でランダム経由地を設定
if not args.random_route and not tags_list:
    print("ランダム・タグの指定がないため、ルート上に自動ピンを生成します。")
    selected_points = generate_waypoints_from_route(base_route_latlon, count=3, jitter=0.0005)
    args.random_route = True  # ←描画ロジックのために true にする


# ------------------------- ③ フルルート構築 ------------------------- #
full_points = [start_lonlat]
if args.random_route:
    full_points += [(p[1], p[0]) for p in selected_points]
else:
    full_points += [(p["lon"], p["lat"]) for p in selected_points]
full_points.append(end_lonlat)

final_route_coords = get_route_segments_with_waypoints(full_points)

# ------------------------- ④ 地図生成 ------------------------- #
if selected_points:
    if args.random_route:
        mean_lat = sum(p[0] for p in selected_points) / len(selected_points)
        mean_lon = sum(p[1] for p in selected_points) / len(selected_points)
    else:
        mean_lat = sum(p["lat"] for p in selected_points) / len(selected_points)
        mean_lon = sum(p["lon"] for p in selected_points) / len(selected_points)
else:
    mean_lat, mean_lon = start_point

m = folium.Map(location=(mean_lat, mean_lon), zoom_start=14)

# 出発・目的地マーカー
folium.Marker(start_point, tooltip="出発点", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(end_point, tooltip="目的地", icon=folium.Icon(color="green")).add_to(m)

# 経由地マーカー
# 経由地マーカー
if args.random_route:
    for i, p in enumerate(selected_points):
        folium.Marker(
            (p[0], p[1]),
            tooltip=f"経由地{i+1}",
            popup=f"経由地{i+1}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
elif tags_list:
    for i, p in enumerate(selected_points):
        popup = Popup(p["name"], max_width=300)
        folium.Marker(
            (p["lat"], p["lon"]),
            tooltip=f"経由地{i+1}",
            popup=popup,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)


# 寄り道経由地ありルートを青色で描画
route_latlon = [(lat, lon) for lon, lat in final_route_coords]
folium.PolyLine(route_latlon, color="blue", weight=4, opacity=0.7, tooltip="経由地ルート").add_to(m)

# 直行ルート（赤）を先に描画
folium.PolyLine(base_route_latlon, color="red", weight=3, opacity=0.8, tooltip="直行ルート").add_to(m)

# ------------------------- ⑤ 保存 ------------------------- #
m.save(args.output)
print(f"✅ 地図作成完了: {args.output}")
