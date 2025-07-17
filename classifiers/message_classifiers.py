from utilities.LLM_init import llm
from pydantic import BaseModel, Field
from schema.Models import State
from typing import Literal

class inputClassifier(BaseModel):
    message: Literal["RAG_answer_Queary", "Web_search"] = Field(
        ..., description="Classify the user message into 'RAG_answer_Queary' or 'Web_search'."
    )

def Classify_user(state: State) -> State:
    last_message = state["messages"][-1]
    user_input = last_message.content.strip()

    classify_llm = llm.with_structured_output(inputClassifier)

    system_prompt = """ 
    You are an AI assistant that classifies user queries into one of two categories:

    - "Web_search": if the query is about real-time, current events, changing data, live statistics, breaking news, stock prices, weather, or anything that requires up-to-date web information.
    
    - "RAG_answer_Queary": if the query is about general knowledge, history, static facts, company profiles, law, programming, or anything that can be answered using a fixed knowledge base.

    Respond with only one of the following exactly: "RAG_answer_Queary" or "Web_search".
    Do NOT include explanations or anything else.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    result = classify_llm.invoke(messages)
    state["messages_route"] = result.message  # type: ignore
    return state
