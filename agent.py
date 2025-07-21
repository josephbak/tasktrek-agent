# agent.py

import requests
import os
from dotenv import load_dotenv

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

def call_groq_agent(message_history):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": message_history,
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content.strip()
    else:
        raise Exception(f"Groq API error {response.status_code}: {response.text}")