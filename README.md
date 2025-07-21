# TaskTrek Agent

A simple command-line AI agent powered by Groq's Llama 3.3 model with conversation memory.

## Features

- Interactive chat interface with memory
- Powered by Groq API
- Remembers conversation context throughout the session
- Clean command-line experience
- Environment variable configuration

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

## Example

```
TaskTrek Agent (Groq - Phase 2: Memory Enabled)
Type 'exit' to quit.

Task: Write a Python function to calculate fibonacci numbers
Agent: Here's a Python function to calculate Fibonacci numbers...

Task: Can you optimize that function?
Agent: Sure! I can optimize the Fibonacci function I just showed you by using memoization...

Task: exit
Goodbye!
```

## Project Structure

```
├── main.py          # Main CLI interface with memory management
├── agent.py         # Groq API integration
├── memory.py        # Conversation memory handling
├── .env            # API key (not in git)
├── requirements.txt # Dependencies
└── README.md       # This file
```

## Requirements

- Python 3.7+
- Groq API key (free tier available)
- Internet connection

## License

MIT License