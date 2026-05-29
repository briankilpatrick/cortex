# Cortex Chatbot Roadmap

## Phase 1 — Foundation

Completed / reconstructed:

- Python package structure
- Ollama local API integration
- Basic chatbot loop
- Session-only conversation memory
- 60 second timeout
- README
- requirements.txt
- .gitignore

## Phase 2 — Reliability and Logging

Completed / reconstructed:

- System logger
- Audit logger
- Chat logger
- Log rotation
- Separate log folders
- Session lifecycle tracking

Still to improve:

- Better error codes
- More detailed system logging
- Configurable logging levels
- Optional chat log enable/disable switch
- Sanitisation of sensitive chat content

## Phase 3 — Context Awareness

To do:

- Add support for text files
- Add support for markdown
- Add support for PDFs
- Add support for web pages
- Decide where context files live
- Decide whether context is loaded at startup or retrieved on demand

## Phase 4 — Web Scraping Tool

To do:

- Use `requests` to download pages
- Use `BeautifulSoup` to extract clean text
- Remove navigation, scripts, headers, and footers
- Save scraped context into a local context folder
- Decide how often web pages should be refreshed

## Phase 5 — Larger / Alternate Model Testing

To do:

- Pull and test another model such as `mistral`
- Compare with `llama2`
- Compare quality, speed, and memory usage
- Update `config.py` to switch models cleanly

## Phase 6 — Documentation

To do:

- Expand README
- Add macOS + IntelliJ setup guide
- Add Ollama troubleshooting guide
- Add examples of use
- Add screenshots if useful

## Phase 7 — Packaging

To do:

- Add `pyproject.toml`
- Make project installable
- Add command line entrypoint
- Add tests
- Add linting / formatting

## Phase 8 — GitHub / Gerrit

To do:

- Push to source control
- Make sure `.gitignore` is correct
- Avoid committing logs or `.venv`
- Decide whether repo is private or public
