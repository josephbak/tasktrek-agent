# TaskTrek Agent

An intelligent command-line AI agent powered by Groq's Llama 3.3 model with conversation memory, tool integration, and intelligent task planning capabilities.

## Features

- **Interactive Chat Interface** - Seamless conversation experience with memory persistence
- **Intelligent Task Planning** - Automatically breaks down complex requests into structured, multi-step plans
- **Hybrid Planning System** - LLM-based complexity detection with heuristic fallbacks for reliability
- **Tool Integration** - Function calling capabilities for enhanced problem-solving across 12 specialized tools
- **Mathematical Calculations** - Built-in calculator tool for precise arithmetic operations
- **Date/Time Operations** - Current time retrieval and date calculations
- **Text Processing** - Word, character, and line counting for content analysis
- **Web Integration** - Search capabilities, weather information, and webpage content extraction
- **File System Operations** - Directory listing, file reading, and file information retrieval
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

### Web Operations
```
Task: Search for information about artificial intelligence
[TOOL] Using 1 tool(s):
[TOOL] → web_search({"query": "artificial intelligence"})
[TOOL] ← web_search result: Definition of artificial intelligence: The simulation of human intelligence...
Agent: Artificial intelligence (AI) refers to the simulation of human intelligence in machines...

Task: What's the weather in Tokyo?
[TOOL] Using 1 tool(s):
[TOOL] → get_weather({"city": "Tokyo"})
[TOOL] ← get_weather result: Weather in Tokyo: Partly cloudy, 18°C (64°F), Humidity: 72%
Agent: The current weather in Tokyo is partly cloudy with a temperature of 18°C (64°F) and 72% humidity.
```

### Intelligent Task Planning
```
Task: List all Python files and analyze their structure
[PLAN] Created plan: Analyze Python project structure
📋 Plan: Analyze Python project structure
📝 Steps (3):
   1. List all files in current directory [list_files]
   2. Filter and identify Python files [null]
   3. Read and analyze each Python file [read_file]

🔄 Step 1/3: List all files in current directory
[TOOL] Using 1 tool(s):
[TOOL] → list_files({"directory": "."})
[TOOL] ← list_files result: Contents of '.': 📄 main.py (2KB), 📄 agent.py (5KB), 📄 tools.py (8KB)...
✅ Step 1 complete

🔄 Step 2/3: Filter and identify Python files
[LLM] Responding directly without tools
✅ Step 2 complete

🔄 Step 3/3: Read and analyze each Python file
[TOOL] Using 1 tool(s):
[TOOL] → read_file({"filename": "main.py"})
[TOOL] ← read_file result: Content of 'main.py': # main.py...
✅ Step 3 complete

Agent: Based on the analysis, your Python project has a clean structure with 3 main files...
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

TaskTrek follows a clean, modular architecture with separated concerns and intelligent task planning:

```
├── main.py          # Entry point - environment setup and chat loop
├── agent.py         # TaskTrekAgent class - manages chat flow, planning, tool calling, memory
├── planner.py       # SmartTaskPlanner class - intelligent task planning and complexity detection
├── memory.py        # Memory class - conversation context management
├── tools.py         # Tool system - function schemas, implementations, and dispatch logic
├── .env            # API key configuration (excluded from git)
├── requirements.txt # Python dependencies
└── README.md       # Documentation
```

### Component Responsibilities

- **main.py**: Application entry point, initializes agent and manages user interaction loop
- **agent.py**: Core agent logic with planning integration, function calling, memory management, and error handling
- **planner.py**: Intelligent task planning system with hybrid complexity detection and plan execution
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

### Web Tools
- **Function**: `web_search(query)`
- **Purpose**: Search the web using DuckDuckGo Instant Answer API
- **Best for**: Definitions, facts, calculations, reference queries
- **Example**: `web_search("What is Python programming")` → Returns definition and overview

- **Function**: `get_weather(city)`
- **Purpose**: Get current weather information for any city
- **API**: wttr.in (free, no API key required)
- **Example**: `get_weather("London")` → `Weather in London: Clear, 15°C (59°F), Humidity: 65%`

- **Function**: `url_content(url)`
- **Purpose**: Fetch and summarize webpage content
- **Returns**: First 500 characters of text content
- **Example**: `url_content("https://example.com")` → Text summary of the webpage

### Adding New Tools
To extend TaskTrek with additional tools:

1. Add function definition to `function_defs` in `tools.py`
2. Implement the tool function
3. Add dispatch logic to `handle_tool_call()`

## Intelligent Planning System

TaskTrek features a sophisticated planning system that automatically determines when complex requests need multi-step execution:

### **Automatic Complexity Detection**
- **LLM-based analysis**: Uses Groq's Llama model to intelligently assess task complexity
- **Heuristic fallback**: Reliable backup system using pattern matching and keyword analysis
- **Dynamic tool discovery**: Automatically stays synchronized with available tools

### **Plan Generation**
- **Structured breakdown**: Complex tasks are decomposed into clear, sequential steps
- **Tool optimization**: Each step specifies the optimal tool for execution
- **Validation system**: Plans are validated for correctness and tool availability

### **Execution Monitoring**
- **Progress tracking**: Real-time feedback on plan execution progress
- **Step-by-step visibility**: Clear indication of current step and completion status
- **Error handling**: Graceful handling of step failures with detailed error reporting

### **Examples of Planning Triggers**
- **Multi-tool requests**: "Get weather for Tokyo and calculate days until New Year"
- **Analysis tasks**: "Analyze all Python files in my project"
- **Research workflows**: "Search for AI trends and create a summary report"
- **File operations**: "List all files and read the important ones"

## Development Roadmap

### **Current Status: Phase 1 Complete**
- ✅ Hybrid planning system with LLM + heuristic complexity detection
- ✅ Structured plan generation and validation
- ✅ Multi-step task execution with progress tracking
- ✅ 12 specialized tools across 5 categories

### **Phase 2: ReAct Integration (In Progress)**
- 🔄 Add ReAct (Reasoning and Acting) pattern to each planned step
- 🔄 Enhanced step-by-step reasoning visibility
- 🔄 Improved tool selection with explicit thought processes
- 🔄 Better error recovery and plan adaptation

### **Phase 3: Advanced Features (Planned)**
- 📋 Dynamic plan modification based on step results
- 📋 Learning system for improved complexity detection
- 📋 Performance optimization and caching
- 📋 Enhanced debugging and monitoring capabilities

## Monitoring

TaskTrek provides comprehensive real-time feedback on its decision-making process:

### **Planning Indicators**
- `[SIMPLE]` - Single-step task execution
- `[PLAN]` - Multi-step planned task execution
- `📋 Plan:` - Shows the overall goal and step breakdown
- `🔄 Step X/Y:` - Current step execution with progress

### **Tool Usage Indicators**
- `[TOOL]` - Indicates when and which tools are being used
- `[LLM]` - Shows when the agent responds directly without tools
- Tool arguments and results are displayed for transparency

### **Debug Commands**
- Type `debug` to see planning statistics and system performance
- Intelligent tool selection based on query context and planning analysis

## Requirements

- Python 3.7+
- Groq API key (free tier available)
- Internet connection for API calls and web tools
- No additional API keys required for web tools (uses free public APIs)

## Development

The codebase follows clean architecture principles with:
- Separation of concerns across modules
- Dependency injection for testability
- Error handling with retry mechanisms
- Extensible tool system

## License

MIT License