import sqlite3, json

conn = sqlite3.connect("chat.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS chats
(user TEXT, chat_id TEXT, title TEXT, messages TEXT)""")

def save_chat(user, chat_id, messages):
    title = messages[0]["content"][:40]
    c.execute("REPLACE INTO chats VALUES (?,?,?,?)",
              (user, chat_id, title, json.dumps(messages)))
    conn.commit()

def load_chats(user):
    c.execute("SELECT chat_id,title FROM chats WHERE user=?", (user,))
    return dict(c.fetchall())

def load_chat(user, chat_id):
    c.execute("SELECT messages FROM chats WHERE user=? AND chat_id=?", (user,chat_id))
    row = c.fetchone()
    return json.loads(row[0]) if row else []

def delete_chat(user, chat_id):
    c.execute("DELETE FROM chats WHERE user=? AND chat_id=?", (user,chat_id))
    conn.commit()