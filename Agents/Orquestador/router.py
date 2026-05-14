from dotenv import load_dotenv

from langchain.messages import HumanMessage

from langchain_core.messages import HumanMessage
from pprint import pprint
from Config.modelos import definir_modelo_groq


load_dotenv()

modelo_orquestador = definir_modelo_groq()


def router_node(state):

    user_query = state["messages"][-1].content

    prompt = f"""
    Eres un supervisor de agentes IA.

    Decide qué agente debe responder.

    Opciones:

    - mentor
      Preguntas sobre Scrum,
      Agile,
      ceremonias,
      Jira conceptual,
      metodologías.

    - jira
      Consultas operacionales:
      tickets,
      issues,
      sprint,
      blockers,
      backlog,
      creación de tareas,
      filtrar historias de usuario por sprint,
      crear informe de fin de sprint para stakeholders.

    Consulta:
    {user_query}

    Responde SOLO:
    mentor
    o
    jira
    """

    response = modelo_orquestador.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    decision = response.content.strip().lower()

    return {
        "next_agent": decision
    }