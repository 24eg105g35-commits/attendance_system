"""Creates the database/tables and default users. Run once: python init_db.py"""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import mysql.connector
from werkzeug.security import generate_password_hash

db_name = os.environ.get("DB_NAME", "attendance_db")
db_port = int(os.environ.get("DB_PORT", 3306))

try:
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "123456"),
        port=db_port,
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cur.execute(f"USE {db_name}")
except Exception:
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "123456"),
        database=db_name,
        port=db_port,
    )
    cur = conn.cursor()

with open("schema.sql") as f:
    for stmt in f.read().split(";"):
        cleaned = stmt.strip()
        if cleaned and not cleaned.upper().startswith("CREATE DATABASE") and not cleaned.upper().startswith("USE "):
            cur.execute(cleaned)

for user, pw, role in [("admin", "admin123", "admin"), ("faculty", "faculty123", "faculty")]:
    cur.execute(
        "INSERT IGNORE INTO users (username, password_hash, role) VALUES (%s,%s,%s)",
        (user, generate_password_hash(pw), role),
    )
conn.commit()
print("Database ready. Logins -> admin/admin123, faculty/faculty123 (change these!)")
