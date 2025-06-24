import cv2
import numpy as np
from cv2 import aruco

# マーカーサイズと間隔
size = 150
offset = 100  # 広めの間隔
x_offset = y_offset = offset // 2

# マーカーの個数
num_markers = 2 #個数
grid_size = int(np.ceil(np.sqrt(num_markers)))

# ArUco辞書の取得
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 白背景画像の作成
grid_cols = num_markers  # 横に2個並べる
img_height = size + offset  # 最小限の高さ
img_width = grid_cols * (size + offset)

# マーカーの生成と配置
img = np.full((img_height, img_width), 255, dtype=np.uint8)
for marker_id in range(num_markers):
    ar_img = aruco.generateImageMarker(dictionary, marker_id, size)
    row = marker_id // grid_size
    col = marker_id % grid_size
    y_start = (img_height - size) // 2
    x_start = col * (size + offset) + x_offset
    img[y_start:y_start + ar_img.shape[0], x_start:x_start + ar_img.shape[1]] = ar_img

# 画像保存
cv2.imwrite("markers_0_to_5.png", img)

# 検出器の準備
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

# 画像読み込みとマーカー検出
input_file = "markers_0_to_5.png"
output_file = "markers_0_to_5_drawing.png"
input_img = cv2.imread(input_file)
corners, ids, rejectedCandidates = detector.detectMarkers(input_img)

# マーカー描画
ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)
cv2.imwrite(output_file, ar_image)

# IDの表示と判定変数の設定
print("Detected marker IDs:", ids)
marker_detected = 1 if ids is not None and len(ids) >= 2 else 0 #個数検知、2個以上で1,二個以下で0
print("Marker detection flag:", marker_detected)