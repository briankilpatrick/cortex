# Cortex Chatbot Design Notes

## Original Goal

Create a basic Python chatbot using best practices, clean file structure, naming conventions, Ollama, and future support for external context files.

## Current Architecture

The project is split into separate modules:

- `main.py` starts the program.
- `core.py` contains the chatbot loop.
- `input_utils.py` contains timeout input handling.
- `ollama_client.py` talks to the local Ollama API.
- `logging_utils.py` creates loggers.
- `session.py` handles session start/end.
- `config.py` stores settings.

## Key Decisions

### Use Ollama

Ollama was chosen so the LLM runs locally and privately.

### Use API Instead of Subprocess

Initial design used the `ollama` command via subprocess. This was replaced with the local HTTP API because it is cleaner and easier to control.

### Use Session Memory Only

Conversation history is kept only in memory during the current run.

We decided not to reload old chat history automatically because it could:
- bloat prompts
- slow the model down
- accidentally expose old sensitive content
- create confusing context

### Add Timeout

The original infinite loop could wait forever if the user walked away. We added a 60 second timeout using threads and a queue so the approach is OS agnostic.

### Separate Logs

We separated logs into:

- system logs
- audit logs
- chat logs

This gives flexibility for future development.

## Design Questions Still Open

### Context Files

Questions to answer:

- Which formats should be supported first?
- Should files be loaded at startup or on demand?
- Should all context be sent every time?
- Should context be chunked?
- Should embeddings / vector search be added later?

### Web Scraping

Questions to answer:

- Should web links be scraped manually or automatically?
- How should scraped pages be cleaned?
- Should scraped content be stored as files?
- Should the bot be allowed to refresh links?

### Chat Logs

Questions to answer:

- Should chat logs be used for training?
- Should sensitive data be masked?
- Should users opt in to chat logging?
- Should chat logs be JSON rather than plain Python dict strings?

### Security Logging

Questions to answer:

- What should count as suspicious activity?
- Should rate limits be added?
- Should IP addresses be logged for public deployments?
- Should logs be encrypted?

### Packaging

Questions to answer:

- Should this remain a script project?
- Should it become an installable Python package?
- Should it provide a CLI command?
