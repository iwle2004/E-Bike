import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()
 
# Web APIキー
api_key = os.environ.get('API_KEY')
 
# プロジェクトID
project_id = os.environ.get('PROJECT_ID')
 
# Firestoreコレクションのパス
collection_path = 'posts'
 
# Firestore REST APIのURL
url = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_path}?key={api_key}'

#flagが"true"のとき6桁のパスワードをランダムに生成
def password_generater():
    global password  #passwordをグローバル関数に

    a = [random.randint(0, 9),
         random.randint(0, 9),
         random.randint(0, 9),
         random.randint(0, 9),
         random.randint(0, 9),
         random.randint(0, 9),
         random.randint(0, 9)]
    password = str(a[0]) + str(a[1]) + str(a[2]) + str(a[3]) + str(a[4]) + str(a[5])
    print(password)
 
#配列の一番最後の要素を抜き出す。
def get_last_document_ids(strings):
    if not strings:
        return None
    return strings[-1]

#サーバからGETする
def server_get():
    global flag_value  #flag_valueをグローバル関数に
    global pass_value  #pass_valueをグローバル関数に
    # HTTP GETリクエストを送信
    response = requests.get(url)
 
    # レスポンスを表示
    print(response.status_code)

    #ドキュメントIDを取得
    if response.status_code == 200:
        documents = response.json().get('documents', [])
        document_ids = [doc['name'].split('/')[-1] for doc in documents]
        print("Document IDs:", document_ids)
        # 最後の文字列を取得
        document_id = get_last_document_ids(document_ids)
        print("ドキュメントID:", document_id)

    else:
        print("Error:", response.json())

    #ドキュメントIDを指定したURL
    last_url = f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_path}/{document_id}?key={api_key}'

    # HTTP GETリクエストを送信
    response1 = requests.get(last_url)
    print(last_url)

    data = response1.json()
 
    # レスポンスを表示
    print(response1.status_code)

    #サーバからデータを抜き出す。
    if response1.status_code == 200:
        id_value = data["fields"]["id"]["stringValue"]
        key_value = data["fields"]["key"]["stringValue"]
        pass_value = data["fields"]["pass"]["stringValue"]
        flag_value = data["fields"]["flag"]["stringValue"]
        print(f"id: {id_value}")
        print(f"key: {key_value}")
        print(f"pass: {pass_value}")
        print(f"flag: {flag_value}")

    else:
        print("Error:", response1.json())

#サーバから受け取った"pass"を生成したパスワードと照合する。
def password_matching():
    if password == pass_value:
        post = {
    "fields": {
     "id": {
         "stringValue": "spot1"
     },
     "key": {
         "stringValue": "true"
     }
    }
}
        requests.post(url, post)
        print(post.text)
    else:
        print("not match")


while True:
    server_get()
    if flag_value == "true":
        password_generater()

    #pass_valueが空でないとき
    if pass_value != '':
        password_matching()