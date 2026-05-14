from dotenv import load_dotenv
load_dotenv()

from App.rag.ingesta.pipeline_de_ingesta import ejecutar_ingestion

if __name__ == "__main__":
    ejecutar_ingestion()