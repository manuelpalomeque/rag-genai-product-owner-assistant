from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings


def obtener_embeddings():

    return HuggingFaceEmbeddings(
        model_name=(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    )