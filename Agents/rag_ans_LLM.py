from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def rag_answer_LLM(state: State):
  
    rag_answer = state["retriver_doc"]
    user_query = state["messages"][-1].content
    history_messages = state["messages"][-5:]
    system_prompt = """
You are an AI assistant in a multi-agent Retrieval-Augmented Generation (RAG) pipeline.

    The assistant before you has already answered the user's query based on retrieved documents.

    Your ONLY task is to:
    1. KEEP the given answer AS IT IS.
    3. DO NOT change or summarize the original answer.

    Tone: Curious, helpful, and professional.
    Output Format:
    <Original Answer>
"""
    chat_history = []
    for msg in history_messages:
        if isinstance(msg, HumanMessage):
            chat_history.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            chat_history.append({"role": "assistant", "content": msg.content})
              
    # judge_query = f"Question: {user_query}\nAnswer: {rag_answer}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ] + chat_history

    reply = llm.invoke(messages)
    if(reply):
        print(reply.content)
    else:
        print("MMO reply ")

    state["messages"].append(AIMessage(content=reply.content))
    
    return state