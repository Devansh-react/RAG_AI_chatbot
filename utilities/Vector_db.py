from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader

from utilities.LLM_init import llm
from schema.Models import State
from pathlib import Path
import hashlib
import os


def get_faiss_path(pdf_path: str, model_name: str) -> str:
    key = f"{pdf_path}_{model_name}"
    return f"faiss_index/{hashlib.md5(key.encode()).hexdigest()}"


def run_pdf_rag(state: State, query: str):
    pdf_path = state.get("pdf_path")

    if not pdf_path or not os.path.exists(pdf_path):
        return "No PDF file found.", []

    model_name = "sentence-transformers/all-mpnet-base-v2"
    faiss_path = get_faiss_path(pdf_path, model_name)

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True}
    )

    # Load or build FAISS
    if Path(faiss_path).exists():
        vector_db = FAISS.load_local(
            faiss_path, embeddings, allow_dangerous_deserialization=True
        )
    else:
        docs = PyPDFLoader(pdf_path).load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=550,
            chunk_overlap=60,
        )
        chunks = splitter.split_documents(docs)
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(faiss_path)

    # ---- RETRIEVE (NO SCORE FILTERING) ----
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})
    retrieved_docs = retriever.invoke(query)

    # ---- GENERATE ----
    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    prompt = PromptTemplate(
        template="""
You must answer ONLY using the context below.
If the context does not contain the answer, say:
"No relevant information found."

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"],
    )

    chain = (
        {
            "context": lambda _: format_docs(retrieved_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(query)

    return answer, retrieved_docs
