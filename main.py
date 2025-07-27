# main.py

from agent import TaskTrekAgent

def main():
    print("TaskTrek Agent (Groq - Phase 3: Tool Integration)")
    print("Type 'exit' to quit.\n")

    agent = TaskTrekAgent()

    while True:
        user_input = input("Task: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            # Show session info before exiting
            print(f"Session saved to: {agent.memory.current_session_file}")
            print("Goodbye!")
            break
        
        # Memory debug commands
        if user_input.strip().lower() == "memory":
            stats = agent.memory.get_memory_stats()
            print(f"Memory Stats: {stats}")
            continue
        elif user_input.strip().lower() == "important":
            summary = agent.memory.get_important_summary()
            print("Important Messages:")
            for item in summary:
                print(f"  {item['reason']}: {item['preview']}")
            continue
        elif user_input.strip().lower() == "session":
            print(f"Current session file: {agent.memory.current_session_file}")
            continue
        
        try:
            response = agent.chat(user_input)
            print("Agent:", response, "\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()