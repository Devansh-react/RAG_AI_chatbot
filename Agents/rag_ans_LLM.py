from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def rag_answer_LLM(state: State):
  
    rag_answer = state["retriver_doc"]
    user_query = state["messages"][-1].content
    system_prompt = """
    You are the final answering agent in a multi-stage AI assistant.
    You will get a RAG-based answer for the user query.
    """

    judge_query = f"Question: {user_query}\nAnswer: {rag_answer}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": judge_query}
    ]

    reply = llm.invoke(messages)
    print(reply.content)

    state["messages"].append(AIMessage(content=reply.content))
    
    return state