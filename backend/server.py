from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app, origins=["https://e-bike-dun.vercel.app"])

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")

        tags = request.json.get("tags", [])
        if isinstance(tags, str):
            tags = json.loads(tags)

        # tagsが ["key=value", ...] 形式のリストならそのまま、
        # もし {"key": ..., "value": ...} の辞書なら key=value形式に変換
        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        print("Received tags:", tags)
        print("Constructed tag string:", tag_str)

        # navigation.pyを引数付きで実行
        subprocess.run(["python", nav_path, "--tags", tag_str], check=True)

        return jsonify({"status": "success"})
    except Exception as e:
        print("Navigation failed:", e)
        return jsonify({"status": "error"}), 500

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))