import os
from flask import Flask, render_template, jsonify, request
from logic import generate_question, get_user_data_from_db, save_keywords_to_db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/get_question")
def get_question_route():
    new_q = generate_question()
    return jsonify(question=new_q)

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