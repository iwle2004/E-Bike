import folium
import openrouteservice
from openrouteservice import convert
from itertools import permutations
import requests
import json

# 検索する地理範囲
Serch_Box = "35.46086527229766, 135.38547415225145,35.47810686320488, 135.4033106490184"  # 南緯,西経,北緯,東経

# 検索する店舗の検索に必要なタグ(amenityかshop)
Serch_key = "amenity"

# 検索する店舗の種類
Serch_type = "=cafe"

#名前で店舗を検索(検索しない場合は空白)
Serch_name = ""

# Overpass QL クエリ
if Serch_name:
    query = f"""
    [out:json];
    node[{Serch_key} {Serch_type}]["name" ~ {Serch_name}]({Serch_Box});
    out body;
    """
else:
    query = f"""
    [out:json];
    node[{Serch_key} {Serch_type}]({Serch_Box});
    out body;
    """

# APIエンドポイント
url = "http://overpass-api.de/api/interpreter"

# リクエスト送信
response = requests.post(url, data={"data": query})
data = response.json()
points = []
# 結果を表示（座標と店名）
i = 0
for element in data["elements"]:
    lat = element["lat"]
    lon = element["lon"]
    name = element["tags"].get("name", "(名前なし)")
    shop_type = element["tags"].get("shop", "(種別不明)")
    print(f"{name} ({shop_type}): {lat}, {lon}")
    points.append((lat,lon))
    i=i+1



# ORSクライアント（APIキーを有効なものに）
client = openrouteservice.Client(
    key="5b3ce3597851110001cf6248b9ea1dfdfdb7416eb962ef2ad2bd129e"
)
print(points)
# ORS用に (lon, lat) に変換
coords = [tuple(reversed(p)) for p in points]

# 距離行列を取得
matrix = client.distance_matrix(coords, profile='foot-walking', metrics=['distance'])["distances"]

# 全探索TSPで最短経路を求める

def brute_force_tsp(matrix):
    """
    Brute force algorithm for solving the TSP.
    """
    n = len(matrix)
    best_path = []
    min_dist = float('inf')
    # Iterate over all permutations of the path
    for perm in permutations(range(1, n)):
        path = [0] + list(perm)
        # Calculate the total distance of the path
        dist = sum(matrix[path[i]][path[i+1]] for i in range(n-1))
        # If the distance is less than the current minimum, update the minimum
        if dist < min_dist:
            min_dist = dist
            best_path = path
    # Return the best path
    return best_path


# 実際の道順（ナビ）を取得する
def get_route_coordinates(path_indices):
    route_coords = []
    for i in range(len(path_indices) - 1):
        start = coords[path_indices[i]]
        end = coords[path_indices[i + 1]]
        try:
            route = client.directions(
                [start, end],
                #profile='driving-car',
                profile='foot-walking',
                radiuses=[600, 600],  # 最大許容距離を広げてエラー回避
            )
            decoded = convert.decode_polyline(route["routes"][0]["geometry"])["coordinates"]
            route_coords.extend(decoded)
        except Exception as e:
            print(f"ルート取得失敗: {start} → {end}")
            print(e)
    # folium用に (lat, lon) に戻す
    return [(lat, lon) for lon, lat in route_coords]

# 最短ルート探索
path = brute_force_tsp(matrix)
route_coords = get_route_coordinates(path)

# 地図の中心位置を計算
mean_lat = sum(p[0] for p in points) / len(points)
mean_lon = sum(p[1] for p in points) / len(points)

# 地図描画
m = folium.Map(location=(mean_lat, mean_lon), zoom_start=15)
for i, p in enumerate(points):
    folium.Marker(p, tooltip=f"地点{i}: {p}").add_to(m)
folium.PolyLine(route_coords, color="green", weight=4, tooltip="最短徒歩ルート").add_to(m)
m.save("map.html")

print("✅ 東舞鶴ナビ作成完了: maizuru_full_tsp_route.html")
