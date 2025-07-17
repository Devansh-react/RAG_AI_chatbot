import streamlit as st
import requests
from streamlit_chat import message  # pip install streamlit-chat
import uuid

# Set up Streamlit page
st.set_page_config(page_title="LangGraph Chatbot", layout="centered")
st.title("🧠 AI Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat input field
user_input = st.chat_input("Ask me anything...")

# Handle user input
if user_input:
    # Show user message immediately
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        # Send to FastAPI backend
        response = requests.post(
            "http://localhost:8000/chat",
            json={ "session_id": st.session_state.session_id,"User_message": user_input}
        )

        # Handle API response
        if response.status_code == 200:
            reply = response.json().get("reply", "⚠️ No reply received.")
        else:
            reply = f"⚠️ Server error {response.status_code}"
    except Exception as e:
        reply = f"❌ Request failed: {str(e)}"

    # Add assistant reply to history
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Display chat messages
for i, chat in enumerate(st.session_state.chat_history):
    message(chat["content"], is_user=(chat["role"] == "user"), key=str(i))
