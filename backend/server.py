from flask import Flask, request, jsonify, send_from_directory  # ← send_file → send_from_directory に変更
from flask_cors import CORS
import subprocess
import os
import json
import time

app = Flask(__name__)
CORS(app)

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")

        # maps ディレクトリを指定（事前に作っておく！）
        maps_dir = os.path.join(base_dir, "maps")  # ← 追加
        os.makedirs(maps_dir, exist_ok=True)       # ← ディレクトリがなければ作る

        unique_filename = f"map_{int(time.time())}.html"
        output_filepath = os.path.join(maps_dir, unique_filename)  # ← maps に保存

        tags = request.json.get("tags", [])
        currentLocation = request.json.get("currentLocation")
        endLocation = request.json.get("endLocation")
        if isinstance(tags, str):
            tags = json.loads(tags)

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        random_route = request.json.get("random_route", False)

        args = [
            "python", nav_path,
            "--tags", tag_str,
            "--output", output_filepath,
            "--currentLocation", json.dumps(currentLocation),
            "--endLocation", json.dumps(endLocation),
        ]
        if random_route:
            args.append("--random_route")

        subprocess.run(args, check=True)

        return jsonify({"status": "success", "filename": unique_filename})

    except Exception as e:
        print("❌ ナビゲーション失敗:", e)
        return jsonify(status="error", message=str(e)), 500

@app.route("/get-map/<string:filename>")
def get_map(filename):
    # maps フォルダから安全にファイル提供
    maps_dir = os.path.join(os.path.dirname(__file__), "maps")  # ← maps ディレクトリに限定
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    file_path = os.path.join(maps_dir, filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_from_directory(maps_dir, filename)  # ← 安全に返却

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
