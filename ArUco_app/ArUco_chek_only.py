import cv2
import numpy as np
import os
from datetime import datetime
import glob

class ArUcoImageDetectionSystem:
    def __init__(self, target_aruco_num=1, image_folder="images"):
        """
        ArUcoマーカー検出システムの初期化（画像ファイル処理用）
        
        Args:
            target_aruco_num (int): 検出したいArUcoマーカーの数
            image_folder (str): 処理対象の画像が格納されているフォルダパス
        """
        self.ArUco_num = target_aruco_num
        self.ArUco_check = 0
        self.image_folder = image_folder
        
        # ArUco辞書の設定（一般的な4x4_50を使用）
        # OpenCVのバージョンに応じて適切なAPIを使用
        try:
            # OpenCV 4.7.0以降の新しいAPI
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            self.aruco_params = cv2.aruco.DetectorParameters()
        except AttributeError:
            try:
                # OpenCV 4.6.x以前の古いAPI
                self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
                self.aruco_params = cv2.aruco.DetectorParameters_create()
            except AttributeError:
                # さらに古いバージョンの場合
                self.aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_4X4_50)
                self.aruco_params = cv2.aruco.DetectorParameters_create()
        
        # 結果保存用のディレクトリ
        self.result_dir = "detection_results"
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
    
    def get_image_files(self):
        """
        指定されたフォルダから画像ファイル（jpg, jpeg, png）を取得
        
        Returns:
            list: 画像ファイルのパスリスト
        """
        if not os.path.exists(self.image_folder):
            print(f"指定されたフォルダが存在しません: {self.image_folder}")
            return []
        
        # サポートする画像形式
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_files = []
        
        for extension in extensions:
            pattern = os.path.join(self.image_folder, extension)
            image_files.extend(glob.glob(pattern))
        
        image_files.sort()  # ファイル名順にソート
        return image_files
    
    def detect_aruco_markers(self, image_path):
        """
        指定された画像からArUcoマーカーを検出
        
        Args:
            image_path (str): 画像ファイルのパス
        
        Returns:
            tuple: (検出されたマーカー数, 検出結果の画像, マーカーID)
        """
        # 画像を読み込み
        image = cv2.imread(image_path)
        if image is None:
            print(f"画像を読み込めませんでした: {image_path}")
            return 0, None, None
        
        # グレースケールに変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ArUcoマーカーを検出（OpenCVバージョンに対応）
        try:
            # 新しいAPI
            detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
            corners, ids, rejected = detector.detectMarkers(gray)
        except AttributeError:
            # 古いAPI
            corners, ids, rejected = cv2.aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.aruco_params
            )
        
        detected_count = 0
        marker_ids = None
        
        if ids is not None:
            detected_count = len(ids)
            marker_ids = ids.flatten()
            
            # 検出されたマーカーを画像に描画（OpenCVバージョンに対応）
            try:
                # 新しいAPI
                cv2.aruco.drawDetectedMarkers(image, corners, ids)
            except:
                # 古いAPI（fallback）
                image = cv2.aruco.drawDetectedMarkers(image, corners, ids)
            
            print(f"検出されたArUcoマーカー数: {detected_count}")
            print(f"マーカーID: {marker_ids}")
        else:
            print("ArUcoマーカーは検出されませんでした")
        
        return detected_count, image, marker_ids
    
    def check_aruco_condition(self, detected_count):
        """
        検出されたArUcoマーカー数が設定値と一致するかチェック
        
        Args:
            detected_count (int): 検出されたマーカー数
        
        Returns:
            int: 条件を満たす場合1、そうでなければ0
        """
        if detected_count == self.ArUco_num:
            self.ArUco_check = 1
            print(f"✓ 条件を満たしました: 検出数 {detected_count} = 設定数 {self.ArUco_num}")
        else:
            self.ArUco_check = 0
            print(f"✗ 条件を満たしませんでした: 検出数 {detected_count} ≠ 設定数 {self.ArUco_num}")
        
        return self.ArUco_check
    
    def process_image(self, image_path):
        """
        単一の画像を処理してArUcoマーカーを検出
        
        Args:
            image_path (str): 処理する画像のパス
        
        Returns:
            dict: 処理結果の辞書
        """
        print(f"\n処理対象の画像: {os.path.basename(image_path)}")
        
        # ArUcoマーカーを検出
        detected_count, result_image, marker_ids = self.detect_aruco_markers(image_path)
        
        # 条件チェック
        aruco_check = self.check_aruco_condition(detected_count)
        
        # 結果画像を保存
        result_filename = None
        if result_image is not None:
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            result_filename = f"result_{name}{ext}"
            result_path = os.path.join(self.result_dir, result_filename)
            cv2.imwrite(result_path, result_image)
            print(f"結果画像を保存しました: {result_path}")
        
        return {
            "image_path": image_path,
            "ArUco_check": aruco_check,
            "detected_count": detected_count,
            "target_count": self.ArUco_num,
            "marker_ids": marker_ids.tolist() if marker_ids is not None else [],
            "result_image": result_filename
        }
    
    def process_all_images(self):
        """
        指定されたフォルダ内のすべての画像を処理
        
        Returns:
            dict: 全体の処理結果
        """
        print("=== ArUcoマーカー検出システム開始 ===")
        print(f"設定されたマーカー数: {self.ArUco_num}")
        print(f"処理対象フォルダ: {self.image_folder}")
        
        # 画像ファイルを取得
        image_files = self.get_image_files()
        
        if not image_files:
            print("処理対象の画像ファイルが見つかりませんでした")
            return {
                "total_images": 0,
                "matched_images": 0,
                "results": [],
                "error": "No image files found"
            }
        
        print(f"見つかった画像ファイル数: {len(image_files)}")
        
        # 各画像を処理
        all_results = []
        matched_count = 0
        
        for image_path in image_files:
            result = self.process_image(image_path)
            all_results.append(result)
            if result["ArUco_check"] == 1:
                matched_count += 1
        
        print(f"\n=== 処理完了 ===")
        print(f"処理した画像数: {len(image_files)}")
        print(f"条件を満たした画像数: {matched_count}")
        
        return {
            "total_images": len(image_files),
            "matched_images": matched_count,
            "results": all_results,
            "ArUco_check": 1 if matched_count > 0 else 0  # 1つでも条件を満たせばTrue
        }
    
    def process_specific_image(self, image_filename):
        """
        特定の画像ファイルを処理
        
        Args:
            image_filename (str): 処理したい画像のファイル名
        
        Returns:
            dict: 処理結果
        """
        image_path = os.path.join(self.image_folder, image_filename)
        
        if not os.path.exists(image_path):
            print(f"指定された画像ファイルが見つかりません: {image_path}")
            return {"ArUco_check": 0, "error": "Image file not found"}
        
        print("=== ArUcoマーカー検出システム開始 ===")
        print(f"設定されたマーカー数: {self.ArUco_num}")
        
        result = self.process_image(image_path)
        
        print("=== 処理完了 ===")
        print(f"最終結果 ArUco_check: {result['ArUco_check']}")
        
        return result

# ========== 設定項目 ==========
# 検索対象のディレクトリパス
IMAGE_FOLDER_PATH = "captured_photos"

# 検出したいArUcoマーカーの数
TARGET_ARUCO_COUNT = 2
# =============================

# 使用例
if __name__ == "__main__":
    # システムを初期化
    detector = ArUcoImageDetectionSystem(target_aruco_num=TARGET_ARUCO_COUNT, image_folder=IMAGE_FOLDER_PATH)
    
    # 全ての画像を処理
    result = detector.process_all_images()
    
    # 結果を表示
    print("\n=== 最終結果 ===")
    print(f"処理した画像数: {result.get('total_images', 0)}")
    print(f"条件を満たした画像数: {result.get('matched_images', 0)}")
    print(f"ArUco_check: {result.get('ArUco_check', 0)}")
    
    # WebアプリのフラグとしてArUco_checkを使用
    ArUco_check = result.get('ArUco_check', 0)
    if ArUco_check == 1:
        print("✓ WebアプリのフラグがTrueに設定されました")
    else:
        print("✗ WebアプリのフラグがFalseに設定されました")
    
    # 特定の画像のみを処理したい場合の例
    # specific_result = detector.process_specific_image("pic1.jpg")
    
    # 個別結果の詳細表示
    print("\n=== 個別結果詳細 ===")
    for i, res in enumerate(result.get('results', []), 1):
        print(f"{i}. {os.path.basename(res['image_path'])}: "
              f"検出数={res['detected_count']}, 条件={res['ArUco_check']}, "
              f"ID={res['marker_ids']}")

#to us
#ArUco_checkはint型です。ArUcoを2つ検知したらT,それ以外の個数のArUcoを検知したらFとなります。
#指定されたフォルダから画像ファイル（jpg, jpeg, png）を読み込み、ArUcoマーカーの検出を行います。