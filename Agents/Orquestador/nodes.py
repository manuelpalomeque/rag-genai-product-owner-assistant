from dotenv import load_dotenv

from pprint import pprint
from Agents.agente_1_mentor_scrum.agente_mentor_rag import mentor_agent
from Agents.agente_2_jira.agente_jira import jira_agent

load_dotenv()

def mentor_node(state):

    query = state["messages"][-1].content

    response = mentor_agent.invoke(query)

    return {
        "final_response": response
    }


def jira_node(state):

    query = state["messages"][-1].content

    response =jira_agent.invoke(query)

    return {
        "final_response": response
    }