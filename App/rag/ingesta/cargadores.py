from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document



def cargar_pdf(path: str) -> list[Document]:

    loader = PyPDFLoader(path)

    return loader.load()