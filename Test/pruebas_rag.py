from dotenv import load_dotenv

#---
load_dotenv()

from App.rag.recuperacion.retriever import get_retriever
from pprint import pprint

def main():
    retriever = get_retriever()
    query = "Que son los artefactos de scrum?"
    results = retriever.invoke(query)

    print("\nRESULTADOS\n")

    for idx, doc in enumerate(results, start=1):
        print(f"\nResultado {idx}")
        print("-" * 50)
        print(doc.page_content[:500])
        print("\nMetadata:")
        pprint(doc.metadata)
        print("-" * 50)
        

if __name__ == "__main__":

    main()