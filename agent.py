# agent.py

import requests
import os
import json
from dotenv import load_dotenv
from memory import Memory
from tools import function_defs, handle_tool_call
from planner import SmartTaskPlanner

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or None
if GROQ_API_KEY is None:
    print("Error: Please set your GROQ_API_KEY in the .env file")
    exit(1)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class TaskTrekAgent:
    def __init__(self):
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
        
        # Initialize the hybrid planner
        self.planner = SmartTaskPlanner(self)

    def chat(self, user_input):
        """Enhanced chat with hybrid planning capability"""
        self.memory.add_user_message(user_input)
        
        # Step 1: Try to create a plan using hybrid approach
        plan = self.planner.create_plan(user_input)
        
        if plan is None:
            # Simple task - use existing single-step execution
            print("[SIMPLE] Executing as single task")
            return self._execute_simple_task()
        else:
            # Complex task - use planned execution  
            print(f"[PLAN] Created plan: {plan['goal']}")
            return self._execute_planned_task(plan)
    
    def _execute_simple_task(self):
        """Execute simple task using existing functionality"""
        for attempt in range(self.max_retries):
            try:
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
    
    def _execute_planned_task(self, plan):
        """Execute a multi-step plan"""
        print(f"📋 Plan: {plan['goal']}")
        print(f"📝 Steps ({len(plan['steps'])}):")
        for i, step in enumerate(plan['steps'], 1):
            tool_info = f" [{step['tool_needed']}]" if step['tool_needed'] and step['tool_needed'] != 'null' else ""
            print(f"   {i}. {step['description']}{tool_info}")
        print()
        
        final_results = []
        
        while not self.planner.is_plan_complete():
            current_step = self.planner.get_next_step()
            status = self.planner.get_plan_status()
            
            print(f"🔄 Step {current_step['step']}/{status['total_steps']}: {current_step['description']}")
            
            # Execute this step (Phase 1: using existing system, Phase 2: will add ReAct)
            step_result = self._execute_planned_step(current_step)
            
            # Mark step complete
            self.planner.mark_step_complete(step_result)
            final_results.append(step_result)
            
            print(f"✅ Step {current_step['step']} complete\n")
        
        # Synthesize final answer
        return self._synthesize_final_answer(plan, final_results)
    
    def _execute_planned_step(self, step):
        """Execute a single planned step (Phase 1: basic, Phase 2: will add ReAct)"""
        # Create step-specific context
        step_context = f"Execute this planned step: {step['description']}"
        if step['tool_needed'] and step['tool_needed'] != 'null':
            step_context += f" (Expected tool: {step['tool_needed']})"
        
        # Add step context to memory temporarily for this execution
        original_messages = self.memory.get_history().copy()
        self.memory.add_user_message(step_context)
        
        try:
            # Execute using existing system
            result = self._execute_simple_task()
            
            # Restore original memory state (remove step context)
            self.memory.history = original_messages
            
            return result
            
        except Exception as e:
            # Restore memory state on error
            self.memory.history = original_messages
            return f"Error executing step: {e}"
    
    def _synthesize_final_answer(self, plan, results):
        """Create final answer from plan results"""
        synthesis_prompt = f"""Based on the completed plan and step results, provide a comprehensive final answer.

Original Goal: {plan['goal']}

Step Results:
{chr(10).join([f"Step {i+1}: {result}" for i, result in enumerate(results)])}

Provide a clear, organized final answer that:
1. Addresses the original goal
2. Synthesizes information from all steps
3. Presents results in a logical, easy-to-understand format
4. Highlights key findings or conclusions

Be concise but comprehensive."""

        try:
            final_response = self._call_llm_for_planning(synthesis_prompt)
            self.memory.add_agent_message(final_response)
            return final_response
        except Exception as e:
            # Fallback to simple concatenation
            fallback = f"Completed plan: {plan['goal']}\n\nResults:\n" + "\n".join([f"• {result}" for result in results])
            self.memory.add_agent_message(fallback)
            return fallback
        
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
        
        # Add the assistant message with tool calls to memory (need to add the full message object)
        self.memory.history.append({
            "role": "assistant",
            "content": message.get('content', ''),
            "tool_calls": tool_calls
        })
        
        # Execute each tool call
        for tool_call in tool_calls:
            result = handle_tool_call(tool_call)
            tool_name = tool_call['function']['name']
            print(f"[TOOL] ← {tool_name} result: {result}")
            
            # Add tool result to memory
            self.memory.history.append({
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": result
            })
        
        # Get final response after tool execution
        final_response = self._call_groq_with_tools()
        return final_response['choices'][0]['message']['content']
    
    def _call_llm_for_planning(self, prompt: str) -> str:
        """Make LLM call specifically for planning with optimized settings"""
        messages = [
            {"role": "system", "content": "You are a task planning assistant. Be precise and follow instructions exactly."},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.1,  # Lower temperature for more consistent planning
            "max_tokens": 1000
        }
        
        response = requests.post(GROQ_API_URL, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Planning API error {response.status_code}: {response.text}")
        
        return response.json()['choices'][0]['message']['content']