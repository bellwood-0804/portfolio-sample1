# 1. ベースイメージを指定
FROM python:3.12-slim

# 2. 作業ディレクトリを作成
WORKDIR /app

# 3. Python パッケージをインストールする前に pip をアップグレード
RUN python -m pip install --upgrade pip

# 4. Flask をインストール
RUN pip install flask flask-jwt-extended
RUN pip install ortools
RUN pip install mysql-connector-python
# 5. アプリコードをコンテナにコピー（後で追加する）
COPY . /app


# 環境変数の設定（必要に応じて）
# ENV MYSQL_HOST=db
# ENV MYSQL_USER=user
# ENV MYSQL_PASSWORD=pass
# ENV MYSQL_DATABASE=shift_db


# 6. コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
