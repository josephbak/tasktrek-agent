# planner.py
import json
from datetime import datetime
from typing import List, Dict, Optional
from tools import function_defs

class SmartTaskPlanner:
    def __init__(self, agent):
        self.agent = agent
        self.current_plan = []
        self.completed_steps = []
        self.current_step_index = 0
        self.plan_goal = ""
        
        # Phase 1: Start with basic mode
        self.use_basic_mode = True
        self.planning_history = []
    
    def get_available_tools(self) -> List[str]:
        """Dynamically extract tools from function_defs"""
        return [
            f"{tool_def['function']['name']} - {tool_def['function']['description']}"
            for tool_def in function_defs
        ]
    
    def get_tool_names(self) -> List[str]:
        """Get just the tool names for validation"""
        return [tool_def["function"]["name"] for tool_def in function_defs]
    
    def should_create_plan(self, user_request: str) -> bool:
        """Hybrid approach: LLM decision with heuristic fallback"""
        # Start with conservative heuristic-only approach
        return self._heuristic_complexity_check(user_request)
        
        # TODO: Re-enable LLM complexity check after more testing
        # try:
        #     return self._llm_complexity_check(user_request)
        # except Exception as e:
        #     print(f"[PLANNER] LLM complexity check failed: {e}")
        #     return self._heuristic_complexity_check(user_request)
    
    def _llm_complexity_check(self, user_request: str) -> bool:
        """LLM-based complexity detection"""
        prompt = f"""Analyze if this request needs multi-step planning or can be handled as a single action.

User Request: "{user_request}"

Available Tools: {', '.join(self.get_tool_names())}

Reply with ONLY "COMPLEX" or "SIMPLE"

COMPLEX if:
- Multiple tools needed
- Analysis of multiple items ("all files", "each", "compare")
- Research and synthesis ("search and summarize", "analyze and report")
- Sequential dependencies ("first do X, then Y")

SIMPLE if:
- Single tool call
- One clear action
- Straightforward question
- Direct calculation or lookup

Examples:
"What's 2+2?" → SIMPLE
"List all Python files and analyze their structure" → COMPLEX
"Get weather for Tokyo" → SIMPLE
"Research AI trends and create summary" → COMPLEX"""

        response = self.agent._call_llm_for_planning(prompt)
        decision = "COMPLEX" in response.strip().upper()
        
        # Store for learning (future enhancement)
        self.planning_history.append({
            "request": user_request,
            "decision": decision,
            "method": "llm",
            "timestamp": datetime.now()
        })
        
        return decision
    
    def _heuristic_complexity_check(self, user_request: str) -> bool:
        """Fallback heuristic complexity detection"""
        tool_names = self.get_tool_names()
        request_lower = user_request.lower()
        
        # Count mentioned tools
        mentioned_tools = sum(1 for tool in tool_names if tool in request_lower)
        
        # Check for complexity indicators
        complexity_signals = [
            mentioned_tools >= 2,  # Multiple tools mentioned
            len(user_request.split()) > 15,  # Long request
            any(word in request_lower for word in [
                "and then", "after", "all", "each", "every", "analyze", 
                "compare", "summarize", "research", "create report"
            ]),
            any(word in request_lower for word in ["and", "also", "plus"]) and mentioned_tools >= 1
        ]
        
        decision = any(complexity_signals)
        
        # Store for learning
        self.planning_history.append({
            "request": user_request,
            "decision": decision,
            "method": "heuristic",
            "timestamp": datetime.now()
        })
        
        return decision
    
    def create_plan(self, user_request: str) -> Optional[Dict]:
        """Generate a structured plan using LLM with validation"""
        if not self.should_create_plan(user_request):
            return None
        
        planning_prompt = f"""You are a task planning assistant. Break down this user request into a clear, step-by-step plan.

User Request: "{user_request}"

Available Tools:
{chr(10).join(self.get_available_tools())}

Create a JSON plan with this EXACT structure:
{{
    "goal": "Clear description of the main objective",
    "steps": [
        {{
            "step": 1,
            "description": "Clear, actionable description of what to do",
            "tool_needed": "exact_tool_name or null",
            "expected_output": "what we expect to get from this step"
        }},
        {{
            "step": 2,
            "description": "Next action to take",
            "tool_needed": "exact_tool_name or null", 
            "expected_output": "what we expect to get from this step"
        }}
    ]
}}

Rules:
- Use EXACT tool names from the available tools list
- If no tool is needed for a step (like analysis/synthesis), use null
- Keep descriptions clear and actionable
- Aim for 2-6 steps maximum
- Each step should build logically on previous steps
- Focus on the essential steps only

Return ONLY the JSON, no other text."""

        try:
            response = self.agent._call_llm_for_planning(planning_prompt)
            
            # Clean response (remove any markdown formatting)
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            clean_response = clean_response.strip()
            
            plan = json.loads(clean_response)
            
            # Validate plan structure
            if not self._validate_plan(plan):
                print("[PLANNER] Plan validation failed")
                return None
                
            self.current_plan = plan["steps"]
            self.plan_goal = plan["goal"]
            self.current_step_index = 0
            self.completed_steps = []
            
            return plan
            
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"[PLANNER] Planning failed: {e}")
            return None
    
    def _validate_plan(self, plan: Dict) -> bool:
        """Validate plan structure and tool names"""
        # Check required keys
        if not all(key in plan for key in ["goal", "steps"]):
            return False
        
        if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
            return False
        
        # Validate each step
        valid_tool_names = self.get_tool_names() + [None, "null"]
        
        for step in plan["steps"]:
            # Check step structure
            required_keys = ["step", "description", "tool_needed", "expected_output"]
            if not all(key in step for key in required_keys):
                return False
            
            # Validate tool name
            tool_needed = step["tool_needed"]
            if tool_needed not in valid_tool_names and tool_needed != "null":
                print(f"[PLANNER] Invalid tool name: {tool_needed}")
                return False
        
        return True
    
    def get_next_step(self) -> Optional[Dict]:
        """Get the next step to execute"""
        if self.current_step_index < len(self.current_plan):
            return self.current_plan[self.current_step_index]
        return None
    
    def mark_step_complete(self, step_result: str):
        """Mark current step as complete and move to next"""
        if self.current_step_index < len(self.current_plan):
            completed_step = {
                "step": self.current_step_index + 1,
                "description": self.current_plan[self.current_step_index]["description"],
                "result": step_result,
                "completed_at": datetime.now().isoformat()
            }
            self.completed_steps.append(completed_step)
            self.current_step_index += 1
    
    def is_plan_complete(self) -> bool:
        """Check if all steps are completed"""
        return self.current_step_index >= len(self.current_plan)
    
    def get_plan_status(self) -> Dict:
        """Get current plan progress"""
        return {
            "goal": self.plan_goal,
            "total_steps": len(self.current_plan),
            "completed_steps": len(self.completed_steps),
            "current_step": self.current_step_index + 1 if not self.is_plan_complete() else len(self.current_plan),
            "progress": f"{len(self.completed_steps)}/{len(self.current_plan)}"
        }
    
    def reset_plan(self):
        """Reset planner state"""
        self.current_plan = []
        self.completed_steps = []
        self.current_step_index = 0
        self.plan_goal = ""
    
    def get_planning_stats(self) -> Dict:
        """Get statistics about planning decisions (for debugging)"""
        if not self.planning_history:
            return {"total": 0, "llm_decisions": 0, "heuristic_decisions": 0}
        
        total = len(self.planning_history)
        llm_count = sum(1 for item in self.planning_history if item["method"] == "llm")
        heuristic_count = sum(1 for item in self.planning_history if item["method"] == "heuristic")
        
        return {
            "total": total,
            "llm_decisions": llm_count,
            "heuristic_decisions": heuristic_count,
            "llm_success_rate": f"{(llm_count/total)*100:.1f}%" if total > 0 else "0%"
        }