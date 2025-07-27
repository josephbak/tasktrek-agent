# agent.py

import requests
import os
import json
from dotenv import load_dotenv
from memory import Memory
from tools import function_defs, handle_tool_call

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or None
if GROQ_API_KEY is None:
    print("Error: Please set your GROQ_API_KEY in the .env file")
    exit(1)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class TaskTrekAgent:
    def __init__(self):
        # System prompt ready for ReAct enhancement
        self.memory = Memory(
            system_prompt="""You are TaskTrek, a helpful AI agent that assists users in solving tasks. Use available tools when needed.

Tool Usage Guidelines:
- Use calculate() ONLY when the user asks for a specific calculation or mathematical computation
- Use get_current_time() when asked about current time, date, "now", "today", etc.
- Use days_between() for specific date difference calculations
- Respond directly for explanations, definitions, concepts, or general knowledge

Examples:
- "what's 2+2?" → use calculate("2+2")
- "calculate 5 to the power of 3" → use calculate("5**3")
- "what's power in math?" → explain directly, optionally show example with calculate
- "what is electrical power?" → explain directly (concept/definition)
- "what time is it?" → use get_current_time()"""
        )
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.max_retries = 3

    def chat(self, user_input):
        """Main chat method - ready for ReAct enhancement"""
        self.memory.add_user_message(user_input)
        
        # Execute task (ready to be enhanced with ReAct pattern)
        return self._execute_task()
    
    def _execute_task(self):
        """Execute task - structured for easy ReAct integration"""
        for attempt in range(self.max_retries):
            try:
                # This is where ReAct reasoning will be added:
                # 1. Thought: Analyze what needs to be done
                # 2. Action: Use tools or respond directly  
                # 3. Observation: Review results
                # 4. Answer: Provide final response
                
                response = self._call_groq_with_tools()
                
                # Handle tool calls if present
                if self._has_tool_calls(response):
                    tool_response = self._handle_tool_calls(response)
                    self.memory.add_agent_message(tool_response)
                    return tool_response
                else:
                    print("[LLM] Responding directly without tools")
                    content = response['choices'][0]['message']['content']
                    self.memory.add_agent_message(content)
                    return content
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")
    
    # Planning methods removed - ready for ReAct implementation
        
    def _call_groq_with_tools(self):
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": self.memory.get_history(),
            "temperature": 0.7,
            "tools": function_defs,
            "tool_choice": "auto"
        }

        response = requests.post(GROQ_API_URL, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Groq API error {response.status_code}: {response.text}")
            
        return response.json()

    def _has_tool_calls(self, response):
        message = response['choices'][0]['message']
        return 'tool_calls' in message and message['tool_calls']

    def _handle_tool_calls(self, response):
        message = response['choices'][0]['message']
        tool_calls = message['tool_calls']
        
        # Show which tools are being called
        print(f"[TOOL] Using {len(tool_calls)} tool(s):")
        for tool_call in tool_calls:
            tool_name = tool_call['function']['name']
            tool_args = tool_call['function']['arguments']
            print(f"[TOOL] → {tool_name}({tool_args})")
        
        # Execute each tool call and collect results
        tool_results = []
        for tool_call in tool_calls:
            result = handle_tool_call(tool_call)
            tool_name = tool_call['function']['name']
            print(f"[TOOL] ← {tool_name} result: {result}")
            tool_results.append(f"{tool_name}: {result}")
        
        # Create a summary of tool usage for memory
        tool_summary = f"[TOOL] Used {len(tool_calls)} tool(s): " + "; ".join(tool_results)
        
        # Get final response after tool execution
        final_response = self._call_groq_with_tools()
        final_content = final_response['choices'][0]['message']['content']
        
        # Combine tool summary with final response for memory
        combined_response = f"{tool_summary}\n{final_content}"
        return combined_response
    
    # Helper methods for future ReAct implementation
    
    def _make_llm_call(self, messages, temperature=0.7):
        """Generic LLM call - useful for ReAct reasoning steps"""
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(GROQ_API_URL, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"LLM API error {response.status_code}: {response.text}")
        
        return response.json()['choices'][0]['message']['content']