# 名前を登録　削除するための処理、管理者しか使えない

from flask import Blueprint,Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from db import get_conn, init_db

register_bp=Blueprint("register", __name__)


# 名前登録削除するためのページ
@register_bp.route("/register",methods=["GET"])
def auto():
     return render_template("register.html")

# データベースに接続
@register_bp.route("/database", methods=["POST"])
def add_name():    
    data = request.get_json()
    if not data:
        return jsonify({"message": "JSONが不正です"}), 400

    name = data.get("name")
    password = data.get("password")
    hourly_wage = data.get("hourly_wage")


    if hourly_wage is None:
        return jsonify({"message": "時給が未入力です"}), 400
    # tryを実行してできなかったらexcpetを実行
    try:
        #  jsonから送られてくるデータは文字列なのでintで囲う
         hourly_wage = int(hourly_wage)
        #  このifが実行されなかったらexceptに行くのか
         if hourly_wage <= 0:
           raise ValueError
    except ValueError:
        return jsonify({"message": "時給は正の整数で入力してください"}), 400

    

    # stripは空白を取り除いたもの、not name.strip()は空白を除いたときに空白の時
    if not name or not name.strip():
        return jsonify({"message": "名前が空です"}), 400
    if not password or not password.strip():
        return jsonify({"message": "パスワードが空です"}), 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        password = generate_password_hash(password)
        cur.execute("INSERT INTO staff (name,password,hourly_wage) VALUES (%s,%s,%s)", (name.strip(),password,hourly_wage))
        # cur.execute("INSERT INTO staff (name, body) VALUES (%s, %s)", (name.strip(), body.strip()))入れたい値が二つあるならこのようにする
        # 直前に INSERT した staff の id を取得,primarykeyを取得している
        staff_id = cur.lastrowid
        cur.execute("INSERT INTO adminuser (staff_id,name,password) VALUES (%s,%s,%s)", (staff_id,name.strip(),password))
#    名前やパスワードを登録した時にその人物でも入れるようにするため
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({"message": str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": f"{name} を登録しました"}), 201
# fは文字列を展開するもの　なければ　nameのままmessageとして登録される


#登録した情報の一覧を出すコード 
@register_bp.route("/database/list", methods=["GET"])
def list_names():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name,hourly_wage FROM staff ORDER BY id DESC")
    # sql の実行結果をすべて取得　fetchallによって
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # JSONで返す
    return jsonify([{"id": r[0], "name": r[1],"hourly_wage":r[2]} for r in rows])  




# 削除用のflask
@register_bp.route("/delete",methods=["POST"])
def delete_process():
    data=request.get_json()
    ids=data.get("ids")

    if not ids:
        return jsonify({"message": "チェックがついていません"}), 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        placeholders = ','.join(['%s'] * len(ids))
        sql = f"DELETE FROM staff WHERE id IN ({placeholders})"
        # executeの第一引数は実行するやつ　第二引数はステークホルダーに実際に代入する値
        cur.execute(sql, ids)
        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"message": "DBエラー"}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": f"{ids} を削除しました"}), 201
    

