# Cortex Chatbot Blog Journal

## Entry 1 — Project Setup

The project started as a private local chatbot experiment using Python and Ollama.

Initial decisions:
- Use IntelliJ as the IDE.
- Use Python with a virtual environment.
- Use Ollama to run a local model.
- Start with a simple command line chatbot.
- Keep code readable and heavily commented.

## Entry 2 — Ollama Integration

The first version used subprocess to call the `ollama` command directly.

Problems found:
- Python could not always find the `ollama` binary.
- IntelliJ did not always pass the same PATH as the terminal.
- The chatbot could hang if the Ollama server was not running.

The design was changed to use the Ollama local API instead:

```text
http://localhost:11434/api/generate
```

## Entry 3 — Model Discovery

The installed model was checked with:

```bash
ollama list
```

The local model was:

```text
llama2:latest
```

This confirmed that the chatbot was using a local model, not ChatGPT.

## Entry 4 — Conversation Memory

The first chatbot sent every question independently.

That meant the model treated each question as brand new.

Session conversation memory was added by keeping a list:

```python
conversation_history = []
```

Every user question and bot response is appended to this list and the full session is sent as context.

## Entry 5 — Timeout

The original loop could wait forever.

A 60 second timeout was added using `threading` and `queue`.

This was chosen because it is OS agnostic and works across macOS, Linux, and Windows.

## Entry 6 — Logging

Logging was added in three separate areas:

- system logs for errors
- audit logs for session start/end
- chat logs for conversation history

Log rotation was set at:
- 20 MB per file
- 5 backup files
- around 100 MB per log category

## Entry 7 — Refactor

The original `main.py` started getting too long.

The project was refactored into:
- `main.py`
- `core.py`
- `input_utils.py`
- `ollama_client.py`
- `logging_utils.py`
- `session.py`
- `config.py`

This keeps each file focused on one responsibility.

## Entry 8 — Source Control

The project was prepared for Git / Gerrit / GitHub.

A `.gitignore` was added to prevent committing:
- `.venv`
- logs
- cache files
- OS files
- IntelliJ files
