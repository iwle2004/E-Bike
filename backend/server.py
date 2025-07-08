from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import json
import uuid  # 変更点: timeの代わりにuuidをインポート
import sys

app = Flask(__name__)
CORS(app)

@app.route("/run-navigation", methods=["POST"])
def run_navigation():
    try:
        # --- 基本的なパス設定 ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")
        maps_dir = os.path.join(base_dir, "maps")
        
        # ディレクトリが既に存在していてもエラーにならないようにする
        os.makedirs(maps_dir, exist_ok=True) 

        # 変更点: uuidを使用して、衝突の心配がないユニークなファイル名を生成
        unique_filename = f"map_{uuid.uuid4()}.html"
        output_filepath = os.path.join(maps_dir, unique_filename)

        # --- リクエストデータの取得 ---
        data = request.get_json()
        if not data:
            return jsonify(status="error", message="リクエストデータがありません。"), 400

        tags = data.get("tags", [])
        currentLocation = data.get("currentLocation")
        endLocation = data.get("endLocation")
        random_route = data.get("random_route", False)
        # 変更点: fun_routeオプションを受け取る
        fun_route = data.get("fun_route", False)

        # --- 入力値チェック ---
        if currentLocation is None:
            return jsonify(status="error", message="現在地の情報がありません。"), 400
        
        # 変更点: 目的地が不要なモードでなければ、目的地を必須とする
        if not random_route and not fun_route and endLocation is None:
            return jsonify(status="error", message="目的地の情報がありません。"), 400

        # --- タグの処理 ---
        if isinstance(tags, str):
            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                return jsonify(status="error", message="タグの形式が不正です。"), 400

        if tags and isinstance(tags[0], dict):
            tag_str = ",".join(f"{t['key']}={t['value']}" for t in tags)
        else:
            tag_str = ",".join(map(str, tags))

        # --- navigation.py を実行する引数を構築 ---
        args = [
            sys.executable,
            nav_path,
            "--tags", tag_str,
            "--output", output_filepath,
            "--currentLocation", json.dumps(currentLocation),
        ]
        
        if endLocation:
            args.extend(["--endLocation", json.dumps(endLocation)])

        if random_route:
            args.append("--random_route")

        # 変更点: fun_routeがTrueなら引数を追加
        if fun_route:
            args.append("--fun_route")
        
        # --- 外部スクリプトの実行 ---
        # check=Trueで、スクリプトがエラー終了した場合に例外を発生させる
        subprocess.run(args, check=True, capture_output=True, text=True, encoding='utf-8')

        return jsonify({"status": "success", "filename": unique_filename})

    except subprocess.CalledProcessError as e:
        # navigation.py がエラーを返した場合の処理
        print(f"❌ navigation.py の実行に失敗: {e}")
        print(f"Stderr: {e.stderr}")
        # navigation.py が出力したエラーメッセージをフロントに返す
        return jsonify(status="error", message=f"ナビゲーションスクリプトでエラーが発生しました: {e.stderr}"), 500
    except Exception as e:
        # その他の予期せぬエラー
        print(f"❌ サーバー内部エラー: {e}")
        return jsonify(status="error", message=str(e)), 500

@app.route("/get-map/<string:filename>")
def get_map(filename):
    maps_dir = os.path.join(os.path.dirname(__file__), "maps")
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    return send_from_directory(maps_dir, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
