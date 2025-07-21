from langgraph.graph import START , END , StateGraph
# agents
from Agents.Final_answer import final_answer
from Agents.judge_sufficiency import judge_sufficiency
from Agents.rag_ans_LLM import rag_answer_LLM
from Agents.WEB_search_LLM import web_LLM_answer
# tools
from Tools.webSearch_tool import search_tool
from Tools.rag_tools import Rag_tool

# message classifer
from classifiers.message_classifiers import Classify_user
#  utilities 
from utilities.LLM_init import llm
# schema
from schema.Models import State


# routing function 
def route(state:State):
    print("Routing based on messages_route:", state.get("messages_route"))
    match state.get("messages_route"):
        case "Web_search":
            return "search_tool"
        case "RAG_answer_Queary" :
            return "rag_tool"
        case _ :
            return "final_answer"
    
def route_by_justification(state: State):
    route = state.get("is_justified")
    print(f"Routing based on is_justified: {route}")
    if route == "yes":
        print("RAG answer sufficient → ending.")
        return "rag_ans_LLM"
    else:
        print("RAG insufficient → invoking LLM fallback.")
        return "final_answer"
    
    
# graph builder
def build_graph():
    graph_builder = StateGraph(State)
    
    #  making nodes 
    graph_builder.add_node("inputClassifer", Classify_user)
    graph_builder.add_node("route", route)
    graph_builder.add_node("route_by_justification", route_by_justification)
    
    graph_builder.add_node("rag_tool", Rag_tool)
    graph_builder.add_node("rag_ans_LLM", rag_answer_LLM)
    
    
    graph_builder.add_node("search_tool",search_tool)
    graph_builder.add_node("web_LLM_answer",web_LLM_answer)
    
    graph_builder.add_node("judge_sufficiency",judge_sufficiency)
    graph_builder.add_node("final_answer",final_answer)



#  add edges 
    graph_builder.set_entry_point("inputClassifer")
    graph_builder.add_conditional_edges("inputClassifer",route)
    graph_builder.add_edge("rag_tool","judge_sufficiency")
    graph_builder.add_conditional_edges("judge_sufficiency",route_by_justification)
    
    graph_builder.add_edge("search_tool","web_LLM_answer")

    
    graph_builder.add_edge("web_LLM_answer",END)
    graph_builder.add_edge("rag_ans_LLM",END)
    graph_builder.add_edge("final_answer",END)
    
    
    return graph_builder.compile()