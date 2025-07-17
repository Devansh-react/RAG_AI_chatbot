# tools/web_search.py
from langchain_community.utilities import GoogleSerperAPIWrapper
from schema.Models import State
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()  

# Initialize search tool
search = GoogleSerperAPIWrapper()

def serper_tool(state: State) -> str:
    """
    Perform a web search using Serper.dev (Google-based).
    """
    query = next((m.content for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None)

    if not query:
        return "No user input found."

    try:
        result = search.run(str(query))  
    except Exception as e:
        result = f"Web search failed: {str(e)}"

    return result

def search_tool(state: State) -> State:
    """
    LangGraph-compatible wrapper for web search.
    """
    result = serper_tool(state)
    state["web_result"] = result
    return state
