# Cortex Chatbot

A private AI chatbot built in Python using Ollama and a local LLaMA model.

This project was built as a learning project and as the basis of a small local chatbot that can later be expanded with context files, web scraping, better logging, model switching, and packaging.

The chatbot currently:
- Runs locally using Ollama
- Uses a local model such as `llama2`
- Checks Ollama is reachable before starting and fails fast with a clear message if not
- Applies a system prompt to give the model consistent identity and behaviour
- Maintains conversation memory during the current session only
- Automatically exits after a timeout
- Logs system errors, session audit events, and chat history separately in JSON format

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

6. **Install the Package**

   Install the project and its dependencies in editable mode:

   ```bash
   pip install -e .
   ```

   This installs the `cortex` terminal command and all required packages. Alternatively, install dependencies only:

   ```bash
   pip install -r requirements.txt
   ```

---

## Project Structure

```text
cortex/
├─ README.md                  # Project overview, usage, logging, and roadmap
├─ pyproject.toml             # Package definition and cortex CLI entry point
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

   If installed with `pip install -e .`, run from anywhere:

   ```bash
   cortex
   ```

   Or run directly from the project root:

   ```bash
   python -m chatbot.main
   ```

   You will see:

   ```text
   Cortex Chatbot ready! Type 'exit' or 'quit' to stop.
   ```

2. **Startup Health Check**

   Before the session starts, the chatbot checks that Ollama is reachable at `http://localhost:11434`. If it is not, you will see:

   ```text
   Error: Cannot connect to Ollama at http://localhost:11434.
   Make sure Ollama is running ('ollama serve') and try again.
   ```

   The chatbot exits cleanly rather than crashing mid-session.

3. **User Interaction**

   - The chatbot waits for input with a timeout of 60 seconds.
   - Type your message and press Enter.
   - The bot responds using the local Ollama model.
   - Conversation memory is stored only for the current session.

4. **Conversation History**

   - Each user message and bot response is stored in `conversation_history` in memory.
   - Every message is also logged to chat logs for auditing and internal review.
   - Conversation history is not automatically loaded again as future context.

5. **Exit**

   - Type `exit` or `quit` to end the session.
   - If no input is received for 60 seconds, the chatbot automatically quits.
   - Session start and end times are recorded in the audit log.

6. **Logging**

   - System logs: unexpected errors and exceptions
   - Audit logs: session start and end events
   - Chat logs: full conversation history stored as JSON

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
- startup health check failures
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

Each entry is a JSON object on a single line, for example:

```json
{"session_id": "abc-123", "role": "user", "content": "How do I reset my password?"}
```

Used for:
- user questions
- bot responses
- session-linked conversation history
- analysis of what users are asking

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

### System Prompt

A system prompt is defined in `config.py` and passed to the Ollama API as a separate `system` field alongside the conversation text. This gives the model consistent identity and behaviour across all sessions without the prompt appearing in the conversation history. The system prompt can be updated in `config.py` without changing any other code.

### Startup Health Check

Before starting a session, the chatbot calls `GET /api/tags` on the Ollama server. If Ollama is not reachable, the chatbot exits immediately with a clear error message rather than failing mid-conversation with a confusing traceback.

### Session Memory Only

Conversation history is kept in memory during a session only. When the chatbot exits, the memory is gone.

The full session history is retained in memory throughout a conversation. Dropping early messages would harm answer quality for long sessions, so there is no sliding window. If context size becomes a problem in future, the right solution is to summarise older messages rather than discard them.

The chat log persists to disk, but it is not currently loaded back into the model as context.

### Timeout

The chatbot has a 60 second inactivity timeout so it does not sit forever waiting for input.

### Separate Logs

System logs, audit logs, and chat logs are kept separate to support future growth.

### JSON Chat Logging

Chat log entries are serialised as JSON so they can be parsed, filtered, and analysed with standard tools. Each line contains the session ID, role, and message content.

---

## Next Steps / TODO

- **Add relevant context files**
  - Load external PDFs, text files, markdown files, or other resources to provide additional knowledge for the chatbot.

- **Web scraping tool for context creation**
  - Use `requests` and `BeautifulSoup` to pull relevant content from websites for context-aware responses.

- **Integrate conversation history into context**
  - Optionally feed previous chat logs back into the context section for continuity and learning.
  - This should be done carefully to avoid bloated prompts or leaking sensitive data.

- **Conversation summarisation for long sessions**
  - If context window limits become a problem, compress older messages into a summary rather than discarding them, so early context is not lost.

- **Increase captured log information**
  - Add more detailed system and audit logs.
  - Consider user metadata, timestamps, duration, IP address, exit reason, and error codes.

- **Consider security logging**
  - If the chatbot becomes public-facing, track abnormal behaviour, repeated requests, abusive prompts, or DDoS-style patterns.

- **Test larger LLaMA / Ollama models**
  - Explore using bigger or newer models to improve chatbot responses and accuracy.
  - Compare speed, quality, and resource usage.

- **User documentation / onboarding**
  - Add setup instructions for macOS, IntelliJ, and terminal use.
  - Add troubleshooting for Ollama and Python environment issues.

- **Upload project to GitHub or Gerrit**
  - Include `.gitignore`, `README.md`, and `requirements.txt`.
  - Avoid committing `.venv`, logs, or local IDE files.

---

## Running the Project

If installed with `pip install -e .`, run from anywhere:

```bash
cortex
```

Or from the project root:

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
pip install -e .
```

### Ollama not reachable on startup

The chatbot will display a clear error message and exit. Start Ollama and try again:

```bash
ollama serve
```

Verify Ollama is responding:

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