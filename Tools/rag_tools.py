from utilities.Vector_db import run_pdf_rag
from schema.Models import State
from langchain_core.messages import HumanMessage,AIMessage


def Rag_tool(state:State)->State:
    query = state["messages"][-1].content  # User question
    answer = run_pdf_rag(state, query)
    print(f""" Retriver_Answer: {answer}""")
    state["retriver_doc"] = [answer]
    state["retriver_score"] = 1.0 if "No relevant" not in answer else 0.0
    # state["messages"].append(AIMessage(content=answer))
    return state
    

      