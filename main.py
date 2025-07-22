from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from schema.Models import State
from graph.graph_builder import build_graph
from fastapi import FastAPI
from database.message_history import get_sqlite_history
from typing import Optional
app = FastAPI()
from fastapi import UploadFile, File
import os 
from fastapi.middleware.cors import CORSMiddleware
from database.sql_lite import create_tables

bot_graph = build_graph()   


class User_input(BaseModel):
    session_id:str
    User_message: str   
    pdf_path: Optional[str] 
#  req python-multipart lib 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
create_tables()
@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...)):
    upload_dir = "uploaded_pdfs"
    os.makedirs(upload_dir, exist_ok=True)

    filename = file.filename
    if not filename or not isinstance(filename, str):
        raise ValueError("Uploaded file has no valid filename.")

    file_location = os.path.join(upload_dir, filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"pdf_path": file_location}


@app.post("/chat")
def chat(input: User_input):
    session_id = input.session_id
    last_message = input.User_message
    pdf_path = input.pdf_path
    
    history_message = get_sqlite_history(session_id)
    
    history_message.add_user_message(last_message)
    
    message = []
    
    for m in history_message.messages:
        if m["type"] == "human":
            message.append(HumanMessage(content=m["content"]))
        elif m["type"] == "ai":
            message.append(AIMessage(content=m["content"]))
            
    
    state: State = State(
        session_ID=session_id,
        messages=message,
        messages_route=None,
        is_justified=None,
        retriver_doc=[],         # Now treated as list[str]
        retriver_score=0.0 ,
        web_result=None, 
        pdf_path=pdf_path if pdf_path is not None else ""
    )

    new_state = bot_graph.invoke(state)
    Airesponse = new_state["messages"][-1].content
    history_message.add_ai_message(Airesponse)
    return {"reply": Airesponse}


# if __name__ == "__main__":
#     test = User_input(session_id="agfa", User_message="HI")
#     print(chat(test))
    