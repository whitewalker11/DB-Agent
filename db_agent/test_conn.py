# test_connection.py

import psycopg2
from config import DB_CONFIG

def test_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("✅ Connected to the database.")
        print("PostgreSQL version:", db_version[0])
        conn.close()
    except Exception as e:
        print("❌ Failed to connect to the database.")
        print("Error:", e)

if __name__ == "__main__":
    test_db_connection()
