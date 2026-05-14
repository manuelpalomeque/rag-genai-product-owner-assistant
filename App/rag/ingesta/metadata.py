from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document


def agregar_metadata(
    chunks: list[Document],
    document_name: str,
    source: str,
) -> list[Document]:

    for idx, chunk in enumerate(chunks):

        chunk.metadata["document_name"] = (
            document_name
        )

        chunk.metadata["chunk_id"] = idx

        chunk.metadata["source"] = source

    return chunks