import sqlite3
from datetime import datetime

DB_FILE = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(session_id, role, message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (session_id, role, message) VALUES (?, ?, ?)",
                   (session_id, role, message))
    conn.commit()
    conn.close()

def load_history(session_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, message FROM chat_history WHERE session_id = ? ORDER BY id", (session_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def clear_history(session_id=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if session_id:
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
    else:
        cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()

def list_sessions():
    """Return all distinct sessions with their latest message preview"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, MAX(timestamp), 
               (SELECT message FROM chat_history c2 WHERE c2.session_id = c1.session_id ORDER BY id DESC LIMIT 1)
        FROM chat_history c1
        GROUP BY session_id
        ORDER BY MAX(timestamp) DESC
    """)
    sessions = cursor.fetchall()
    conn.close()
    return sessions
