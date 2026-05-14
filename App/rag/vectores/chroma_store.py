from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_core.documents import Document
from App.rag.ingesta.embeddings import obtener_embeddings


PERSIST_DIRECTORY = "data/chroma_db"


def crear_chroma_store(chunks: list[Document],) -> Chroma:

    embeddings = obtener_embeddings()

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )


def cargar_chroma_store() -> Chroma:

    embeddings = obtener_embeddings()

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
    )