from agents.agent import create_agent
from utils.logging import setup_logging

def main():
    setup_logging()
    agent = create_agent('summarization')
    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break
        response = agent.work(prompt)
        print(response)

if __name__ == "__main__":
    main()
