"""Memory management for the chatbot."""

import pickle
from pathlib import Path

import click
import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.messages import BaseMessage
from langchain_openai import OpenAIEmbeddings

from chatbot.cli import __app_name__

APP_DIR = Path(click.get_app_dir(__app_name__))
MEMORY = APP_DIR / "memory"
CHAT_MEMORY = MEMORY / "history.pkl"
CHROMA_PATH = MEMORY / "chroma"


def load_documents() -> list[Document]:
    """Load the documents from filesystem."""
    path = ""
    with Path(path).open() as f:
        data = yaml.safe_load(f)
    pages = data["pages"]
    loader = WebBaseLoader(pages)
    return loader.load()


def load_chat_messages() -> list[BaseMessage]:
    """Load the chat messages from the memory.

    Returns
    -------
    list[BaseMessage]
        The list of chat messages.

    """
    if not CHAT_MEMORY.exists():
        return []
    with CHAT_MEMORY.open("rb") as f:
        return pickle.load(f)  # noqa: S301


def save_chat_messages(messages: list[BaseMessage]) -> None:
    """Save the chat messages to the memory.

    Parameters
    ----------
    messages : list[BaseMessage]
        The list of chat messages to save.

    """
    if not CHAT_MEMORY.parent.exists():
        CHAT_MEMORY.parent.mkdir()
    with CHAT_MEMORY.open("wb") as f:
        pickle.dump(messages, f)


def load_pdfs(path: str | Path) -> list[Document]:
    """Load the pdfs from the path."""
    loader = PyPDFDirectoryLoader(path)
    return loader.load()


def split_text(
    documents: list[Document],
    chunk_size: int,
    overlap: int,
) -> list[Document]:
    """Split the text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Number of docs: {len(documents)}")
    print(f"Number of chunks: {len(chunks)}")

    return chunks


def get_memory(embeddings: Embeddings) -> Chroma:
    """Get the chroma database."""
    return Chroma(embedding_function=embeddings, persist_directory=str(CHROMA_PATH))


def create_database_from_docs(docs: list[Document], model: Embeddings) -> Chroma:
    """Create a chroma database from the documents."""
    # save to chroma
    db = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=str(CHROMA_PATH),
    )

    return db


def create_memory(
    api_key: str,
    resource: Path,
    file_format: str,
    chunk_size: int,
    overlap: int,
) -> None:
    """Create a chroma database from the documents."""
    if CHROMA_PATH.exists():
        msg = "Chroma database already exists."
        raise Exception(msg)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=api_key,  # type: ignore
    )

    # load documents
    chunks = []

    if not resource.is_dir():
        msg = "È stato inserito un file come fonte di risorse."
        raise Exception(msg)

    if file_format == "web":
        docs = load_documents()
        chunks.extend(split_text(docs, chunk_size, overlap))

    if file_format == "pdf":
        pdfs = load_pdfs(resource)
        chunks.extend(split_text(pdfs, chunk_size, overlap))

    # save to chroma
    create_database_from_docs(chunks, embeddings)
