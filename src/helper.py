from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from typing import List
from langchain.schema import Document

# Extract text from PDF files in the "data" directory
def load_pdf_file(directory):
    loader = DirectoryLoader(directory,
                              glob="*.pdf",
                              loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# filter to minimal docs
def filter_to_minimal_docs(docs:List[Document]) -> List[Document]:
    """given list of document objects, return a new list of document objects containing only 'source" in metadata in original page content"""

    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

# split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    text_chunks = text_splitter.split_documents(minimal_docs)
    return text_chunks

# embedding model
from langchain.embeddings import HuggingFaceEmbeddings
def download_hugging_face_embeddings():
    """Download the embedding model from HuggingFace and return the embeddings object"""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
        )
    return embeddings

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory() 
    return store[session_id]



