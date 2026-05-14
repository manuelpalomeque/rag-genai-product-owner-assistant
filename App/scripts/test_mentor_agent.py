
from dotenv import load_dotenv
load_dotenv()

from Agents.agente_1_mentor_scrum.agente_mentor_rag import MentorAgent


def main():
    agent = MentorAgent()
    question = (
        "Que son los artefactos Scrum?"
    )
    response = agent.ask(question)
    print("\nRESPUESTA:\n")
    print(response)


if __name__ == "__main__":
    main()