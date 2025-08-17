import os
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

if __name__ == "__main__":
    # Code Engineから、環境変数PORTで、使用すべきポート番号が渡される
    # もし、ローカルで動かす場合は、PORTが設定されていないので、代わりに8080番を使う
    port = int(os.getenv('PORT', 8080))
    # host='0.0.0.0'は、コンテナの外部からアクセスできるようにするために重要
    app.run(host='0.0.0.0', port=port)