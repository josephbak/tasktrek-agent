import json
from datetime import datetime

function_defs = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression like '2 + 3 * (4 ** 2)'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "days_between",
            "description": "Calculate the number of days between two dates",
            "parameters": {
                "type": "object",
                "properties": {
                    "date1": {
                        "type": "string",
                        "description": "First date in YYYY-MM-DD format"
                    },
                    "date2": {
                        "type": "string",
                        "description": "Second date in YYYY-MM-DD format"
                    }
                },
                "required": ["date1", "date2"]
            }
        }
    }
    # Add more tool definitions here
]

def calculate(expression: str) -> str:
    allowed_names = {
        "__builtins__": None,
        "abs": abs,
        "pow": pow,
        "round": round,
    }
    try:
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_current_time() -> str:
    """Get current date and time"""
    try:
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S (%A)")
    except Exception as e:
        return f"Error getting time: {e}"

def days_between(date1: str, date2: str) -> str:
    """Calculate days between two dates (YYYY-MM-DD format)"""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = abs((d2 - d1).days)
        return f"{diff} days between {date1} and {date2}"
    except Exception as e:
        return f"Error: {e}. Please use YYYY-MM-DD format (e.g., 2025-01-23)"

def handle_tool_call(tool_call):
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    
    if name == "calculate":
        return calculate(args["expression"])
    
    if name == "get_current_time":
        return get_current_time()
    
    if name == "days_between":
        return days_between(args["date1"], args["date2"])
    
    # Add dispatch for more tools here
    return f"Unknown tool: {name}"