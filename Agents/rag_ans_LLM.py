from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def rag_answer_LLM(state: State):
  
    rag_answer = state["retriver_doc"]
    user_query = state["messages"][-1].content
    history_messages = state["messages"]
    system_prompt = """
    You are a helpful assistant .dont't behave like a chat bot or any AI based agent mimic like a human beign with feelings 

    You are given:
    - The user's current question
    - A RAG-generated answer (factual)
    - A short history of the conversation

    Your job is to:
    1. Rephrase the RAG answer in a more conversational and engaging tone
    2. Keep all factual information intact
    3. Optionally add a follow-up question to keep the conversation going

    Respond in a friendly and concise manner.
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
    # print(chat_history[-5:])
    reply = llm.invoke(messages)
    if(reply):
        print(reply.content)
    state["messages"].append(AIMessage(content=reply.content))
    
    return state