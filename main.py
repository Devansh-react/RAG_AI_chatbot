from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from schema.Models import State
from graph.graph_builder import build_graph
from fastapi import FastAPI
from database.message_history import get_pg_history

app = FastAPI()


class User_input(BaseModel):
    session_id:str
    User_message: str

bot_graph = build_graph()
@app.post("/chat")
def chat(input: User_input):
    session_id = input.session_id
    last_message = input.User_message
    
    history_message = get_pg_history(session_id)
    
    history_message.add_user_message(last_message)
    
    
    message = []
    for m in history_message.messages:
        if m.type == "human":
            message.append(HumanMessage(content=m.content))
        else:
            message.append(AIMessage(content=m.content))
    
    
    state: State = State(
        session_ID=session_id,
        messages=message,
        messages_route=None,
        is_justified=None,
        retriver_doc=[],         # Now treated as list[str]
        retriver_score=0.0 ,
        web_result=None 
    )

    new_state = bot_graph.invoke(state)
    Airesponse = new_state["messages"][-1].content
    history_message.add_ai_message(Airesponse)
    return {"reply": Airesponse}


# if __name__ == "__main__":
#     test = User_input(session_id="agfa", User_message="HI")
#     print(chat(test))
