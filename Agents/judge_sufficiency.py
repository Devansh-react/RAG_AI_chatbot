from schema.Models import State
from utilities.LLM_init import llm


def judge_sufficiency(state: State) -> State:
    user_query = state["messages"][-2].content  # last human message
    rag_answer = state["messages"][-1].content
    docs = state.get("retriver_doc", [])
    if docs is None or len(docs) == 0:
        state["is_justified"] = "no"
        return state
    context = "\n\n".join(d.page_content for d in docs)

    system_prompt = """
You are a strict evaluator. 

Decide whether the answer is relevant and correctly answers the user's question
using ONLY the provided context.

Return:
- "yes" → if the answer is relevant and supported by the context
- "no"  → if the answer is unrelated, hallucinated, or context is insufficient

Respond with only one word: yes or no.
"""

    judge_input = f"""
Question:
{user_query}

Context:
{context}

Answer:
{rag_answer}
"""

    result = llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": judge_input},
        ]
    )
    if isinstance(result, list):
        result = result[0].content
    else:
        result = result.content
    result = result.strip().lower() # type: ignore

    state["is_justified"] = "yes" if result == "yes" else "no"
    return state
