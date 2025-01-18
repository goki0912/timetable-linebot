# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# 開発用と本番用のコマンドを切り替え可能にする
CMD ["bash"]
