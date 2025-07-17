from typing import Annotated , Optional,List
from typing_extensions import TypedDict, Dict , Literal
from langgraph.graph.message import add_messages



class State(TypedDict):
    session_ID : str
    messages: Annotated[List, add_messages]  
    messages_route: Optional[str]
    is_justified: Optional[Literal["yes", "no"]]
    retriver_doc: Optional[List[str]]  
    retriver_score: float
    web_result: Optional[str]