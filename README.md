# TaskTrek Agent

An intelligent command-line AI agent powered by Groq's Llama 3.3 model with conversation memory and tool integration capabilities.

## Features

- **Interactive Chat Interface** - Seamless conversation experience with memory persistence
- **Tool Integration** - Function calling capabilities for enhanced problem-solving
- **Mathematical Calculations** - Built-in calculator tool for precise arithmetic operations
- **Date/Time Operations** - Current time retrieval and date calculations
- **Text Processing** - Word, character, and line counting for content analysis
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

### Mathematical Calculations
```
TaskTrek Agent (Groq - Phase 3: Tool Integration)
Type 'exit' to quit.

Task: What is (8*7) + (2 ** 5)?
[TOOL] Using 1 tool(s):
[TOOL] → calculate({"expression": "(8*7) + (2 ** 5)"})
[TOOL] ← calculate result: 88
Agent: The result is 88.
```

### Date/Time Operations
```
Task: What time is it?
[TOOL] Using 1 tool(s):
[TOOL] → get_current_time({})
[TOOL] ← get_current_time result: 2025-01-23 14:30:45 (Thursday)
Agent: It's currently 2:30 PM on Thursday, January 23rd, 2025.

Task: How many days between 2025-01-01 and 2025-12-31?
[TOOL] Using 1 tool(s):
[TOOL] → days_between({"date1": "2025-01-01", "date2": "2025-12-31"})
[TOOL] ← days_between result: 364 days between 2025-01-01 and 2025-12-31
Agent: There are 364 days between January 1st and December 31st, 2025.
```

### Text Processing
```
Task: How many words are in "Hello world this is a test"?
[TOOL] Using 1 tool(s):
[TOOL] → count_words({"text": "Hello world this is a test"})
[TOOL] ← count_words result: 6 words
Agent: There are 6 words in that text.

Task: Count characters and lines in "Hello\nWorld"
[TOOL] Using 1 tool(s):
[TOOL] → count_characters({"text": "Hello\nWorld"})
[TOOL] ← count_characters result: 11 characters
Agent: The text has 11 characters (including the newline).
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

### Data Flow
```
[User Query] ──▶ [Memory Storage] ──▶ [Agent Processing]
                                           │
                                           ▼
                                    [Tool Decision]
                                           │
                              ┌────────────┴────────────┐
                              ▼                         ▼
                        [Use Tools]              [Direct LLM]
                              │                         │
                              ▼                         │
                      [Tool Execution]                  │
                              │                         │
                              └─────────┬───────────────┘
                                        ▼
                                 [Final Response]
                                        │
                                        ▼
                                [Memory Update]
```

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

### Mathematical Tool
- **Function**: `calculate(expression)`
- **Purpose**: Safely evaluates mathematical expressions
- **Supported Operations**: `+`, `-`, `*`, `/`, `**`, `()`, `abs()`, `pow()`, `round()`
- **Security**: Uses restricted `eval()` environment to prevent code injection

### Date/Time Tools
- **Function**: `get_current_time()`
- **Purpose**: Returns current date and time
- **Format**: `YYYY-MM-DD HH:MM:SS (Day)`
- **Example**: `2025-01-23 14:30:45 (Thursday)`

- **Function**: `days_between(date1, date2)`
- **Purpose**: Calculates days between two dates
- **Format**: Both dates in `YYYY-MM-DD` format
- **Example**: `days_between("2025-01-01", "2025-12-31")` → `365 days between 2025-01-01 and 2025-12-31`

### Text Processing Tools
- **Function**: `count_words(text)`
- **Purpose**: Count the number of words in text
- **Example**: `count_words("Hello world")` → `2 words`

- **Function**: `count_characters(text)`
- **Purpose**: Count the number of characters in text (including spaces)
- **Example**: `count_characters("Hello world")` → `11 characters`

- **Function**: `count_lines(text)`
- **Purpose**: Count the number of lines in text
- **Example**: `count_lines("Line 1\nLine 2")` → `2 lines`

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
- Intelligent tool selection based on query context (calculations vs. concepts)

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