from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import json
import uuid
import sys

from ArUco_check_only import download_firebase_images, ArUcoImageDetectionSystem

app = Flask(__name__)
CORS(app)

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")
        maps_dir = os.path.join(base_dir, "maps")
        os.makedirs(maps_dir, exist_ok=True)

        unique_filename = f"map_{uuid.uuid4()}.html"
        output_filepath = os.path.join(maps_dir, unique_filename)

        data = request.get_json()
        if not data:
            return jsonify(status="error", message="リクエストデータがありません。"), 400

        tags = data.get("tags", [])
        currentLocation = data.get("currentLocation")
        endLocation = data.get("endLocation")
        random_route = data.get("random_route", False)
        fun_route = data.get("fun_route", False)

        if currentLocation is None:
            return jsonify(status="error", message="現在地の情報がありません。"), 400

        if not random_route and not fun_route and endLocation is None:
            return jsonify(status="error", message="目的地の情報がありません。"), 400

        if isinstance(tags, str):
            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                return jsonify(status="error", message="タグの形式が不正です。"), 400

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(map(str, tags))

        args = [
            sys.executable,
            nav_path,
            "--tags", tag_str,
            "--output", output_filepath,
            "--currentLocation", json.dumps(currentLocation),
        ]

        if endLocation:
            args.extend(["--endLocation", json.dumps(endLocation)])
        if random_route:
            args.append("--random_route")
        if fun_route:
            args.append("--fun_route")

        subprocess.run(args, check=True, capture_output=True, text=True, encoding='utf-8')

        return jsonify({"status": "success", "filename": unique_filename})

    except subprocess.CalledProcessError as e:
        print(f"❌ navigation.py の実行に失敗: {e}")
        print(f"Stderr: {e.stderr}")
        return jsonify(status="error", message=f"ナビゲーションスクリプトでエラーが発生しました: {e.stderr}"), 500

    except Exception as e:
        print(f"❌ サーバー内部エラー: {e}")
        return jsonify(status="error", message=str(e)), 500


@app.route("/get-map/<string:filename>")
def get_map(filename):
    maps_dir = os.path.join(os.path.dirname(__file__), "maps")
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    file_path = os.path.join(maps_dir, filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_from_directory(maps_dir, filename)


@app.route('/run-detection', methods=['POST'])
def run_detection():
    try:
        # Step 1: Download images from Firebase
        download_firebase_images(local_folder="captured_photos", firebase_folder="uploads")

        # Step 2: Run ArUco detection
        detector = ArUcoImageDetectionSystem(
            target_aruco_num=2,
            image_folder="captured_photos"
        )
        result = detector.process_latest_image()

        # Step 3: Result judgment
        is_target_met = (result.get("detected_count", 0) == 2)

        return jsonify({
            "status": "success",
            "is_target_met": is_target_met,
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
    app.run(host="0.0.0.0", port=port, debug=True)
