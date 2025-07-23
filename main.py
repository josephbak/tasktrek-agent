# main.py

from agent import TaskTrekAgent

def main():
    print("TaskTrek Agent (Groq - Phase 3: Tool Integration)")
    print("Type 'exit' to quit.\n")

    agent = TaskTrekAgent()

    while True:
        user_input = input("Task: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        try:
            response = agent.chat(user_input)
            print("Agent:", response, "\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()