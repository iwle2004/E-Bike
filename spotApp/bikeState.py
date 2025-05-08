from pygame import mixer
import time
import nfc
import binascii

#------
#音楽再生
#------
def music_play(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play(loops=1)
    while mixer.music.get_busy():
        time.sleep(0.1)

#------
# 自転車の状態管理
#------
# 待ち受けの1サイクル秒
TIME_cycle = 1
# 待ち受けの反応インターバル秒
TIME_interval = 0.1

music_play("start.mp3")
print("bikeState.py is starting!")
while True:
    #自転車の利用状態を参照
    f = open('lockState.txt', 'r')
    data = f.read()
    f.close()

    #利用状態に応じて動作
    if data == '1':
        print("自転車利用中")
    else:
        print("自転車はスポットにあります")
        # 212F(FeliCa)で設定
        target_req_felica = nfc.clf.RemoteTarget("212F")
        # USBに接続されたNFCリーダに接続してインスタンス化
        clf = nfc.ContactlessFrontend('usb')
        #自転車のIdm
        idm = "01010312f41c442a"

        # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
        target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
        
        if not target_res is None:
            tag = nfc.tag.activate(clf, target_res)
            #IDmを取り出す
            Num = binascii.hexlify(tag.idm)

            #IDmの状況に応じて動作を変更
            if Num.decode() == idm:
                print("自転車は近くにあります。")
            else:
                print("自転車なし。警報発動")
                music_play("notBike.mp3")
        else:
            print("自転車なし。警報発動")
            music_play("notBike.mp3")

        clf.close()


