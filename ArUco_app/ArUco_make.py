import cv2
import numpy as np
import os

class ArUcoMarkerGenerator:
    def __init__(self):
        """
        ArUcoマーカー生成器の初期化
        """
        # ArUco辞書の設定（検出システムと同じ4x4_50を使用）
        # OpenCVのバージョンに応じて適切なAPIを使用
        try:
            # OpenCV 4.7.0以降の新しいAPI
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        except AttributeError:
            try:
                # OpenCV 4.6.x以前の古いAPI
                self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
            except AttributeError:
                # さらに古いバージョンの場合
                self.aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_4X4_50)
        
        # マーカー保存用のディレクトリ
        self.marker_dir = "aruco_markers"
        if not os.path.exists(self.marker_dir):
            os.makedirs(self.marker_dir)
    
    def generate_single_marker(self, marker_id, size=200, border_bits=1):
        """
        単一のArUcoマーカーを生成
        
        Args:
            marker_id (int): マーカーのID（0-49）
            size (int): マーカーのサイズ（ピクセル）
            border_bits (int): マーカーの境界線の幅
        
        Returns:
            numpy.ndarray: 生成されたマーカー画像
        """
        # マーカーを生成（OpenCVバージョンに対応）
        try:
            # 新しいAPI
            marker_image = cv2.aruco.generateImageMarker(self.aruco_dict, marker_id, size, borderBits=border_bits)
        except AttributeError:
            # 古いAPI
            marker_image = cv2.aruco.drawMarker(self.aruco_dict, marker_id, size, borderBits=border_bits)
        
        # ファイル名を作成
        filename = f"aruco_marker_{marker_id:02d}.png"
        filepath = os.path.join(self.marker_dir, filename)
        
        # 画像を保存
        cv2.imwrite(filepath, marker_image)
        print(f"マーカー ID {marker_id} を保存しました: {filepath}")
        
        return marker_image
    
    def generate_multiple_markers(self, marker_ids, size=200, border_bits=1):
        """
        複数のArUcoマーカーを生成
        
        Args:
            marker_ids (list): マーカーIDのリスト
            size (int): マーカーのサイズ（ピクセル）
            border_bits (int): マーカーの境界線の幅
        
        Returns:
            dict: 生成されたマーカー画像の辞書
        """
        markers = {}
        
        for marker_id in marker_ids:
            if 0 <= marker_id <= 49:  # DICT_4X4_50は0-49のIDを持つ
                marker_image = self.generate_single_marker(marker_id, size, border_bits)
                markers[marker_id] = marker_image
            else:
                print(f"警告: マーカーID {marker_id} は範囲外です（0-49が有効）")
        
        return markers
    
    def create_test_sheet(self, marker_ids, sheet_size=(1920, 1080), marker_size=200):
        """
        複数のマーカーを配置したテスト用シートを作成
        
        Args:
            marker_ids (list): 配置するマーカーIDのリスト
            sheet_size (tuple): シートのサイズ（幅, 高さ）
            marker_size (int): 各マーカーのサイズ（ピクセル）
        
        Returns:
            numpy.ndarray: テストシート画像
        """
        # 白い背景を作成
        sheet = np.ones((sheet_size[1], sheet_size[0]), dtype=np.uint8) * 255
        
        # マーカーを配置する位置を計算
        cols = sheet_size[0] // (marker_size + 100)  # マーカー間の余白を考慮
        rows = sheet_size[1] // (marker_size + 100)
        
        marker_count = 0
        for row in range(rows):
            for col in range(cols):
                if marker_count >= len(marker_ids):
                    break
                
                marker_id = marker_ids[marker_count]
                
                # マーカーを生成（OpenCVバージョンに対応）
                try:
                    # 新しいAPI
                    marker_image = cv2.aruco.generateImageMarker(self.aruco_dict, marker_id, marker_size)
                except AttributeError:
                    # 古いAPI
                    marker_image = cv2.aruco.drawMarker(self.aruco_dict, marker_id, marker_size)
                
                # 配置位置を計算
                x = col * (marker_size + 100) + 50
                y = row * (marker_size + 100) + 50
                
                # マーカーをシートに配置
                sheet[y:y+marker_size, x:x+marker_size] = marker_image
                
                # マーカーIDをテキストで表示
                cv2.putText(sheet, f"ID: {marker_id}", 
                           (x, y + marker_size + 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0, 2)
                
                marker_count += 1
            
            if marker_count >= len(marker_ids):
                break
        
        # テストシートを保存
        sheet_filename = f"test_sheet_{len(marker_ids)}markers.png"
        sheet_filepath = os.path.join(self.marker_dir, sheet_filename)
        cv2.imwrite(sheet_filepath, sheet)
        print(f"テストシートを保存しました: {sheet_filepath}")
        
        return sheet
    
    def generate_test_set(self, num_markers=5):
        """
        テスト用のマーカーセットを生成
        
        Args:
            num_markers (int): 生成するマーカーの数
        """
        print(f"=== ArUcoマーカー生成開始 ===")
        print(f"生成するマーカー数: {num_markers}")
        
        # テスト用のマーカーIDを選択（0から順番に）
        marker_ids = list(range(num_markers))
        
        # 個別マーカーを生成
        print("\n--- 個別マーカー生成 ---")
        self.generate_multiple_markers(marker_ids, size=300)
        
        # テストシートを生成
        print("\n--- テストシート生成 ---")
        self.create_test_sheet(marker_ids, sheet_size=(1920, 1080), marker_size=200)
        
        # 小さなテストシートも生成（印刷用）
        print("\n--- 印刷用テストシート生成 ---")
        self.create_test_sheet(marker_ids, sheet_size=(1024, 768), marker_size=150)
        
        print(f"\n=== 生成完了 ===")
        print(f"保存先ディレクトリ: {self.marker_dir}")
    
    def display_marker_info(self):
        """
        使用可能なマーカー情報を表示
        """
        print("=== ArUcoマーカー情報 ===")
        print(f"辞書タイプ: DICT_4X4_50")
        print(f"利用可能なマーカーID: 0-49")
        print(f"マーカーサイズ: 4x4ビット")
        print(f"推奨用途: テスト・プロトタイプ開発")

# 使用例とテスト関数
def main():
    generator = ArUcoMarkerGenerator()
    
    # マーカー情報を表示
    generator.display_marker_info()
    
    print("\n" + "="*50)
    print("ArUcoマーカー生成オプション:")
    print("1. 基本テストセット（5個のマーカー）")
    print("2. カスタムマーカー生成")
    print("3. 大量テストセット（10個のマーカー）")
    print("="*50)
    
    choice = input("選択してください (1-3): ").strip()
    
    if choice == "1":
        # 基本テストセット
        generator.generate_test_set(5)
        
    elif choice == "2":
        # カスタムマーカー生成
        try:
            ids_input = input("生成したいマーカーIDをカンマ区切りで入力 (例: 0,1,5,10): ")
            marker_ids = [int(x.strip()) for x in ids_input.split(",")]
            
            print(f"指定されたマーカーID: {marker_ids}")
            generator.generate_multiple_markers(marker_ids, size=300)
            generator.create_test_sheet(marker_ids)
            
        except ValueError:
            print("無効な入力です。数字をカンマ区切りで入力してください。")
            
    elif choice == "3":
        # 大量テストセット
        generator.generate_test_set(10)
        
    else:
        print("デフォルトで基本テストセットを生成します。")
        generator.generate_test_set(5)
    
    print("\n生成されたマーカーファイルを確認してテストに使用してください。")
    print("テストシートを印刷してカメラでテストすることも可能です。")

if __name__ == "__main__":
    main()