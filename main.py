# main.py

from agent import call_groq_agent

def main():
    print("TaskTrek Agent (Groq - Phase 1)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Task: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            output = call_groq_agent(user_input)
            print("Agent:", output, "\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()