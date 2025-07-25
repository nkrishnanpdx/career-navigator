import sqlite3

DB_PATH = "applications.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect_db()
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

def insert_application(company, title, date_applied, status, notes):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, title, date_applied, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (company, title, date_applied, status, notes))
    conn.commit()
    conn.close()

def query_all_applications():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()
    conn.close()
    return rows
