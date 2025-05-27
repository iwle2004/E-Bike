import folium
import openrouteservice
from openrouteservice import convert
from itertools import permutations
import requests
import json
import sys

# 検索する地理範囲
Serch_Box = "35.44880977985438, 135.35154309496215,35.498076744854764, 135.44095761784553"  # 南緯,西経,北緯,東経

# 検索する店舗の検索に必要なタグ(amenityかshop)
Serch_key = "shop"

# 検索する店舗の種類
Serch_type = "=convenience"

# 名前で店舗を検索(検索しない場合は空白)
Serch_name = ""

# Overpass QL クエリ生成
if Serch_name:
    query = f"""
    [out:json];
    node[{Serch_key} {Serch_type}]["name"~"{Serch_name}"]({Serch_Box});
    out body;
    """
else:
    query = f"""
    [out:json];
    node[{Serch_key} {Serch_type}]({Serch_Box});
    out body;
    """

# Overpass APIエンドポイント
url = "http://overpass-api.de/api/interpreter"

# リクエスト送信
try:
    response = requests.post(url, data={"data": query}, timeout=30)
    print("📡 ステータスコード:", response.status_code)
    response.raise_for_status()
except requests.RequestException as e:
    print("❌ Overpass API リクエスト失敗:", e)
    sys.exit(1)

# JSON解析
try:
    data = response.json()
except json.JSONDecodeError:
    print("❌ JSON解析エラー。レスポンス内容:")
    print(response.text[:500])
    sys.exit(1)

# "elements" がなければ終了
if "elements" not in data:
    print("⚠️ 'elements' キーがレスポンスに存在しません")
    sys.exit(1)

# ポイント抽出
points = []
for i, element in enumerate(data["elements"]):
    lat = element["lat"]
    lon = element["lon"]
    name = element["tags"].get("name", "(名前なし)")
    shop_type = element["tags"].get("shop", "(種別不明)")
    print(f"{name} ({shop_type}): {lat}, {lon}")
    points.append((lat, lon))

if not points:
    print("⚠️ 該当する店舗が見つかりませんでした。")
    sys.exit(0)

# OpenRouteServiceクライアント（APIキーは有効なものに差し替えてください）
client = openrouteservice.Client(
    key="5b3ce3597851110001cf6248b9ea1dfdfdb7416eb962ef2ad2bd129e"
)

# ORS形式の座標 (lon, lat)
coords = [tuple(reversed(p)) for p in points]

# 距離行列を取得
try:
    matrix = client.distance_matrix(coords, profile='foot-walking', metrics=['distance'])["distances"]
except Exception as e:
    print("❌ 距離行列の取得に失敗:", e)
    sys.exit(1)

# 全探索TSP（巡回セールスマン）アルゴリズム
def brute_force_tsp(matrix):
    n = len(matrix)
    best_path = []
    min_dist = float('inf')
    for perm in permutations(range(1, n)):
        path = [0] + list(perm)
        dist = sum(matrix[path[i]][path[i+1]] for i in range(n-1))
        if dist < min_dist:
            min_dist = dist
            best_path = path
    return best_path

# 道順取得
def get_route_coordinates(path_indices):
    route_coords = []
    for i in range(len(path_indices) - 1):
        start = coords[path_indices[i]]
        end = coords[path_indices[i + 1]]
        try:
            route = client.directions(
                [start, end],
                profile='foot-walking',
                radiuses=[600, 600],
            )
            decoded = convert.decode_polyline(route["routes"][0]["geometry"])["coordinates"]
            route_coords.extend(decoded)
        except Exception as e:
            print(f"⚠️ ルート取得失敗: {start} → {end}")
            print(e)
    return [(lat, lon) for lon, lat in route_coords]

# 経路計算と描画
path = brute_force_tsp(matrix)
route_coords = get_route_coordinates(path)

# 地図の中心を平均座標に設定
mean_lat = sum(p[0] for p in points) / len(points)
mean_lon = sum(p[1] for p in points) / len(points)

# 地図描画
m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)
for i, p in enumerate(points):
    folium.Marker(p, tooltip=f"地点{i}: {p}").add_to(m)
folium.PolyLine(route_coords, color="green", weight=4, tooltip="最短徒歩ルート").add_to(m)
m.save("maizuru_full_tsp_route.html")

print("✅ 東舞鶴ナビ作成完了: maizuru_full_tsp_route.html")
