from utilities.Vector_db import run_pdf_rag
from schema.Models import State
from langchain_core.messages import AIMessage


def Rag_tool(state: State) -> State:
    query = state["messages"][-1].content

    answer, docs = run_pdf_rag(state, query)

    print(len(docs))
    
    state["retriver_doc"] = docs

    # Append RAG answer
    state["messages"].append(AIMessage(content=answer))

    return state
