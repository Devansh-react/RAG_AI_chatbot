from langchain_community.chat_message_histories import PostgresChatMessageHistory
from dotenv import load_dotenv
import os
load_dotenv()

connection_string =  os.getenv("DATABASE_URL")

def get_pg_history(session_id: str):
    return PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=connection_string, # type: ignore
        table_name="chat_messages"
    )
