# Cortex Chatbot

A private AI chatbot built in Python using Ollama and a local LLaMA model.

This project was built as a learning project and as the basis of a small local chatbot that can later be expanded with context files, web scraping, better logging, model switching, and packaging.

The chatbot currently:
- Runs locally using Ollama
- Uses a local model such as `llama2`
- Maintains conversation memory during the current session only
- Automatically exits after a timeout
- Logs system errors, session audit events, and chat history separately

---

## Prerequisites

Before running the Cortex Chatbot, ensure the following are installed and configured:

1. **Python 3.9+**

   Verify Python is installed:

   ```bash
   python3 --version
   ```

2. **Ollama CLI**

   Install Ollama from https://ollama.com or via Homebrew on macOS:

   ```bash
   brew install ollama
   ```

3. **Ollama Model**

   Pull the model you want to use, for example LLaMA2:

   ```bash
   ollama pull llama2
   ```

   Ensure the model is available locally before running the chatbot:

   ```bash
   ollama list
   ```

4. **Ollama Server Running**

   Make sure the Ollama server is running locally to respond to chatbot requests:

   ```bash
   ollama serve
   ```

   Or run a model directly:

   ```bash
   ollama run llama2
   ```

   The chatbot expects the Ollama API at:

   ```text
   http://localhost:11434
   ```

5. **Virtual Environment Recommended**

   Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

6. **Install Python Dependencies**

   Install required packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Project Structure

```text
cortex/
├─ README.md                  # Project overview, usage, logging, and roadmap
├─ requirements.txt           # Python dependencies
├─ .gitignore                 # Files and folders excluded from Git
├─ chatbot/                   # Main Python package
│  ├─ __init__.py
│  ├─ main.py                 # Entrypoint to start the chatbot
│  ├─ core.py                 # Main chatbot loop and conversation handling
│  ├─ input_utils.py          # Input helper with timeout support
│  ├─ ollama_client.py        # Ollama API wrapper for sending prompts
│  ├─ logging_utils.py        # Sets up system, audit, and chat loggers
│  ├─ session.py              # Session lifecycle management
│  └─ config.py               # Central configuration
├─ docs/                      # Notes, roadmap, and design documents
└─ logs/                      # Log files created at runtime
   ├─ system_logs/            # Technical errors and exceptions
   ├─ audit/                  # Session start/end events
   └─ chat_logs/              # Full conversation history
```

---

## How It Works

1. **Start the Chatbot**

   Run the chatbot from the command line:

   ```bash
   python -m chatbot.main
   ```

   You will see:

   ```text
   Cortex Chatbot ready! Type 'exit' or 'quit' to stop.
   ```

2. **User Interaction**

   - The chatbot waits for input with a timeout of 60 seconds.
   - Type your message and press Enter.
   - The bot responds using the local Ollama model.
   - Conversation memory is stored only for the current session.

3. **Conversation History**

   - Each user message and bot response is stored in `conversation_history` in memory.
   - Every message is also logged to chat logs for auditing and internal review.
   - Conversation history is not automatically loaded again as future context.

4. **Exit**

   - Type `exit` or `quit` to end the session.
   - If no input is received for 60 seconds, the chatbot automatically quits.
   - Session start and end times are recorded in the audit log.

5. **Logging**

   - System logs: unexpected errors and exceptions
   - Audit logs: session start and end events
   - Chat logs: full conversation history

---

## Logging

### System Logs

Stored in:

```text
logs/system_logs/system.log
```

Used for:
- unexpected errors
- Ollama API failures
- future file loading errors
- developer debugging

### Audit Logs

Stored in:

```text
logs/audit/audit.log
```

Used for:
- session start
- session end
- duration
- exit reason
- hostname

### Chat Logs

Stored in:

```text
logs/chat_logs/chat.log
```

Used for:
- user questions
- bot responses
- session-linked conversation history

Important note:

Chat logs may contain sensitive data. If this becomes a public-facing chatbot, chat logs should be reviewed carefully. Future work may include masking, sanitising, encryption, or configurable chat logging.

---

## Design Decisions

### Local LLM

The chatbot uses Ollama so that the model runs locally. Prompts are sent to:

```text
http://localhost:11434/api/generate
```

### Service Does Not Use ChatGPT

This project is separate from ChatGPT. It uses a local Ollama model such as `llama2`.

### Session Memory Only

Conversation history is kept in memory during a session only. When the chatbot exits, the memory is gone.

The chat log persists to disk, but it is not currently loaded back into the model as context.

### Timeout

The chatbot has a 60 second inactivity timeout so it does not sit forever waiting for input.

### Separate Logs

System logs, audit logs, and chat logs are kept separate to support future growth.

---

## Next Steps / TODO

- **Add relevant context files**
  - Load external PDFs, text files, markdown files, or other resources to provide additional knowledge for the chatbot.

- **Web scraping tool for context creation**
  - Use `requests` and `BeautifulSoup` to pull relevant content from websites for context-aware responses.

- **Integrate conversation history into context**
  - Optionally feed previous chat logs back into the context section for continuity and learning.
  - This should be done carefully to avoid bloated prompts or leaking sensitive data.

- **Increase captured log information**
  - Add more detailed system and audit logs.
  - Consider user metadata, timestamps, duration, IP address, exit reason, and error codes.

- **Consider security logging**
  - If the chatbot becomes public-facing, track abnormal behaviour, repeated requests, abusive prompts, or DDoS-style patterns.

- **Test larger LLaMA / Ollama models**
  - Explore using bigger or newer models to improve chatbot responses and accuracy.
  - Compare speed, quality, and resource usage.

- **Improve prompt and context handling**
  - Add a system prompt.
  - Limit prompt size.
  - Consider a sliding memory window.
  - Consider retrieval augmented generation later.

- **User documentation / onboarding**
  - Add setup instructions for macOS, IntelliJ, and terminal use.
  - Add troubleshooting for Ollama and Python environment issues.

- **Proper packaging**
  - Add `pyproject.toml`.
  - Make the project installable.
  - Add a CLI command.

- **Upload project to GitHub or Gerrit**
  - Include `.gitignore`, `README.md`, and `requirements.txt`.
  - Avoid committing `.venv`, logs, or local IDE files.

---

## Running the Project

From the project root:

```bash
source .venv/bin/activate
python -m chatbot.main
```

If Ollama is not running, start it first:

```bash
ollama serve
```

Or:

```bash
ollama run llama2
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named requests`

Install dependencies:

```bash
pip install -r requirements.txt
```

### Ollama API error

Check that Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

### Model not found

Check installed models:

```bash
ollama list
```

Pull the model if missing:

```bash
ollama pull llama2
```

### macOS SSL warning

You may see a warning about LibreSSL and urllib3. For this local chatbot, it is usually not a blocker because Ollama is called over local HTTP.

---

## Git Ignore Notes

The project ignores:

- virtual environments
- Python cache files
- logs
- macOS system files
- IntelliJ project files

This avoids accidentally committing local runtime data or generated files.
