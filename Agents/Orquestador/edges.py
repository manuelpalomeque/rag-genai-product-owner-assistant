from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory  import InMemorySaver
from pprint import pprint
from Config.modelos import definir_modelo_groq
from Agents.agente_1_mentor_scrum import agente_mentor_rag
from Agents.agente_2_jira import agente_jira


load_dotenv()

def route_decision(state):
    return state["next_agent"]