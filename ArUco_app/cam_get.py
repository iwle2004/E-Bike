import cv2

# カメラを開く
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

indexNo = 0
while True:
    # 画像をキャプチャする
    ret, frame = cap.read()

    # 画像を表示する
    cv2.imshow("Image", frame)

    # `q`キーを押すとループを終了する
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('c'):
        cv2.imwrite(f"image{indexNo:05d}.jpg", frame)
        indexNo = indexNo + 1
# カメラを閉じる
cap.release()
# すべてのウィンドウを閉じる
cv2.destroyAllWindows()