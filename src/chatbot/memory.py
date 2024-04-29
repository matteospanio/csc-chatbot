from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_chroma import Chroma
import pickle
from pathlib import Path
import os
import yaml


def load_documents() -> list[Document]:
    path = os.getenv("DATA_PATH")
    if path is None:
        raise Exception("DATA_PATH environment variable not set.")
    with open(path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    pages = data["pages"]
    loader = WebBaseLoader(pages)
    return loader.load()


def load_chat_messages() -> list[BaseMessage]:
    path = os.getenv("CHAT_MEMORY")
    if path is None:
        raise Exception("CHAT_MEMORY environment variable not set.")
    messages_path = Path(path)
    if not messages_path.exists():
        return []
    with messages_path.open("rb") as f:
        return pickle.load(f)


def save_chat_messages(messages: list[BaseMessage]) -> None:
    path = os.getenv("CHAT_MEMORY")
    if path is None:
        raise Exception("CHAT_MEMORY environment variable not set.")
    messages_path = Path(path)
    with messages_path.open("wb") as f:
        pickle.dump(messages, f)


def load_pdfs() -> list[Document]:
    path = os.getenv("PDF_PATH")
    if path is None:
        raise Exception("PDF_PATH environment variable not set.")
    loader = PyPDFDirectoryLoader(path)
    return loader.load()


def split_text(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Number of docs: {len(documents)}")
    print(f"Number of chunks: {len(chunks)}")

    return chunks


def get_memory(embeddings: Embeddings) -> Chroma:
    """Get the chroma database."""
    path = os.getenv("CHROMA_PATH")
    if path is None:
        raise Exception("CHROMA_PATH environment variable not set.")
    return Chroma(embedding_function=embeddings, persist_directory=path)


def create_database_from_docs(docs: list[Document], model: Embeddings) -> Chroma:
    # save to chroma
    path = os.getenv("CHROMA_PATH")
    if path is None:
        raise Exception("CHROMA_PATH environment variable not set.")
    db = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=path,
    )

    return db


def create_memory(with_pdf: bool, with_web: bool) -> None:
    """Create a chroma database from the documents."""
    path = os.getenv("CHROMA_PATH")
    if path is None:
        raise Exception("CHROMA_PATH environment variable not set.")
    if Path(path).exists():
        raise Exception("Chroma database already exists.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # load documents
    chunks = []

    if with_web:
        docs = load_documents()
        chunks.extend(split_text(docs))

    if with_pdf:
        pdfs = load_pdfs()
        chunks.extend(split_text(pdfs))

    # save to chroma
    create_database_from_docs(chunks, embeddings)
