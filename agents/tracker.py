import sqlite3
from datetime import datetime

DB_PATH = "applications.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            title TEXT,
            date_applied TEXT,
            status TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_application(company: str, title: str, status: str = "applied", notes: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (company, title, date_applied, status, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (company, title, datetime.utcnow().strftime("%Y-%m-%d"), status, notes))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    results = cursor.fetchall()
    conn.close()
    return results
