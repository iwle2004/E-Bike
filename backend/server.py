from flask import Flask, jsonify, send_file
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Reactからの通信を許可する

@app.route("/run-navigation", methods=["GET"])
def run_navigation():
    try:
        # server.py のディレクトリを基準に navigation.py のパスを作成
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nav_path = os.path.join(base_dir, "navigation.py")  # navigation.py の場所に合わせて修正

        # navigation.py を実行
        subprocess.run(["python", nav_path], check=True)
        return jsonify({"status": "success"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error"})

@app.route("/get-map", methods=["GET"])
def get_map():
    # HTMLファイルのパスも同様に指定（navigation.pyが生成する想定）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "maizuru_full_tsp_route.html")

    return send_file(html_path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
