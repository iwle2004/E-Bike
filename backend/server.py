from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app)

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")

        tags = request.json.get("tags", [])
        locations = request.json.get("locations")
        print("受け取った locations:", locations)

        if isinstance(tags, str):
            tags = json.loads(tags)

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        print("📌 Received tags:", tag_str)
        print("📌 Received locations:", locations)

        subprocess.run([
            "python", nav_path,
            "--tags", tag_str,
            "--locations", json.dumps(locations)
        ], check=True)

        return jsonify({"status": "success"})
    except Exception as e:
        #print("❌ ナビゲーション失敗:", e)
        return jsonify({"status": "error", "message": str(e)})


@app.route("/get-map", methods=["GET"])
def get_map():
    html_path = os.path.join(os.path.dirname(__file__), "maizuru_full_tsp_route.html")
    return send_file(html_path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    