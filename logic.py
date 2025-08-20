import json
import random
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# --- データベース接続設定 ---
db_client = None
try:
    apikey = os.environ.get('CLOUDANT_APIKEY')
    url = os.environ.get('CLOUDANT_URL')
    
    if not apikey or not url:
        print("!!! 重大なエラー: 環境変数 CLOUDANT_APIKEY または CLOUDANT_URL が設定されていません。")
    else:
        authenticator = IAMAuthenticator(apikey)
        db_client = CloudantV1(authenticator=authenticator)
        db_client.set_service_url(url)
        print(">>> データベースへの接続準備が完了しました。")

except Exception as e:
    print(f"!!! 重大なエラー: データベース接続の初期化中に例外が発生しました: {e}")


# --- 初期データの読み込み ---
def load_default_templates():
    try:
        # DockerfileのWORKDIR /app を基準にするため、これでOK
        with open('data.json', 'r', encoding='utf-8') as f:
            print(">>> data.json の読み込みに成功しました。")
            return json.load(f).get('question_templates', {})
    except Exception as e:
        print(f"!!! 重大なエラー: data.json の読み込みに失敗しました: {e}")
        return {}

# --- データベースからユーザーデータを取得/作成 ---
def get_user_data_from_db():
    if not db_client:
        return {"user_keywords": [], "question_templates": load_default_templates()}
    
    DB_NAME = "rintalk-user-data"
    try:
        # データベースが存在しなければ作成
        db_client.put_database(db=DB_NAME).get_result()
        print(f"データベース '{DB_NAME}' を作成しました。")
    except Exception:
        pass # すでに存在する場合は何もしない

    try:
        # 'user1' という固定IDで、ユーザーデータを取得
        response = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        response['question_templates'] = load_default_templates()
        return response
    except Exception:
        # ドキュメントがなければ、デフォルトデータで作成
        default_data = {"_id": "user1", "user_keywords": []}
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
    
    DB_NAME = "rintalk-user-data"
    try:
        doc = db_client.get_document(db=DB_NAME, doc_id="user1").get_result()
        doc['user_keywords'] = keywords
        db_client.post_document(db=DB_NAME, document=doc)
        return True, "保存しました。"
    except Exception as e:
        return False, f"保存に失敗しました: {e}"