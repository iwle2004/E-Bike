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

# 結果を表示（座標と店名）
for element in data["elements"]:
    lat = element["lat"]
    lon = element["lon"]
    name = element["tags"].get("name", "(名前なし)")
    shop_type = element["tags"].get("shop", "(種別不明)")
    print(f"{name} ({shop_type}): {lat}, {lon}")