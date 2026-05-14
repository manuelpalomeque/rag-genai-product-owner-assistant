from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Prompts.agente_1_mentor_rag_scrum import mentor_system_prompt
from Config.modelos import definir_modelo_groq
from App.rag.recuperacion.retriever import get_retriever

def construir_mentor_chain():

    retriever = get_retriever()

    modelo = definir_modelo_groq()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", mentor_system_prompt),
            (
                "human",
                """
                Contexto:
                {context}

                Pregunta:
                {question}
                """
            ),
        ]
    )

    chain = (
        {
            "context": lambda x: _retrieve_context(
                retriever,
                x["question"],
            ),
            "question": lambda x: x["question"],
        }
        | prompt
        | modelo
        | StrOutputParser()
    )

    return chain


def _retrieve_context(retriever, question: str,) -> str:
    docs = retriever.invoke(question)

    return "\n\n".join(
        [doc.page_content for doc in docs]
    )