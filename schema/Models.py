from typing import Annotated 
from typing_extensions import TypedDict, Dict , Literal
from langgraph.graph.message import add_messages



class State(TypedDict):
    messages: Annotated[list, add_messages]
    messages_route:str | None
    is_justified: Literal["yes","no"] |None
    retriver_doc:list[str] 
    retriver_score: float
    web_result : str | None