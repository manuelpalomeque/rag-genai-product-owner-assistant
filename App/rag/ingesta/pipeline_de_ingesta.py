from dotenv import load_dotenv
load_dotenv()

from App.rag.ingesta.cargadores import cargar_pdf
from App.rag.ingesta.chunking import dividir_documentos
from App.rag.ingesta.metadata import agregar_metadata
from App.rag.vectores.chroma_store import crear_chroma_store



PDF_PATH = ("App/rag/Documents/Scrum Master_Scrum Manager.pdf")


def ejecutar_ingestion():
    print("Cargando PDF...")
    documentos = cargar_pdf(PDF_PATH)
    print(f"Se cargaron {len(documentos)} páginas")

    print("Dividiendo documentos...")
    chunks = dividir_documentos(documentos)
    print(f"Se generaron {len(chunks)} chunks")

    print("Agregando metadata...")
    chunks = agregar_metadata(
        chunks=chunks,
        document_name=(
            "Scrum Master Scrum Manager"
        ),
        source=PDF_PATH,
    )

    print("Creando ChromaDB...")
    crear_chroma_store(chunks=chunks)

    print("Ingestión completada")