from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
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
        if isinstance(tags, str):
            tags = json.loads(tags)
        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        subprocess.run(["python", nav_path, "--tags", tag_str], check=True)

        return jsonify({"status": "success"})
    except Exception as e:
        print("Navigation failed:", e)
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    # Use port from environment or default to 5000
    port = int(os.environ.get("PORT", 5001))
    serve(app, host="0.0.0.0", port=port)
