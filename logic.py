import json
import random
import os

# 変更点：単純に、プロジェクトのルートからのパスを指定する
DATA_FILE_PATH = 'data.json'

def load_data():
    """ 同梱された初期データを読み込む """
    with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_question():
    data = load_data()
    question_categories = list(data['question_templates'].keys())
    chosen_category_name = random.choice(question_categories)
    templates_list = data['question_templates'][chosen_category_name]
    template = random.choice(templates_list)
    
    if "{keyword}" in template:
        if data['user_keywords']:
            keyword = random.choice(data['user_keywords'])
            return template.format(keyword=keyword)
        else:
            # キーワードが空の場合の代替質問
            return "あなたの最近のマイブームは何ですか？"
    else:
        return template