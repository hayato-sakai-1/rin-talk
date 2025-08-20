import json
import random
import os

def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_question():
    data = load_data()
    question_categories = list(data['question_templates'].keys())
    chosen_category_name = random.choice(question_categories)
    templates_list = data['question_templates'][chosen_category_name]
    template = random.choice(templates_list)
    
    # --- ここからが、改善されたロジックです ---
    if "{keyword}" in template:
        # ユーザーデータがない場合に備えて、汎用的なキーワードのリストを用意する
        generic_keywords = [
            "あなたの趣味",
            "あなたの好きなこと",
            "あなたの得意なこと",
            "あなたの仕事",
            "あなたの学生時代の思い出"
        ]
        # そのリストから、ランダムで一つを選ぶ
        keyword = random.choice(generic_keywords)
        # 選ばれたキーワードで、質問を完成させる
        return template.format(keyword=keyword)
    else:
        # キーワードを含まない質問は、そのまま返す
        return template