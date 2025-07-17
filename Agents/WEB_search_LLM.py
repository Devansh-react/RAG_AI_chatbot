from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
from utilities.LLM_init import llm

def web_LLM_answer(state: State):
    history_messages = state["messages"][-5:]
    user_query = state["messages"][-1].content
    web_result = state["web_result"]
    
    system_prompt = """
    You're a helpful AI assistant responsible for summarizing and formatting information gathered from a web search.
    Your task is to:
    1. Use the web search results and the user query to create a well-structured, human-friendly, and informative answer.
    2. Keep the tone friendly, conversational, and natural — as if you're genuinely trying to help someone out.
    3. Avoid robotic phrases or overly formal language. Don’t generate extra facts on your own; stick to the web result.
    4. Make the content easy to scan, clear, and concise — use bullets or short paragraphs if helpful.

    Imagine you're explaining the result to a friend — that's the tone you're aiming for.
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
