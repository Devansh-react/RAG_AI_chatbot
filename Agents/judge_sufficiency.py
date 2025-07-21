from schema.Models import State
from utilities.LLM_init import llm

def judge_sufficiency(state: State) -> State:
    user_query = state["messages"][-1].content
    
    rag_output = state.get("retriver_doc", "No answer found.")    
    system_prompt = """
    dont't behave like a chat bot or any AI based agent mimic like a human beign with feelings 
    You are an evaluation agent.

    Your task is to decide whether the given answer (from a RAG system) is sufficient and relevant to the user's original question.

    Please follow these instructions carefully:

    Respond with **"yes"** if:
    - The answer is clear, complete, and **directly answers the user's question** with relevant factual content **found in the RAG knowledge base.**

    Respond with **"no"** if:
    if it says something like No relevant information found.then only return NO 
    Respond with only one word: **yes** or **no** (all lowercase). Do NOT explain.
"""

    # make sur eto pass both input question and rag output answer to llm along with prompot
    judge_input = f"Question: {user_query}\nAnswer: {rag_output}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": judge_input}
    ]

    result = llm.invoke(messages).content.lower().strip() # type: ignore
    # print("🧠 Judge Input:\n", judge_input)
    # print("🤖 Judge Output:\n", result)
    
    if result not in("yes","no"):
        result ="no"
    state["is_justified"] = result
    return state
