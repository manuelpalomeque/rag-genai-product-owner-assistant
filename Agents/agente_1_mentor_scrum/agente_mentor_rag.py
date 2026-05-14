from dotenv import load_dotenv
load_dotenv()

from Agents.agente_1_mentor_scrum.chains import (
    construir_mentor_chain
)


class MentorAgent:

    def __init__(self):

        self.chain = construir_mentor_chain()

    def invoke(self, query: str) -> str:

        response = self.chain.invoke(
            {
                "question": query
            }
        )

        return response


mentor_agent = MentorAgent()