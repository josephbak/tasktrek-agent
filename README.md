# TaskTrek Agent

An intelligent command-line AI agent powered by Groq's Llama 3.3 model with conversation memory and tool integration capabilities.

## Features

- **Interactive Chat Interface** - Seamless conversation experience with memory persistence
- **Tool Integration** - Function calling capabilities for enhanced problem-solving
- **Mathematical Calculations** - Built-in calculator tool for precise arithmetic operations
- **Conversation Memory** - Maintains context throughout the entire session
- **Retry Logic** - Robust error handling with automatic retry mechanisms
- **Real-time Tool Monitoring** - Visual indicators showing when tools vs. LLM responses are used
- **Clean Architecture** - Modular design with separated concerns for maintainability
- **Secure Configuration** - Environment variable-based API key management

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tasktrek-agent
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests python-dotenv
   ```
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   - Get your free API key from [Groq Console](https://console.groq.com/)
   - Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Usage

1. **Activate virtual environment** (if not already active)
   ```bash
   source venv/bin/activate
   ```

2. **Run the agent**
   ```bash
   python main.py
   ```

3. **Start chatting**
   - Type your tasks or questions
   - Type `exit` or `quit` to stop

## Example Usage

### Mathematical Calculations with Tools
```
TaskTrek Agent (Groq - Phase 3: Tool Integration)
Type 'exit' to quit.

Task: What is (8*7) + (2 ** 5)?
[TOOL] Using 1 tool(s):
[TOOL] → calculate({"expression": "(8*7) + (2 ** 5)"})
[TOOL] ← calculate result: 88
Agent: The result is 88.

Task: Can you explain how you calculated that?
[LLM] Responding directly without tools
Agent: I used the calculate tool to evaluate the expression (8*7) + (2 ** 5). 
First, 8*7 = 56, then 2**5 = 32, and finally 56 + 32 = 88.
```

### General Conversation
```
Task: Hello, what can you help me with?
[LLM] Responding directly without tools
Agent: Hello! I'm TaskTrek, an AI assistant that can help you with various tasks...

Task: exit
Goodbye!
```

## Architecture

TaskTrek follows a clean, modular architecture with separated concerns:

```
├── main.py          # Entry point - environment setup and chat loop
├── agent.py         # TaskTrekAgent class - manages chat flow, tool calling, memory, retries
├── memory.py        # Memory class - conversation context management
├── tools.py         # Tool system - function schemas, implementations, and dispatch logic
├── .env            # API key configuration (excluded from git)
├── requirements.txt # Python dependencies
└── README.md       # Documentation
```

### Component Responsibilities

- **main.py**: Application entry point, initializes agent and manages user interaction loop
- **agent.py**: Core agent logic with function calling, memory management, and error handling
- **memory.py**: Conversation history storage and retrieval
- **tools.py**: Tool definitions, implementations, and execution dispatch

## Available Tools

### Calculator Tool
- **Function**: `calculate(expression)`
- **Purpose**: Safely evaluates mathematical expressions
- **Supported Operations**: `+`, `-`, `*`, `/`, `**`, `()`, `abs()`, `pow()`, `round()`
- **Security**: Uses restricted `eval()` environment to prevent code injection

### Adding New Tools
To extend TaskTrek with additional tools:

1. Add function definition to `function_defs` in `tools.py`
2. Implement the tool function
3. Add dispatch logic to `handle_tool_call()`

## Monitoring

TaskTrek provides real-time feedback on its decision-making process:

- `[TOOL]` - Indicates when and which tools are being used
- `[LLM]` - Shows when the agent responds directly without tools
- Tool arguments and results are displayed for transparency

## Requirements

- Python 3.7+
- Groq API key (free tier available)
- Internet connection for API calls

## Development

The codebase follows clean architecture principles with:
- Separation of concerns across modules
- Dependency injection for testability
- Error handling with retry mechanisms
- Extensible tool system

## License

MIT License