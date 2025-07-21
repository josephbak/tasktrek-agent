# main.py

from agent import call_groq_agent
from memory import Memory

def main():
    print("TaskTrek Agent (Groq - Phase 2: Memory Enabled)")
    print("Type 'exit' to quit.\n")

    memory = Memory(system_prompt="You are TaskTrek, a helpful AI agent that assists users in solving tasks.")

    while True:
        user_input = input("Task: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        memory.add_user_message(user_input)

        try:
            response = call_groq_agent(memory.get_history())
            memory.add_agent_message(response)
            print("Agent:", response, "\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()