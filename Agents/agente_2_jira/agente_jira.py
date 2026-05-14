from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

from Tools.tools import crear_issue_en_backlog, get_issues_by_label
from Prompts.prompt_agente_2_Jira import jira_system_prompt
from Config.modelos import (
    definir_modelo_google_flash,
    definir_modelo_groq
)


class JiraAgent:

    def __init__(self):

        self.tools = [crear_issue_en_backlog, get_issues_by_label]

        self.agent = create_agent(
            #model=definir_modelo_google_flash(),
            model = definir_modelo_groq(),
            tools=self.tools,
            system_prompt=jira_system_prompt,
            checkpointer=InMemorySaver()
        )

        self.config = {
            "configurable": {
                "thread_id": "jira-thread"
            }
        }

    def invoke(self, query: str) -> str:

        response = self.agent.invoke(
            {
                "messages": [
                    HumanMessage(content=query)
                ]
            },
            config=self.config
        )

        last_message = response["messages"][-1]

        if hasattr(last_message, "content"):

            content = last_message.content

            if isinstance(content, str):
                return content

            if isinstance(content, list):

                if (
                    len(content) > 0
                    and isinstance(content[0], dict)
                    and "text" in content[0]
                ):
                    return content[0]["text"]

            return str(content)

        return str(last_message)


jira_agent = JiraAgent()