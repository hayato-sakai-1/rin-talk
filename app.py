import os
from flask import Flask, render_template, jsonify
from logic import generate_question

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_question")
def get_question_route():
    new_q = generate_question()
    return jsonify(question=new_q)