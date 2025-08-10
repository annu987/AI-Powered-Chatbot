import sqlite3

def init_db():
    conn = sqlite3.connect("chatlogs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            bot_response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_chat(user_input, bot_response):
    conn = sqlite3.connect("chatlogs.db")
    c = conn.cursor()
    c.execute("INSERT INTO chats (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()
    conn.close()
