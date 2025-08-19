import json
import random
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# --- データベース接続設定 ---
try:
    apikey = os.environ.get('CLOUDANT_APIKEY')
    url = os.environ.get('CLOUDANT_URL')
    if not apikey or not url:
        raise ValueError("環境変数 CLOUDANT_APIKEY または CLOUDANT_URL が設定されていません。")
    
    authenticator = IAMAuthenticator(apikey)
    db_client = CloudantV1(authenticator=authenticator)
    db_client.set_service_url(url)
    print("データベースに接続しました。")
except Exception as e:
    print(f"データベース接続エラー: {e}")
    db_client = None

DB_NAME = "rintalk-user-data"

# --- 初期データの読み込み ---
def load_default_templates():
    # DockerfileのWORKDIR /app を基準にするため、これでOK
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f).get('question_templates', {})

# (以降のコードは、先日お渡ししたものから変更ありません)
def get_user_data_from_db():
    if not db_client:
        return {"user_keywords": [], "question_templates": load_default_templates()}
    
    try:
        db_client.put_database(db=DB_NAME).get_result()
        print(f"データベース '{DB_NAME}' を作成しました。")
    except Exception:
        pass

    try:
        response = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        response['question_templates'] = load_default_templates()
        return response
    except Exception:
        default_data = {"_id": "user1", "user_keywords": []}
        db_client.post_document(db=DB_NAME, document=default_data).get_result()
        default_data['question_templates'] = load_default_templates()
        return default_data

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

def save_keywords_to_db(keywords):
    if not db_client:
        return False, "データベースに接続されていません。"
    try:
        doc = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        doc['user_keywords'] = keywords
        db_client.post_document(db=DB_NAME, document=doc)
        return True, "保存しました。"
    except Exception as e:
        return False, f"保存に失敗しました: {e}"