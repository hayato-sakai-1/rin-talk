import json
import random
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# このスクリプト(logic.py)が存在するディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# data.jsonへの絶対パスを構築
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data.json')

# --- データベース接続設定 ---
try:
    authenticator = IAMAuthenticator(os.environ.get('CLOUDANT_APIKEY'))
    db_client = CloudantV1(authenticator=authenticator)
    db_client.set_service_url(os.environ.get('CLOUDANT_URL'))
    print("データベースに接続しました。")
except Exception as e:
    print(f"データベース接続エラー: {e}")
    db_client = None

DB_NAME = "rintalk-user-data"

# --- 初期データの読み込み ---
def load_default_templates():
    with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f).get('question_templates', {})

# --- データベースからキーワードを取得 ---
def get_user_data_from_db():
    if not db_client:
        return {"user_keywords": [], "question_templates": load_default_templates()}
    
    try:
        # データベースが存在しなければ作成
        db_client.put_database(db=DB_NAME).get_result()
        print(f"データベース '{DB_NAME}' を作成しました。")
    except Exception:
        # すでに存在する場合は何もしない
        pass

    try:
        # 'user1' というIDで、ユーザーデータを取得
        response = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        # question_templatesは常に最新のものをファイルから読み込む
        response['question_templates'] = load_default_templates()
        return response
    except Exception:
        # ドキュメントがなければ、デフォルトデータで作成
        default_data = {
            "_id": "user1",
            "user_keywords": [],
        }
        db_client.post_document(db=DB_NAME, document=default_data).get_result()
        default_data['question_templates'] = load_default_templates()
        return default_data

# --- 質問生成ロジック ---
def generate_question():
    data = get_user_data_from_db()
    question_templates = data.get('question_templates', {})
    user_keywords = data.get('user_keywords', [])

    question_categories = list(question_templates.keys())
    if not question_categories:
        return "質問テンプレートが見つかりません。"

    chosen_category_name = random.choice(question_categories)
    templates_list = question_templates[chosen_category_name]
    template = random.choice(templates_list)
    
    if "{keyword}" in template:
        if user_keywords:
            keyword = random.choice(user_keywords)
            return template.format(keyword=keyword)
        else:
            return "キーワードが設定されていません。設定画面から登録してください。"
    else:
        return template

# --- データベースにキーワードを保存 ---
def save_keywords_to_db(keywords):
    if not db_client:
        return False, "データベースに接続されていません。"
    try:
        # まず現在のドキュメントを取得
        doc = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        # キーワードを更新
        doc['user_keywords'] = keywords
        # ドキュメントを更新
        db_client.post_document(db=DB_NAME, document=doc)
        return True, "保存しました。"
    except Exception as e:
        return False, f"保存に失敗しました: {e}"