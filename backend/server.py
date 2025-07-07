from flask import Flask, request, jsonify, send_file
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
        unique_filename = f"map_{int(time.time())}.html"
        output_filepath = os.path.join("/tmp", unique_filename)  # /tmp を使用

        tags = request.json.get("tags", [])
        currentLocation = request.json.get("currentLocation")
        endLocation = request.json.get("endLocation")

        if isinstance(tags, str):
            tags = json.loads(tags)

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        print("🎯 コマンド実行:")
        print("python", "navigation.py",
              "--tags", tag_str,
              "--output", output_filepath,
              "--currentLocation", json.dumps(currentLocation),
              "--endLocation", json.dumps(endLocation))

        result = subprocess.run([
            "python", "navigation.py",
            "--tags", tag_str,
            "--output", output_filepath,
            "--currentLocation", json.dumps(currentLocation),
            "--endLocation", json.dumps(endLocation)
        ], check=True)

        print("✅ 地図ファイル生成:", output_filepath)
        print("✅ 実在チェック:", os.path.exists(output_filepath))

        return jsonify({"status": "success", "filename": unique_filename})
    except Exception as e:
        print("❌ ナビゲーション失敗:", e)
        return jsonify(status="error", message=str(e)), 500

@app.route("/get-map/<string:filename>")
def get_map(filename):
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    html_path = os.path.join("/tmp", filename)

    print("📁 ファイル提供要求:", html_path)
    if not os.path.exists(html_path):
        print("❌ ファイル存在しない")
        return "File not found", 404

    return send_file(html_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
