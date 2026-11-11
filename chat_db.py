import sqlite3
from datetime import datetime

# connect to sqlite database 
def get_connection():

    conn= sqlite3.connect("chat_history.db")

    return conn


def create_tables():
    conn=get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
    """)
# store individual messages 

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                role TEXT,
                content TEXT,
                sources TEXT,
                created_at TEXT,
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
            )
        """)
    conn.commit()
    conn.close()
def create_chat(chat_id,tittle):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO chats
        (chat_id, title, created_at)
        VALUES (?, ?, ?)
    """,(
        chat_id,tittle,datetime.now().isoformat()
))
    