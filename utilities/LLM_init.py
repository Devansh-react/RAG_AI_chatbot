from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()
llm = init_chat_model("google_genai:gemini-2.0-flash", temperature=0.7, model_kwargs={"streaming": True})

