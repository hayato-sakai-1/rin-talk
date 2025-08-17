import json
import random
import os

# このスクリプト(logic.py)が存在するディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# data.jsonへの絶対パスを構築
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data.json')

def load_data():
    """ 同梱された初期データを、絶対パスで読み込む """
    # 変更点：絶対パスでファイルを開く
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