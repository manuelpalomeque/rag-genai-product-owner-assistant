from dotenv import load_dotenv

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pprint import pprint

load_dotenv()

class OrchestratorState(TypedDict):

    messages: Annotated[
        Sequence[BaseMessage],
        add_messages
    ]

    next_agent: str

    final_response: str