from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import json
import time
import threading

from ArUco_check_only import download_firebase_images, ArUcoImageDetectionSystem
app = Flask(__name__)
CORS(app)

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")
        
        unique_filename = f"map_{int(time.time())}.html"
        output_filepath = os.path.join(base_dir, unique_filename)

        tags = request.json.get("tags", [])
        currentLocation = request.json.get("currentLocation")
        if isinstance(tags, str):
            tags = json.loads(tags)

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(tags)

        subprocess.run([
            "python", nav_path,
            "--tags", tag_str,
            "--output", output_filepath,
            "--currentLocation", json.dumps(currentLocation)
        ], check=True
        )

        return jsonify({"status": "success", "filename": unique_filename})

    except Exception as e:
        print("❌ ナビゲーション失敗:", e)
        return jsonify(status="error", message=str(e)), 500

@app.route("/get-map/<string:filename>")
def get_map(filename):
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400
    
    html_path = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(html_path):
        return "File not found", 404
        
    return send_file(html_path)
@app.route('/run-detection', methods=['POST'])
def run_detection():
    try:
        # Step 1: Download new images from Firebase
        download_firebase_images(local_folder="captured_photos", firebase_folder="uploads")
        
        # Step 2: Run ArUco detection
        detector = ArUcoImageDetectionSystem(
            target_aruco_num=2,
            image_folder="captured_photos"
        )
        result = detector.process_latest_image()

        # Create a boolean: True if detected_count == 2, else False
        is_target_met = (result.get("detected_count", 0) == 2)

        return jsonify({
            "status": "success",
            "is_target_met": is_target_met,  # <-- this boolean is sent to frontend
            "detected_count": result.get("detected_count"),
            "target_count": result.get("target_count"),
            "marker_ids": result.get("marker_ids"),
            "ArUco_check": result.get("ArUco_check")
        })
    except Exception as e:
        print("Error during detection:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)