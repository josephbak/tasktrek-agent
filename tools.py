# tools.py

def calculate(expression: str) -> str:
    """
    Safely evaluate a basic math expression.
    Supports +, -, *, /, **, parentheses.
    """
    try:
        # Limit the eval environment for safety
        allowed_names = {
            "__builtins__": None, # Removes access to dangerous functions
            "abs": abs,           # only allows specific safe functions
            "pow": pow
        }
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"