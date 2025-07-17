from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from schema.Models import State
from graph.graph_builder import build_graph
from fastapi import FastAPI

app = FastAPI()


class User_input(BaseModel):
    User_message: str

bot_graph = build_graph()
@app.post("/chat")
def chat(input: User_input):
    last_message = input.User_message

    state: State = State(
        messages=[HumanMessage(content=last_message)],
        messages_route=None,
        is_justified=None,
        retriver_doc=[],         # Now treated as list[str]
        retriver_score=0.0 ,
        web_result=None 
    )

    new_state = bot_graph.invoke(state)
    Airesponse = new_state["messages"][-1].content
    return {"reply": Airesponse}


# if __name__ == "__main__":
#     test = User_input(User_message="tell me about RAG ")
#     print(chat(test))
