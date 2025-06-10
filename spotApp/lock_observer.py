import time
import RPi.GPIO as GPIO

#ソレノイドロックSWをつなぐピンのGPIO(BCM番号)
sw = 12

#ソレノイドロックSWにつなぐピンのGPIOをINMODE(プルアップ)に
GPIO.setmode(GPIO.BCM)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#スイッチの状態を監視する。
def observe_sw():
    sw_status = GPIO.input(sw)

    #0で施錠、1で開錠を示す。
    if sw_status == 0:
        print('施錠中')

    else:
        print('開錠中')

    time.sleep(1.0)
    GPIO.cleanup

while True:
    observe_sw()