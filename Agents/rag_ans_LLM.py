from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def rag_answer_LLM(state: State):
  
    rag_answer = state["retriver_doc"]
    user_query = state["messages"][-1].content
    history_messages = state["messages"][-5:]
    system_prompt = """
    You are the final AI responder in a multi-agent RAG (Retrieval-Augmented Generation) pipeline.
    You are given a user query and supporting RAG-based evidence.
    Your job is to:
    1. Give a helpful, concise, and friendly response based on the retrieved evidence.
    2. Follow up with a relevant question to continue the conversation naturally.
    Be conversational, curious, and professional — like a helpful human assistant.
    """
    chat_history = []
    for msg in history_messages:
        if isinstance(msg, HumanMessage):
            chat_history.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            chat_history.append({"role": "assistant", "content": msg.content})
              
    judge_query = f"Question: {user_query}\nAnswer: {rag_answer}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": judge_query}
    ] + chat_history

    reply = llm.invoke(messages)
    print(reply.content)

    state["messages"].append(AIMessage(content=reply.content))
    
    return state