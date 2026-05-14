from dotenv import load_dotenv

from pprint import pprint


from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import (
    InMemorySaver
)

from Agents.Orquestador.state import OrchestratorState
from Agents.Orquestador.router import router_node
from Agents.Orquestador.nodes import mentor_node, jira_node
from Agents.Orquestador.edges import route_decision

load_dotenv()

workflow = StateGraph(OrchestratorState)


# Nodes
workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "mentor",
    mentor_node
)

workflow.add_node(
    "jira",
    jira_node
)

# Entry
workflow.set_entry_point("router")

# Conditional routing
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "mentor": "mentor",
        "jira": "jira",
    }
)

# Finish
workflow.add_edge("mentor", END)
workflow.add_edge("jira", END)


graph = workflow.compile(
)