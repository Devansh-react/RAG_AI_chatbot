from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from utilities.LLM_init import llm
from langchain_community.document_loaders import PyPDFLoader
from schema.Models import State
from pathlib import Path
import hashlib
import os

# Create a unique FAISS index path based on the PDF file path
def get_faiss_path(pdf_path: str) -> str:
    hashed = hashlib.md5(pdf_path.encode()).hexdigest()
    return f"faiss_index/{hashed}"

def run_pdf_rag(state: State, query: str) -> str:
    pdf_path = state.get("pdf_path")

    # Validate PDF existence
    if not pdf_path or not os.path.exists(pdf_path):
        return "**No PDF file found or invalid path.**"

    faiss_path = get_faiss_path(pdf_path)

    # Initialize embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Load or create FAISS index
    if Path(faiss_path).exists():
        vector_db = FAISS.load_local(
            faiss_path, embeddings, allow_dangerous_deserialization=True
        )
    else:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        if not docs:
            return "**Failed to read PDF.**"

        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ".", ","],
            chunk_size=150,
            chunk_overlap=20,
            length_function=len,
        )
        chunks = text_splitter.split_documents(docs)

        # Create FAISS index and persist locally
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(faiss_path)

    # Create prompt template
    prompt = PromptTemplate(
        template="""Use the following context to answer the question. If you cannot answer based on the context, say "No relevant information found."

Context: {context}

Question: {question}

Answer:""",
        input_variables=["context", "question"],
    )

    # Build retrieval chain using LCEL
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "lambda_mult": 0.25}
    )
    
    # Format documents helper function
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create the chain using LCEL
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Execute query
    result = chain.invoke(query)
    return result