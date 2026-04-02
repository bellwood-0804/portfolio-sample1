from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies
from datetime import timedelta
from db import get_conn, init_db
from routes.index import index_bp
from routes.list import list_bp
from routes.register import register_bp
from routes.stamping import stamping_bp
from routes.adminlist import adminlist_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=100)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# ログインするための処理
app.register_blueprint(index_bp)

#ログイン後入るフォルダー
app.register_blueprint(list_bp)

# 人物を登録削除するためのルートに移動
app.register_blueprint(register_bp)

# 打刻時の時間をとうろくするもの
app.register_blueprint(stamping_bp)

# 管理者がすべての従業員の打刻情報を閲覧および変更
app.register_blueprint(adminlist_bp)

if __name__ == "__main__": 
    init_db()
    app.run(host="0.0.0.0",port=5000, debug=True)
