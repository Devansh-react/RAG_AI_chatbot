# 🔍 RAGAgent - Hybrid RAG + Web Search AI Chatbot

RAGAgent is an intelligent hybrid chatbot system that combines **Retrieval-Augmented Generation (RAG)** and **real-time web search** capabilities to provide precise, up-to-date, and context-aware responses. It uses **Google Gemini** as the underlying LLM and classifies queries to route them through the optimal information pipeline.



---

## 🧠 System Overview

The application handles queries by routing them based on **intent classification** into three paths:

1. **RAG Lookup**: If query is informational or previously known, it uses vector DB retrieval.
2. **Web Search**: If it's real-time (e.g., current events), it uses a DuckDuckGo search tool.
3. **LLM Answering**: If neither RAG nor web search answers it well, Gemini LLM generates a response.

---

## 📁 Project Structure

```bash
RAGAGENT/
│
├── Agents/                  # LLM-based agents (retrievers, checkers)
├── Tools/                   # Custom tools
│   ├── rag_tools.py
│   └── webSearch_tool.py    # DuckDuckGo web search tool
├── classifiers/             # Intent classifiers
├── database/                # RAG DB (FAISS or similar)
├── graph/                   # LangGraph workflow configuration
├── schema/                  # Pydantic schemas (e.g., State)
│   └── Models.py
├── utilities/               # Helpers, Gemini init, etc.
├── .env                     # Environment variables (API keys, etc.)
├── app.py                   # FastAPI app for serving frontend/backend
├── main.py                  # Entry point for initializing LangGraph
├── requirements.txt         # Python dependencies
├── image.png                # System architecture diagram
└── FOLDER_STRUCT.txt        # Folder layout (optional docs)
```

---

## 🛠️ Features

- 🔍 **Query Classification** using intent detection
- 📚 **RAG Integration** via FAISS vector DB
- 🌐 **Real-time Web Search** using DuckDuckGo API
- 🤖 **Gemini LLM** for fallback generation
- 🧪 Modular tools and graph nodes for LangGraph
- 🚀 Built with **FastAPI** for scalability

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/RAGAgent.git
cd RAGAgent
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file with your Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

### 4. Run the App

```bash
uvicorn app:app --reload
```

---

## 🔧 Tools Used

| Tool            | Purpose                      |
|-----------------|------------------------------|
| **LangChain / LangGraph** | Workflow and LLM orchestration |
| **Gemini API**  | Large Language Model         |
| **DuckDuckGo API** | Real-time web search         |
| **FAISS**       | Vector similarity search     |
| **FastAPI**     | Backend framework            |
| **Pydantic**    | Input/output validation      |

---

## 📌 Query Flow

```
User Message
   ↓
Classifier (Intent)
   ├─→ RAG Lookup (Vector DB) ─→ Checker ─→ LLM Answer or RAG Answer
   └─→ Web Search ─→ Gemini LLM ─→ Final Answer
```

Diagram:  
![Query Flow](./image.png)

---

## 📈 Future Improvements

- Add memory for context retention
- Integrate LangSmith for observability
- UI frontend for chat interactions
- Add Redis for caching results

---

## 📄 License

This project is licensed under the MIT License.