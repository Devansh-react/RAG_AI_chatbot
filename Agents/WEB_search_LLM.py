from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def web_LLM_answer(state: State):
    history_messages = state["messages"]
    user_query = state["messages"][-1].content
    web_result = state["web_result"]
    
    system_prompt = """
    You are a friendly and intelligent AI assistant.

    Your job is to take the user's question, the retrieved answer (from a web or knowledge search), and the recent conversation history, and craft a helpful, clear, and engaging response.

    Please follow these rules:
    1. Rephrase the given answer in a natural, conversational tone — imagine you're helping a friend understand it.
    2. DO NOT make up facts. Only use the information provided in the retrieved answer and the user's messages.
    3. Make the response well-structured — use short paragraphs, lists, or highlights if it improves readability.
    4. Try to naturally include context from the previous messages to keep the flow smooth and personalized.
    5. Optionally ask a short follow-up question at the end to keep the conversation interactive (but only if it makes sense based on the topic).

    Your goal: Keep it informative yet friendly, concise but complete, and above all, human — not robotic.
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
