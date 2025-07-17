from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utilities.LLM_init import llm
from pathlib import Path
#  selecting the file 


# use lasy loading funtion for production level code 
def load_document(path:str)->str:
    file = Path(path)
    if not file:
        return("path not found")
    else:
        return file.read_text(encoding="utf-8");    
    
    

document_file = load_document("./utilities/treatment.txt")
    
# creatinf text splitter 

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n","\n"," ",".",","],
    chunk_size=150,
    chunk_overlap=20,
    length_function = len,
)

docs = text_splitter.create_documents([document_file])

#  create embeddings 

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_db = FAISS.from_documents(docs,embeddings)

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


chain  = create_stuff_documents_chain(llm , prompt)
#  retriver
retriver = vector_db.as_retriever(
    search_type="mmr",  # similarity search
    search_kwargs={'k': 6, 'lambda_mult': 0.25}
)

retriver_chain = create_retrieval_chain(retriver,chain)


    
