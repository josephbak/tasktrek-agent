# memory.py

class Memory:
    def __init__(self, system_prompt):
        self.history = [{"role": "system", "content": system_prompt}]

    def add_user_message(self, content):
        self.history.append({"role": "user", "content": content})

    def add_agent_message(self, content):
        self.history.append({"role": "assistant", "content": content})

    def get_history(self):
        return self.history
