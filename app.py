import streamlit as st
import requests
from streamlit_chat import message  
import uuid
import os

# ---------- Page Config ----------
st.set_page_config(page_title="LangGraph Chatbot", layout="centered")

# ---------- Custom CSS Styling ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(to right, #232526, #414345);
        color: black;
    }

    .stChatMessage {
        padding: 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stChatMessage.user {
        background: linear-gradient(to right, #007bff, #00aaff);
        border-top-left-radius: 20px;
        border-bottom-left-radius: 20px;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 0px;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size:1.2rem;
        margin-left: 50%;
    }

    .stChatMessage.bot {
        background:linear-gradient(to left, #5cb3cc, #87CEEB);
        border-top-left-radius: 20px;
        border-bottom-left-radius: 20px;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 0px;
        font-size:1.1rem;
        text-align: left;
        margin-right: 30%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        color: Black;
        text-align: Center;
        margin-right: 30%;
    }

    .st-emotion-cache-1c7y2kd {
        padding: 2rem !important;
    }

    .stChatInputContainer {
        padding-top: 1rem;
    }

    .stButton button {
        border-radius: 10px;
        background-color: #00f2fe;
        color: black;
        border: 2px;
    }

    .stTextInput input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 style='text-align: center; color: #00f2fe;`font-size: 5rem;`'>RAG ChatBot©️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>An intelligent assistant powered by LangGraph and RAG.</p>", unsafe_allow_html=True)

# ---------- PDF Upload ----------
with st.sidebar:
    st.header("Upload PDF Interaction")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        save_path = os.path.join("uploaded_pdfs", uploaded_file.name)
        os.makedirs("uploaded_pdfs", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"Uploaded and saved: {uploaded_file.name}")

        # Store path for use in backend (if needed later)
        st.session_state.pdf_path = save_path


# ---------- Session Setup ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---------- Chat Input ----------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        # You can also send `st.session_state.pdf_path` to backend if needed
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "session_id": st.session_state.session_id,
                "User_message": user_input,
                 "pdf_path": st.session_state.get("pdf_path", "")
            }
        )
        if response.status_code == 200:
            reply = response.json().get("reply", "⚠️ No reply received.")
        else:
            reply = f"⚠️ Server error {response.status_code}"
    except Exception as e:
        reply = f"❌ Request failed: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# ---------- Chat History Display ----------
for i, chat in enumerate(st.session_state.chat_history):
    with st.container():
        if chat["role"] == "user":
            st.markdown(f"<div class='stChatMessage user'>{chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stChatMessage bot'>{chat['content']}</div>", unsafe_allow_html=True)
