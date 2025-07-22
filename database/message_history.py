import sqlite3
class SQLiteChatMessageHistory:
    # initalise the db by its path 
    def __init__(self, session_id: str, db_path="chat_history.db"):
        self.session_id = session_id
        self.db_path = db_path
#  storeuser messages 
    def add_user_message(self, message: str):
        self._add_message("human", message)
#  store ai messages 
    def add_ai_message(self, message: str):
        self._add_message("ai", message)
#Basic add messages 
    def _add_message(self, sender, content):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_messages (session_id, sender, content) VALUES (?, ?, ?)",
            (self.session_id, sender, content)
        )
        conn.commit()
        conn.close()
#  retrieve all messages
    @property
    def messages(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT sender, content FROM chat_messages WHERE session_id = ? ORDER BY id ASC",
            (self.session_id,)
        )
        result = [{"type": "human" if row[0] == "human" else "ai", "content": row[1]} for row in cur.fetchall()]
        conn.close()
        return result

def get_sqlite_history(session_id: str):
    return SQLiteChatMessageHistory(session_id=session_id)
