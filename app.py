# Flaskを読み込む
from flask import Flask, render_template, jsonify
# 質問生成ロジックを読み込む
from logic import generate_question
import time

# Flaskアプリケーションを作成
app = Flask(__name__)

@app.route("/")
def index():
    """ 最初のページを表示するための関数 """
    # templatesフォルダの中のindex.htmlというファイルを画面として返す
    return render_template("index.html")

@app.route("/get_question")
def get_question():
    """ 新しい質問を生成して返すための関数 """
    new_q = generate_question()
    # 質問のテキストをJSON形式で返す
    return jsonify(question=new_q)

# このファイルが直接実行された場合に、開発用のWebサーバーを起動する
if __name__ == "__main__":
    app.run(debug=True)