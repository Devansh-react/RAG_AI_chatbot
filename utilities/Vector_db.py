from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utilities.LLM_init import llm
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from schema.Models import State
import hashlib
from pathlib import Path
import os

# create a hash for the pdf path ::
def get_faiss_path(pdf_path:str)->str:
    hashed = hashlib.md5(pdf_path.encode()).hexdigest()
    return f"faiss_index/{hashed}"
    
def run_pdf_rag(state: State, query: str) -> str:
    pdf_path = state.get("pdf_path")

    if not pdf_path or not os.path.exists(pdf_path):
        return "**No PDF file found or invalid path.**"

    faiss_path = get_faiss_path(pdf_path)
    
    if(Path(faiss_path).exists()):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_db = FAISS.load_local(faiss_path,embeddings,allow_dangerous_deserialization=True)
    else:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        if not docs:
            return "**Failed to read PDF.**"

        # Step 2: Split text
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ".", ","],
            chunk_size=150,
            chunk_overlap=20,
            length_function=len,
        )
        chunks = text_splitter.split_documents(docs)

        # Step 3: Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")   
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(faiss_path)


        # Step 4: Prompt template
    prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant. Use the provided context to answer the user's question clearly and concisely.

        <context>
        {context}
        </context>

        Question: {input}

        Instructions:
        - Only answer based on the information in the context.
        - If the context does not have the information, reply exactly: **"No relevant information found."**
        - Do not make up information or assume beyond what's provided.

        Answer:
     """)

    # Step 5: Retrieval chain
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 6, 'lambda_mult': 0.25}
    )
    chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

    # Step 6: Run
    result = chain.invoke({"input": query})
    return result["answer"]
