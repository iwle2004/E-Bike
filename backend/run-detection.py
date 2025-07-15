from flask import Flask, jsonify
from flask_cors import CORS
import threading

# Import your detection system and download helpers
from ArUco_check_only import download_firebase_images, ArUcoImageDetectionSystem

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
