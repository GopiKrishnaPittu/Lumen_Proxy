import sqlite3
from datetime import datetime

DB_NAME = "lumen_proxy.db"

def init_db():
    """Initializes the SQLite database and creates the logs table."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    prompt TEXT,
                    score INTEGER,
                    decision TEXT
                )
            ''')
            conn.commit()
            print("[INFO] Database initialized successfully.")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")

def log_event(prompt, score, decision):
    """Saves a security event into the persistent log."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO security_logs (timestamp, prompt, score, decision)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, prompt, score, decision))
            conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to log event: {e}")
