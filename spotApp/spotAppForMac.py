import flet as ft
import datetime
import random as rnd
import os
import camera
import time
import serial
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

#------
#Firebase初期設定
#------
#Firebaseを初期化
cred = credentials.Certificate('meBike.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Web APIキー
api_key = os.environ.get('API_KEY')
 
# プロジェクトID
project_id = os.environ.get('PROJECT_ID')

#FirebaseのドキュメントIDを指定
city_ref = db.collection("token").document("nitMaizuruCollege")

#------
#画面出力
#------
def main(page: ft.Page):
    #------
    #ページ設定
    #------
    page.title = "ME-Bike GUI"
    page.window_max_width = 1920
    page.window_max_height = 1080
    page.window_minimizable =False
    page.window_maximizable = True
    page.window_resizable = True
    page.window_full_screen = True
    page.window_always_on_top = True
    page.window_skip_task_bar = True
    page.bgcolor=ft.colors.WHITE
    #フォント
    page.fonts={
        "BIZ UDPGothic": "BIZUDPGothic-Regular.ttf"
    }
    #AppBar(上部バナー)
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PEDAL_BIKE_SHARP),
        leading_width=80,
        title=ft.Text("ME-Bike Station (舞鶴高専ステーション)", font_family="BIZ UDPGothic"),
        center_title= False,
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    #------
    #現在時刻取得
    #------
    now = datetime.datetime.now()


    #------
    #画面表示
    #------
    def route_change(e):
        #ページのクリア
        page.views.clear()
        Solenoid = 18
        
        #トップページ
        page.views.append(
            ft.View(
                "/",
                [
                    page.appbar,
                    ft.Container(ft.Column([
                        ft.Row([
                            ft.Text(
                                "ME-Bike 舞鶴高専ステーション",
                                size=120,
                                color=ft.colors.BLACK,
                                selectable=False,
                                font_family="BIZ UDPGothic"
                            ),
                        ],alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            ft.Text(
                                "利用開始ボタンでスタート",
                                size=50,
                                color=ft.colors.BLACK,
                                selectable=False,
                                font_family="BIZ UDPGothic"
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            ft.Image(
                                src=f"ME-Bike.jpg",
                                width=500,
                                height=500,
                                fit=ft.ImageFit.CONTAIN
                            ),
                            ft.Image(
                                src=f"qr.png",
                                width=500,
                                height=500,
                                fit=ft.ImageFit.CONTAIN
                            )
                        ],spacing=20,alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            ft.Text(
                                '最近の利用: '+str(now),
                                size=40,
                                color=ft.colors.BLACK,
                                selectable=False,
                                font_family="BIZ UDPGothic"
                            )
                        ],alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Text(
                                    value="利用開始",
                                    size=60,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_01_token
                            )
                        ],alignment=ft.MainAxisAlignment.CENTER)
                    ],),
                    margin=10,
                    padding=10,
                    )
                ],
            )
        )
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Solenoid, GPIO.OUT)
        GPIO.output(Solenoid, False)

        #トークン入力画面
        if page.route == "/01_token":
            #トークンを生成
            random = rnd.randint(100000,999999)
            city_ref.update({"token_f": random})
            page.views.append(
                ft.View(
                    "/01_token",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_00_top,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Column([
                            ft.Column([
                                ft.Text(
                                    "トークンを入力",
                                    size=60,
                                    weight=ft.FontWeight.W_900,
                                    color=ft.colors.BLACK,
                                    selectable=False,
                                    font_family="BIZ UDPGothic"
                                ),
                                ft.Text(
                                    "Webアプリ上に以下の数字を入力してください。",
                                    size=50,
                                    weight=ft.FontWeight.W_900,
                                    color=ft.colors.BLACK,
                                    selectable=False,
                                    font_family="BIZ UDPGothic"
                                ),
                                ft.Text(
                                    "入力できたら次へ進む",
                                    size=50,
                                    weight=ft.FontWeight.W_900,
                                    color=ft.colors.BLACK,
                                    selectable=False,
                                    font_family="BIZ UDPGothic"
                                )
                            ],horizontal_alignment=ft.CrossAxisAlignment.START),
                            ft.Row([
                                ft.Image(
                                    src=f"qr.png",
                                    width=300,
                                    height=300,
                                    fit=ft.ImageFit.CONTAIN
                                )
                            ],alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([
                                ft.Text(
                                    random,
                                    size=120,
                                    weight=ft.FontWeight.W_900,
                                    color=ft.colors.BLACK,
                                    selectable=False,
                                    font_family="BIZ UDPGothic"
                                )
                            ],alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "次へ",
                                        size=60,
                                        font_family="BIZ UDPGothic"                                        
                                    ),
                                    on_click=open_02_tokenCheck
                                )
                            ],alignment=ft.MainAxisAlignment.CENTER)
                        ],alignment=ft.MainAxisAlignment.END)
                    ]
                )
            )

        if page.route == "/02_tokenCheck":
            page.views.append(
                ft.View(
                    "/02_tokenCheck",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_01_token,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "トークンを照合中...",
                                        size=100,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ProgressRing(
                                        width=75,
                                        height=75
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            alignment=ft.alignment.bottom_center,
                            width=1980,
                            height=960
                        )
                    ]
                )
            )
            tokenPath = ['token_f']
            inputPath = ['inputToken']
            token = city_ref.get(field_paths=tokenPath).to_dict()
            input = city_ref.get(field_paths=inputPath).to_dict()
            token_s = token["token_f"]
            input_s = input["inputToken"]
            if token_s == input_s:
                print("照合成功")
                open_04_face(e)
            elif token_s != input_s:
                print("照合失敗")
                open_03_tokenFaild(e)

        if page.route == "/03_tokenFaild":
            page.views.append(
                ft.View(
                    "/03_tokenFaild",
                    [
                        page.appbar,
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "照合失敗、再度照合してください。",
                                        size=100,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "戻る",
                                            size=50,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_01_token
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=1000
                        )
                    ]
                )
            )

        if page.route == "/04_face":
            page.views.append(
                ft.View(
                    "/04_face",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_01_token,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "顔を撮影します",
                                        size=60,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "準備ができたら撮影ボタンを押してカメラを見てください。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=f"cam.png",
                                        width=400,
                                        height=400,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "撮影",
                                            size=50,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_05_faceCheck
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=960
                        )
                    ]
                )
            )

        if page.route == "/05_faceCheck":
            page.views.append(
                ft.View(
                    "/05_faceCheck",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_04_face,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "顔を撮影中...",
                                        size=100,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ProgressRing(
                                        width=75,
                                        height=75
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            alignment=ft.alignment.bottom_center,
                            width=1980,
                            height=960
                        )
                    ]
                )
            )
            time.sleep(1)
            if camera.main():
                imNow=camera.now
                print("取得時: "+str(imNow))
                open_07_unLock(e)
            else:
                imNow=camera.now
                print("取得時: "+str(imNow))
                open_06_faceFaild(e)

        if page.route == "/06_faceFaild":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/06_faceFaild",
                    [
                        page.appbar,
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "顔を検出できません",
                                        size=85,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "再度撮影してください。",
                                        size=75,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=str(imNow)+".jpg",
                                        width=600,
                                        height=440,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "戻る",
                                            size=50,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_04_face
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=1000
                        )
                    ]
                )
            )

        if page.route == "/07_unLock":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/07_unLock",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_04_face,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "あなたの顔を記録しました。",
                                        size=60,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=str(imNow)+".jpg",
                                        width=600,
                                        height=440,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "自転車のロックを解除します。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "ロックを解除",
                                            size=50,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_08_unLockInfo
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=960
                        )
                    ]
                )
            )

        if page.route == "/08_unLockInfo":
            GPIO.output(Solenoid, False)
            #自転車貸出中
            city_ref.update({"keyState": True})
            page.views.clear()
            page.views.append(
                ft.View(
                    "/08_unLockInfo",
                    [
                        page.appbar,
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "利用開始",
                                        size=70,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "チェーンを外して利用を始めましょう。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "次へボタンを押して待機画面に移ります。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=f"unLockInfo.png",
                                        width=700,
                                        height=540,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "待機画面へ",
                                            size=50,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_09_sleep
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=1000
                        )
                    ]
                )
            )
            GPIO.output(Solenoid, True)
            print("ロックを解錠します")
            f = open('lockState.txt', 'w')
            f.write('1')
            f.close()
            time.sleep(0.2)
            GPIO.output(Solenoid, False)

        if page.route == "/09_sleep":
            page.views.append(
                ft.View(
                    "/09_sleep",
                    [
                        page.appbar,
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "ME-Bike 舞鶴高専ステーション",
                                        size=120,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "現在利用中",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=f"ME-Bike.jpg",
                                        width=500,
                                        height=500,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "返却は、返却ボタンをタップ。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "返却",
                                            size=60,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_10_back
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=1000
                        )
                    ]
                )
            )
            GPIO.output(Solenoid, False)

        if page.route == "/10_back":
            page.views.append(
                ft.View(
                    "/10_back",
                    [
                        page.appbar,
                        ft.Row(
                            [ft.ElevatedButton(
                                content=ft.Text(
                                    "back",
                                    size=40,
                                    font_family="BIZ UDPGothic"
                                ),
                                on_click=open_09_sleep,
                            )],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(
                                        "返却",
                                        size=100,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "自転車前輪をロックしてください。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Image(
                                        src=f"ME-Bike.jpg",
                                        width=500,
                                        height=500,
                                        fit=ft.ImageFit.CONTAIN
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Text(
                                        "終了ボタンを押すと、近くに自転車がないと警報が発動します。",
                                        size=50,
                                        weight=ft.FontWeight.W_900,
                                        color=ft.colors.BLACK,
                                        selectable=False,
                                        font_family="BIZ UDPGothic"
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "終了",
                                            size=60,
                                            font_family="BIZ UDPGothic"
                                        ),
                                        on_click=open_11_top
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                            width=1980,
                            height=920
                        )
                    ]
                )
            )
            city_ref.update({"keyState": False})#自転車貸出終了
        
        #ページ更新
        page.update()


    #------
    #画面遷移
    #------
    #現在のページを削除して前のページに戻る
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    #TOPページへ戻る
    def open_00_top(e):
        page.views.pop()
        top_view = page.views[0]
        page.go(top_view.route)

    #01_tokenへ移動
    def open_01_token(e):
        page.go("/01_token")
    
    #02_tokenCheckへ移動
    def open_02_tokenCheck(e):
        page.go("/02_tokenCheck")

    #03_tokenFaildへ移動
    def open_03_tokenFaild(e):
        page.go("/03_tokenFaild")

    #04_faceへ移動
    def open_04_face(e):
        page.go("/04_face")

    #05_faceCheckへ移動
    def open_05_faceCheck(e):
        page.go("/05_faceCheck")

    #06_faceFaildへ移動
    def open_06_faceFaild(e):
        page.go("/06_faceFaild")

    #07_unLockへ移動
    def open_07_unLock(e):
        page.go("/07_unLock")

    #08_unLockInfoへ移動
    def open_08_unLockInfo(e):
        page.go("/08_unLockInfo")

    #09_sleepへ移動
    def open_09_sleep(e):
        page.go("/09_sleep")

    #10_backへ移動
    def open_10_back(e):
        page.go("/10_back")

    #一連の後TOPページへ戻る
    def open_11_top(e):
        page.views.pop()
        top_view = page.views[0]
        f = open('lockState.txt', 'w')
        f.write('0')
        f.close()
        page.go(top_view.route)

    #------
    #イベントの登録
    #------
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    #------
    #起動時の処理
    #------
    page.go(page.route)

ft.app(target=main)