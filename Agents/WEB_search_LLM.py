from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def web_LLM_answer(state: State):
    history_messages = state["messages"][-5:]
    user_query = state["messages"][-1].content
    web_result = state["web_result"]
    
    system_prompt = """
    You are the final answering agent in a multi-stage AI assistant.you will get a web-seach for the user query .
    you job is to using the web result & user query provid a proper structured output to the use no need to add answer from your side just provid the structured output to the user you give a concise and readable answer .
    """
    
    chat_history = []
    for msg in history_messages:
        if isinstance(msg, HumanMessage):
            chat_history.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            chat_history.append({"role": "assistant", "content": msg.content})
    judge_input = f"Question: {user_query}\nWeb_Answer: {web_result}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": judge_input}
    ]+chat_history

    reply = llm.invoke(messages)

    state["messages"].append(AIMessage(content=reply.content))
    
    return state
