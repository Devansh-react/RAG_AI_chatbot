# 🧠 RAG ChatBot ©️

A multi-agent, retrieval-augmented generation (RAG) chatbot built with **LangGraph**, **FastAPI**, and **Gemini Pro**, capable of classifying inputs, performing intelligent web search, and retrieving contextual knowledge before generating answers—all with a modular, production-ready structure.

![RAG Chatbot Architecture](image.png)

---

## 🚀 Features

✅ **Multi-Stage Agents** via LangGraph  
✅ **LLM Classifier**: Distinguishes between logical vs. emotional queries  
✅ **Contextual Answering** via internal document retrieval (FAISS + Gemini Embeddings)  
✅ **Web Search Agent** using DuckDuckGo for fallback queries  
✅ **Custom Final Answering Agent** with memory-aware responses  
✅ **FastAPI Backend** with Session ID Support  
✅ **Streamlit Frontend** with persistent chat history  
✅ **PostgreSQL Integration** (chat history persistence)  
✅ Modular and scalable folder structure  
✅ Gemini API integration (`models/gemini-pro` + `embedding-001`)

---

## 📂 Project Structure

```
RAGAGENT/
│
├── Agents/                  # LangGraph agent definitions
├── Tools/
│   ├── rag_tools.py         # FAISS-based retrieval logic
│   └── webSearch_tool.py    # DuckDuckGo web search tool
├── classifiers/             # Sentiment / Input type classifier agents
├── graph/                   # LangGraph build and flow logic
├── schema/
│   └── Models.py            # Pydantic schemas for input/output
├── utilities/
│   └── LLM_init.py          # Gemini LLM initialization
├── database/                # PostgreSQL interaction layer (chat history)
├── main.py                  # LangGraph flow starter
├── app.py                   # FastAPI entrypoint
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (Gemini API key etc.)
├── FOLDER_STRUCT.txt        # Optional: Visual folder reference
├── image.png                # Architecture diagram
└── README.md                # 📄 This file
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🧪 Setup Environment

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
```

> 💡 Note: Use a secure password and ensure PostgreSQL is running locally.

### 3. ▶️ Run the Backend

```bash
uvicorn app:app --reload
```

### 4. 💬 Run the Frontend (Streamlit)

```bash
streamlit run main.py
```

---

## 🧠 How It Works

1. **User Input** → Sent to backend with session ID
2. **Classifier Agent** → Determines if input is emotional or logical
3. **Tool Selection**:
   - Logical → FAISS + Gemini Embedding
   - Emotional → Gemini Pro directly
   - Unknown / Insufficient → WebSearch Tool (DuckDuckGo)
4. **Final Answer Agent** → Generates coherent, human-like answer
5. **Chat History** stored in PostgreSQL

---

## 💡 Example Query Flow

```mermaid
graph LR
A[User Message] --> B{Classifier}
B -->|Logical| C[RAG Tool: FAISS + Gemini]
B -->|Emotional| D[LLM Direct Answer]
B -->|Fallback| E[DuckDuckGo Tool]
C & D & E --> F[Final Answer Agent]
F --> G[Reply to User + Store in DB]
```

---

## 📸 Preview

> Powered by Streamlit frontend with real-time chat memory:

![Preview UI](image.png)

---

## 🔒 Security Considerations

- API keys are stored in `.env`
- LangGraph safely routes messages internally (no user info shared with LLM)
- Web search responses are filtered through a final answering node

---

## 📌 TODO / Improvements

- ✅ Add image generation agent
- 🔄 Implement Redis for async memory store
- 🧪 Write Pytest coverage for agents
- 🌐 Deploy via Docker + Nginx

---

## 🤝 Credits

Built with 💙 using:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Gemini Pro](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

## 📜 License

MIT License