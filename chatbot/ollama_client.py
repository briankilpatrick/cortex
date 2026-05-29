# chatbot/ollama_client.py

# Import requests so we can call the local Ollama API
import requests

# Import configuration values
from chatbot.config import MODEL_NAME, OLLAMA_API_URL


def query_ollama(prompt: str) -> str:
    """
    Sends a prompt to the local Ollama API and returns the response text.

    This uses the local Ollama server, normally running at:
    http://localhost:11434

    The model must already be pulled locally, for example:
    ollama pull llama2
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "[No response from Ollama]")
