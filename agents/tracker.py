import sqlite3
from datetime import datetime

DB_PATH = "data/job_applications.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    conn = get_db_connection()
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

def log_application(company: str, title: str, status: str = "Applied", notes: str = ""):
    initialize_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, title, date_applied, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (company, title, datetime.now().isoformat(), status, notes))
    conn.commit()
    conn.close()
