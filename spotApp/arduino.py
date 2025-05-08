import serial
import time

# シリアルポートの設定（ポート名は環境によって異なる）
#ser = serial.Serial('COM3', 9600) # Windowsの場合
# ser = serial.Serial('/dev/ttyACM0', 9600) # Linuxの場合
ser = serial.Serial('/dev/tty.usbmodem1201', 9600) # macOSの場合

time.sleep(2) # Arduinoとの接続が安定するまで待機

# LEDを点灯
ser.write(b'1')

time.sleep(10) # 10秒間点灯

# LEDを消灯
ser.write(b'0')

ser.close() # シリアルポートを閉じる


