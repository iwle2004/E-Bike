import cv2
import numpy as np
import os
from datetime import datetime

class ArUcoDetectionSystem:
    def __init__(self, target_aruco_num=1):
        """
        ArUcoマーカー検出システムの初期化
        
        Args:
            target_aruco_num (int): 検出したいArUcoマーカーの数
        """
        self.ArUco_num = target_aruco_num
        self.ArUco_check = 0
        
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
        
        # 写真保存用のディレクトリ
        self.photo_dir = "captured_photos"
        if not os.path.exists(self.photo_dir):
            os.makedirs(self.photo_dir)
    
    def capture_photo(self, camera_id=0):
        """
        カメラから写真を撮影し、連番で保存
        
        Args:
            camera_id (int): カメラのID（通常は0）
        
        Returns:
            str: 保存された写真のファイルパス
        """
        # Webカメラをキャプチャ
        cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        if not cap.isOpened():
            print("カメラが開けませんでした")
            return None
        
        print("スペースキーを押して写真を撮影、ESCキーで終了")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("フレームの取得に失敗しました")
                break
            
            cv2.imshow('Camera Preview', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # スペースキーで撮影
                # 既存の写真数を数えて連番を決定
                existing_photos = [f for f in os.listdir(self.photo_dir) if f.startswith('pic') and f.endswith('.jpg')]
                pic_num = len(existing_photos) + 1
                
                filename = f"pic{pic_num}.jpg"
                filepath = os.path.join(self.photo_dir, filename)
                
                cv2.imwrite(filepath, frame)
                print(f"写真を保存しました: {filepath}")
                
                cap.release()
                cv2.destroyAllWindows()
                return filepath
            
            elif key == 27:  # ESCキーで終了
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return None
    
    def detect_aruco_markers(self, image_path):
        """
        指定された画像からArUcoマーカーを検出
        
        Args:
            image_path (str): 画像ファイルのパス
        
        Returns:
            tuple: (検出されたマーカー数, 検出結果の画像)
        """
        # 画像を読み込み
        image = cv2.imread(image_path)
        if image is None:
            print(f"画像を読み込めませんでした: {image_path}")
            return 0, None
        
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
        if ids is not None:
            detected_count = len(ids)
            
            # 検出されたマーカーを画像に描画（OpenCVバージョンに対応）
            try:
                # 新しいAPI
                cv2.aruco.drawDetectedMarkers(image, corners, ids)
            except:
                # 古いAPI（fallback）
                image = cv2.aruco.drawDetectedMarkers(image, corners, ids)
            
            print(f"検出されたArUcoマーカー数: {detected_count}")
            print(f"マーカーID: {ids.flatten()}")
        else:
            print("ArUcoマーカーは検出されませんでした")
        
        return detected_count, image
    
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
    
    def process_latest_photo(self):
        """
        最新の撮影写真を処理してArUcoマーカーを検出
        
        Returns:
            dict: 処理結果の辞書
        """
        # 最新の写真を取得
        photos = [f for f in os.listdir(self.photo_dir) if f.startswith('pic') and f.endswith('.jpg')]
        if not photos:
            print("処理する写真がありません")
            return {"ArUco_check": 0, "error": "No photos found"}
        
        # 最新の写真を選択（番号順で最後）
        photos.sort(key=lambda x: int(x.replace('pic', '').replace('.jpg', '')))
        latest_photo = photos[-1]
        latest_photo_path = os.path.join(self.photo_dir, latest_photo)
        
        print(f"処理対象の写真: {latest_photo}")
        
        # ArUcoマーカーを検出
        detected_count, result_image = self.detect_aruco_markers(latest_photo_path)
        
        # 条件チェック
        aruco_check = self.check_aruco_condition(detected_count)
        
        # 結果画像を保存
        if result_image is not None:
            result_filename = f"result_{latest_photo}"
            result_path = os.path.join(self.photo_dir, result_filename)
            cv2.imwrite(result_path, result_image)
            print(f"結果画像を保存しました: {result_path}")
        
        return {
            "ArUco_check": aruco_check,
            "detected_count": detected_count,
            "target_count": self.ArUco_num,
            "processed_image": latest_photo,
            "result_image": result_filename if result_image is not None else None
        }
    
    def run_full_process(self, camera_id=0):
        """
        完全なプロセスを実行：撮影→検出→判定
        
        Args:
            camera_id (int): カメラID（通常は0）
        
        Returns:
            dict: 最終結果
        """
        print("=== ArUcoマーカー検出システム開始 ===")
        print(f"設定されたマーカー数: {self.ArUco_num}")
        
        # 写真撮影
        photo_path = self.capture_photo(camera_id)
        if photo_path is None:
            return {"ArUco_check": 0, "error": "Photo capture failed"}
        
        # 最新写真を処理
        result = self.process_latest_photo()
        
        print("=== 処理完了 ===")
        print(f"最終結果 ArUco_check: {result['ArUco_check']}")
        
        return result

# 使用例
if __name__ == "__main__":
    # システムを初期化（ArUcoマーカーを2個検出したい場合）
    detector = ArUcoDetectionSystem(target_aruco_num=2)
    
    # 完全なプロセスを実行
    result = detector.run_full_process()
    
    # 結果を表示
    print("\n=== 最終結果 ===")
    print(f"ArUco_check: {result.get('ArUco_check', 0)}")
    
    # WebアプリのフラグとしてArUco_checkを使用
    ArUco_check = result.get('ArUco_check', 0)
    if ArUco_check == 1:
        print("✓ WebアプリのフラグがTrueに設定されました")
    else:
        print("✗ WebアプリのフラグがFalseに設定されました")

#to us
#ArUco_checはint型です。ArUcoを2つ検知したらT,それ以外の個数のArUcoを検知したらFとなります。
#aruco_maerkers,captured_photos,二つありますが、captured,photosのみ実行で問題ありません。