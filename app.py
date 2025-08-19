import os
from flask import Flask, render_template, jsonify, request
# logicから、必要な関数だけを読み込むように修正
from logic import generate_question, get_user_data_from_db, save_keywords_to_db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# ★【新機能】設定ページ用のルートを追加
@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/get_question")
def get_question_route():
    new_q = generate_question()
    return jsonify(question=new_q)

# ★【新機能】キーワードを取得・保存するためのAPIルートを追加
@app.route("/api/keywords", methods=['GET', 'POST'])
def handle_keywords():
    if request.method == 'GET':
        user_data = get_user_data_from_db()
        return jsonify(keywords=user_data.get('user_keywords', []))
    
    elif request.method == 'POST':
        data = request.get_json()
        keywords = data.get('keywords', [])
        success, message = save_keywords_to_db(keywords)
        return jsonify(success=success, message=message)

# (Gunicornで起動するため、if __name__ == '__main__': は不要)