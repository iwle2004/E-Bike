import cv2
import numpy as np
from cv2 import aruco

# マーカーサイズと間隔
size = 150
offset = 100  # 広めの間隔
x_offset = y_offset = offset // 2

# マーカーの個数
num_markers = 2
grid_size = int(np.ceil(np.sqrt(num_markers)))

# ArUco辞書の取得
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 白背景画像の作成
grid_cols = num_markers  # 横に2個並べる
img_height = size + offset # 最小限の高さ
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
cv2.imwrite("markers_2.png",img)
