import mysql.connector
import time
from werkzeug.security import generate_password_hash

# # MySQL接続（dbはdocker-composeのservice名）
# 初回でも通常接続でも必ず実行される関数
def get_conn():
    
    # _は変数不要のため　tryは接続をする関数、接続したらretrunを実行
    for _ in range(10): 
        try:
            return mysql.connector.connect(
                host="db",
                user="user",
                password="pass",
                database="shift_db"
            )
        except mysql.connector.Error:
            time.sleep(2)
    raise Exception("MySQL に接続できませんでした")


# 初回起動時にテーブル作成　名前登録削除データベース
def init_db():
    time.sleep(5)  # MySQL起動待ち
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) unique,
            password VARCHAR(255) NOT NULL,
            hourly_wage INT NOT NULL
        )
    """)
     
# 初回起動時にテーブル作成 勤怠情報確認
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stamping (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            start_stamping DATETIME,
            end_stamping DATETIME,
            overtime TIME,
            rest TIME,
            total TIME,
            log TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS adminuser (
            id INT AUTO_INCREMENT PRIMARY KEY,
            staff_id int NOT NULL,
            name VARCHAR(50) unique,
            password VARCHAR(255) NOT NULL,
            judge TINYINT(1) NOT NULL DEFAULT 1, 
            level TINYINT(2) NOT NULL DEFAULT 1,   
            FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE
        )
    """)

     # ① staff に admin があるか確認
    cur.execute("SELECT id FROM staff WHERE name = %s", ("admin",))
    row = cur.fetchone()

    if row is None:
        password = generate_password_hash("1234")
        cur.execute("""
        INSERT INTO staff (name, password, hourly_wage)
        VALUES (%s, %s, %s)
    """, ("admin", password, 3000))
        staff_id = cur.lastrowid
    else:
        staff_id = row[0]

# ② adminuser に admin があるか確認
    cur.execute("SELECT id FROM adminuser WHERE name = %s", ("admin",))
    admin_row = cur.fetchone()

    if admin_row is None:
    # ここで改めてパスワードを取得
      cur.execute("SELECT password FROM staff WHERE id = %s", (staff_id,))
      password = cur.fetchone()[0]

      cur.execute("""
        INSERT INTO adminuser (staff_id, name, password,judge,level)
        VALUES (%s, %s, %s,%s,%s)
    """, (staff_id, "admin", password,1,3))
      
    conn.commit()
    cur.close()
    conn.close()
