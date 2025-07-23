import json

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

def handle_tool_call(tool_call):
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    
    if name == "calculate":
        return calculate(args["expression"])
    
    # Add dispatch for more tools here
    return f"Unknown tool: {name}"