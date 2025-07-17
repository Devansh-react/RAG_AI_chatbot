from utilities.Vector_db import retriver_chain
from schema.Models import State
from langchain_core.messages import HumanMessage,AIMessage


def Rag_tool(state:State)->State:
    
    last_human = state["messages"][-1].content 
    
    if last_human is None:
        raise ValueError("No HumanMessage found in state.")
    
    query_input = {"input": last_human}
    response = retriver_chain.invoke(query_input)
    rag_answer = response.get("answer", "No answer found.")
    rag_score = response.get("score", 0)

    state["retriver_doc"] = rag_answer
    state["retriver_score"] = rag_score
    # print(f""" Retriver_doc = {state["retriver_doc"]} , Retriver_score = {state["retriver_score"]}
    # """)
    return state

    

      