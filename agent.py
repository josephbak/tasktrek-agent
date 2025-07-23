# agent.py

import requests
import os
import re
from dotenv import load_dotenv
from tools import calculate

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or None
if GROQ_API_KEY is None:
    print("Error: Please set your GROQ_API_KEY in the .env file")
    exit(1)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def extract_calculation_command(text):
    match = re.search(r'calculate\((.*?)\)', text)
    return match.group(1) if match else None


def call_groq_agent(message_history):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": message_history,
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")

    reply = response.json()['choices'][0]['message']['content'].strip()

    # If model calls a tool like calculate(x), run it
    expr = extract_calculation_command(reply)
    if expr:
        result = calculate(expr)
        # Add tool output to history for agent to continue
        message_history.append({"role": "assistant", "content": reply})
        message_history.append({"role": "user", "content": f"Observation: {result}"})

        # Follow-up call with tool result
        return call_groq_agent(message_history)
    
    return reply