from dotenv import load_dotenv
load_dotenv()

from langchain_core.vectorstores import VectorStoreRetriever
from App.rag.vectores.chroma_store import cargar_chroma_store



def get_retriever() -> VectorStoreRetriever:

    vector_store = cargar_chroma_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    return retriever