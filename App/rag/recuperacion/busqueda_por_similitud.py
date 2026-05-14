from dotenv import load_dotenv
load_dotenv()
from App.rag.vectores.chroma_store import cargar_chroma_store


def test_busqueda_por_similitud():

    vector_store = cargar_chroma_store()

    results = (
        vector_store.similarity_search_with_score(
            query="Que son los artefactos de scrum?",
            k=5,
        )
    )

    for idx, (doc, score) in enumerate(
        results,
        start=1,
    ):

        print(f"\nResultado {idx}")
        print("-" * 50)
        print(f"Score: {score}")
        print(doc.page_content[:500])


if __name__ == "__main__":

    test_busqueda_por_similitud()