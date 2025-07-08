import firebase_admin
from firebase_admin import credentials, storage as fb_storage
import os
import cv2
import numpy as np
from datetime import datetime
import glob

# ========== Firebase Initialization ==========

cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your JSON key if different
firebase_admin.initialize_app(cred, {
    'storageBucket': 'e-bike-maizuru.firebasestorage.app'  # Replace with your Firebase Storage bucket
})

# ========== Firebase Image Download Helper ==========

def download_firebase_images(local_folder="captured_photos", firebase_folder="uploads"):
    bucket = fb_storage.bucket()
    blobs = bucket.list_blobs(prefix=firebase_folder + "/")
    downloaded_count = 0

    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    for blob in blobs:
        if blob.name.endswith("/"):
            continue  # Skip folders
        filename = os.path.basename(blob.name)
        local_path = os.path.join(local_folder, filename)

        if os.path.exists(local_path):
            print(f"Already downloaded: {filename}")
            continue

        print(f"Downloading: {filename}")
        blob.download_to_filename(local_path)
        downloaded_count += 1

    print(f"\n✅ Download complete. Total new files downloaded: {downloaded_count}")

# ========== ArUco Detection Class (your existing) ==========

class ArUcoImageDetectionSystem:
    def __init__(self, target_aruco_num=1, image_folder="images"):
        self.ArUco_num = target_aruco_num
        self.ArUco_check = 0
        self.image_folder = image_folder

        try:
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            self.aruco_params = cv2.aruco.DetectorParameters()
        except AttributeError:
            self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
            self.aruco_params = cv2.aruco.DetectorParameters_create()

        self.result_dir = "detection_results"
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def get_image_files(self):
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(self.image_folder, ext)))
        image_files.sort()
        return image_files

    def get_latest_image_file(self):
        image_files = self.get_image_files()
        if not image_files:
            return None
        latest_file = max(image_files, key=os.path.getmtime)
        return latest_file

    def detect_aruco_markers(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            return 0, None, None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        try:
            detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
            corners, ids, _ = detector.detectMarkers(gray)
        except AttributeError:
            corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        detected_count = 0
        marker_ids = None

        if ids is not None:
            detected_count = len(ids)
            marker_ids = ids.flatten()
            try:
                cv2.aruco.drawDetectedMarkers(image, corners, ids)
            except:
                image = cv2.aruco.drawDetectedMarkers(image, corners, ids)

            print(f"Detected {detected_count} ArUco markers: {marker_ids}")
        else:
            print("No ArUco markers detected.")

        return detected_count, image, marker_ids

    def check_aruco_condition(self, detected_count):
        if detected_count == self.ArUco_num:
            self.ArUco_check = 1
            print(f"✓ Matched: detected {detected_count} = target {self.ArUco_num}")
        else:
            self.ArUco_check = 0
            print(f"✗ Not matched: detected {detected_count} ≠ target {self.ArUco_num}")
        return self.ArUco_check

    def process_image(self, image_path):
        print(f"\nProcessing image: {os.path.basename(image_path)}")
        detected_count, result_image, marker_ids = self.detect_aruco_markers(image_path)
        aruco_check = self.check_aruco_condition(detected_count)

        result_filename = None
        if result_image is not None:
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            result_filename = f"result_{name}{ext}"
            result_path = os.path.join(self.result_dir, result_filename)
            cv2.imwrite(result_path, result_image)
            print(f"Saved result image: {result_path}")

        return {
            "image_path": image_path,
            "ArUco_check": aruco_check,
            "detected_count": detected_count,
            "target_count": self.ArUco_num,
            "marker_ids": marker_ids.tolist() if marker_ids is not None else [],
            "result_image": result_filename
        }

    def process_latest_image(self):
        latest_image = self.get_latest_image_file()
        if latest_image is None:
            print("No images found.")
            return
        result = self.process_image(latest_image)
        print(f"\nResult: {result}")
        return result

    def process_all_images(self):
        image_files = self.get_image_files()
        if not image_files:
            print("No images found.")
            return
        for image_path in image_files:
            self.process_image(image_path)

# ========== Configuration ==========

IMAGE_FOLDER_PATH = "captured_photos"   # where Firebase images are saved
TARGET_ARUCO_COUNT = 2                  # target number of ArUco markers
PROCESS_MODE = "latest"                 # "latest" or "all"

# ========== Main Execution ==========

if __name__ == "__main__":
    # Step 1: Download images from Firebase
    download_firebase_images(local_folder=IMAGE_FOLDER_PATH, firebase_folder="uploads")

    # Step 2: Initialize ArUco detection system
    detector = ArUcoImageDetectionSystem(
        target_aruco_num=TARGET_ARUCO_COUNT,
        image_folder=IMAGE_FOLDER_PATH
    )

    # Step 3: Run detection
    if PROCESS_MODE == "latest":
        detector.process_latest_image()
    else:
        detector.process_all_images()
