# ステップ1：ベースとなる、公式の厨房環境を指定する (Python 3.10の軽量版)
FROM python:3.10-slim

# ステップ2：厨房の中に、作業用の「/app」という場所を作る
WORKDIR /app

# ステップ3：まず、部品リストだけをコピーし、部品を仕入れる
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ステップ4：レシピブック全体（ソースコード）を、厨房にコピーする
COPY . .

# ステップ5：この厨房の、公式な起動コマンドを指定する
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]