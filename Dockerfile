# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# 環境変数設定
ENV PORT=8080

# Flaskアプリの起動コマンド
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]