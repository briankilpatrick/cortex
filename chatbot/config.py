# chatbot/config.py

"""
Central configuration for the chatbot.

Change MODEL_NAME if you want to test a different Ollama model.
For example:
- llama2
- mistral
- mixtral
- codellama
"""

MODEL_NAME = "llama2"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# How long to wait before quitting if the user does not type anything
TIMEOUT_SECONDS = 60

# Log rotation settings
LOG_MAX_BYTES = 20 * 1024 * 1024  # 20 MB per file
LOG_BACKUP_COUNT = 5              # 5 files = approx 100 MB per log type
