# Cortex — Enterprise Knowledge Assistant
### Living Project Document | Brian Kilpatrick | briankilpatrick.dev
---

## Project Overview

Cortex is a private AI chatbot built in Python using Ollama as the local LLM runtime. Originally built as a hobby project exploring enterprise knowledge management use cases. Reconstructed via ChatGPT history and established as a clean project in version control.

**GitHub:** https://github.com/briankilpatrick/cortex  
**Local path:** /Users/brian/IdeaProjects/cortex

---

## The Problem

Most enterprise knowledge is locked away in documentation, codebases, training materials, and white papers that nobody can find when they need it. Every company has the same issue.

The questions people ask are as valuable as the answers. Every interaction is a signal about what's missing, unclear, or undocumented — feeding into product roadmaps, sales pipelines, training materials, and better customer interactions.

---

## Core Use Cases

### 1. Customer Self-Service
Customers ask questions and get instant, accurate answers without waiting for support. Reduces support burden, improves customer experience, and surfaces gaps in documentation.

### 2. Internal Training and Onboarding
Staff onboard and train through conversation rather than static manuals. Questions asked highlight areas that are missing or unclear in training materials.

### 3. Customer Success and Support Acceleration
Support teams resolve issues faster with an AI that knows the product, documentation, and historical interactions. Reduces resolution time and improves consistency.

### 4. Version-Aware Diagnostics and Upgrade Intelligence
A customer on an older product version raises an issue. Cortex understands the problem through conversation, retrieves documentation relevant to their specific version, provides an immediate workaround, identifies that the issue was fixed in a later version, surfaces all the improvements made since their version, recommends the upgrade path, and automatically alerts the sales team with full context — customer, issue, version gap, and upgrade opportunity. One support interaction becomes a qualified sales lead with zero human effort.

---

## The Data Insight

Every question asked is a signal. Aggregated and analysed, user questions reveal:

- Product gaps and missing features
- Documentation weaknesses
- Common customer pain points
- Training material deficiencies
- Sales pipeline opportunities
- Customer sentiment and urgency patterns

**This data is as valuable as the product itself.**

---

## Intelligence Layers

### Question Classification
Every user question is automatically classified into one of:

- Missing product feature
- Missing or unclear documentation
- Marketing signal or opportunity
- Support or diagnostic request
- Upgrade or upsell opportunity

This classification happens either in real time alongside the conversation, or as a structured summary generated at session end.

### Emotional and Urgency Metadata
Each question is analysed not just for content but for how it was asked. Metadata captured alongside every message:

- **Sentiment** — frustrated, neutral, confident, confused
- **Urgency** — high, medium, low
- **Confidence** — does the user seem sure of what they're asking, or are they guessing?

This turns raw question logs into prioritised intelligence. A frustrated, high-urgency question about the same feature three times in a week is a five-alarm signal. The same question asked casually is just a documentation gap. Emotional context tells you which fires to fight first.

### Session Summarisation
At the end of every conversation, an AI summarisation layer reads the full session and produces a structured report covering:

- Topics discussed
- Questions asked, classified by category
- Sentiment arc across the session
- Any upgrade or sales signals detected
- Recommended follow-up actions

---

## Document and Knowledge Ingestion

### Context File Loading
Cortex can be pointed at documents to use as knowledge context. Two modes:

**Reference mode** — Cortex reads directly from a stable source. Suitable for files in cloud storage (S3, SharePoint, Google Drive) or on a local network path that won't move or have access issues. No copy required.

**Ingest mode** — Cortex copies the document into local storage. Used when the source might change, become unavailable, or needs to be version-pinned.

Supported sources include PDFs, text files, markdown files, and any plain-text format.

### Web Scraping and Knowledge Ingestion
User-initiated scraping of external web content into the Cortex knowledge base. Designed for:

- Product documentation sites (often multiple versions in history)
- User guides and setup guides
- Knowledgebase articles
- CVE and security advisories
- New product release notes

Scraped content is stored locally and tagged with metadata including product version, scrape date, and source URL. Cortex is version-aware — it knows which documentation applies to which product version, and can answer a question in the context of the version the customer actually has, while also surfacing what has changed in later versions.

A refresh schedule can be configured so the knowledge base stays current without manual intervention.

---

## Tech Stack

### Stage 1 — POC (Current)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python | Core application |
| LLM Runtime | Ollama | Local model serving |
| Model | llama2 (upgrade to mistral / llama3) | AI responses |
| Terminal UI | Rich | CLI interface |
| Storage | SQLite | Session and baseline storage |
| Logging | Python logging + JSON | Chat, system, and audit logs |
| Config | YAML + env vars | Configuration management |
| Packaging | pyproject.toml | Installable package |
| Web scraping | beautifulsoup4 (ready, not yet implemented) | Knowledge ingestion |

---

## Roadmap

### Stage 1 — POC (Current)
- Python CLI application
- Ollama local LLM runtime
- Conversation memory retained for session
- JSON logging — chat, system, audit
- Ollama health check on startup
- Environment variable configuration
- System prompt via config.py
- Unit tests for ollama_client, input_utils, session, core
- Ruff linting configuration and clean pass

### Stage 2 — MVP
- Python + FastAPI backend / local agent
- Next.js + React + Tailwind web dashboard
- SQLite → Postgres database migration
- PyInstaller packaging and desktop installer
- Claude API integration
- PDF report generation
- Context file loading — reference mode and ingest mode
- Web scraping implementation — user-initiated, version-tagged, scheduled refresh
- End of session AI summarisation — structured classification report
- Emotional and urgency metadata capture per message
- Question classification layer — feature gap, docs gap, marketing signal, sales signal

### Stage 3 — First Commercial Product
- Rust rewrite for collectors layer (WiFi, network, DNS)
- Python + FastAPI backend retained
- Next.js + React + Tailwind frontend expanded
- Postgres database
- Optional cloud backend for fleet / org correlation
- Stripe billing integration
- Account system — sync, multi-device
- Multi-platform support — Windows, macOS, Linux
- Real-time question classification agent (per-message, low-latency)
- Analytics dashboard — question trends, sentiment patterns, upgrade signals

---

## Fixes Completed to Date

| # | Fix | Detail |
|---|-----|--------|
| 1 | Log path bug fixed | Anchored to source file location, not current working directory |
| 2 | System prompt added | Cortex persona defined in config.py — clear, honest, concise |
| 3 | Conversation history retained | Intentional decision — full history required for use case |
| 4 | Chat log format fixed | JSON serialisation with json.dumps() — parseable programmatically |
| 5 | pyproject.toml added | Project is installable with cortex entrypoint command |
| 6 | Ollama health check | Fails fast on startup with clear message if Ollama not running |
| 7 | Environment variable config | MODEL_NAME and OLLAMA_API_URL overridable via env vars |
| 8 | Cirata references removed | All references refactored to Cortex throughout |
| 9 | README kept in sync | Documentation updated with every change made |

---

## Still To Do

- Add tests — unit tests for ollama_client, input_utils, session, core
- Add linting — ruff configuration and clean pass
- Add `.env.example` — document available environment variables for new contributors
- Check `logs/` directory — confirm no actual log data was committed to git
- Get running locally — install Ollama, pull mistral or llama3 model
- Test end to end — run cortex command and have a real conversation
- Add CI/CD — GitHub Actions for ruff on push as a starting point
- Implement context file loading — reference mode first, ingest mode second
- Implement web scraping — beautifulsoup4 already in requirements
- Implement session summarisation — AI call on session end, structured output
- Implement question classification layer
- Implement emotional / urgency metadata capture
- Add CHANGELOG — track what changed and when
- Consider front end — chat UI rather than CLI for MVP

---

## Architecture Decisions

### Local LLM First
Cortex runs models locally via Ollama. Prompts never leave the machine. This is the core differentiator — company data stays private by design, not by policy.

### RAG vs Simple Context Loading
For small document sets, documents are loaded directly into the prompt as context at session start. For large document sets (thousands of files), the right approach is RAG — retrieval augmented generation — which indexes documents and retrieves only relevant chunks per question. Simple context loading is the Stage 2 approach. RAG is Stage 3.

### Session Memory Only (Current)
Conversation history lives in memory during a session. When the session ends, memory is gone. The chat log persists to disk but is not currently loaded back as future context. This is intentional for the POC — loading historical context requires careful design to avoid bloated prompts and sensitive data leakage.

### Separate Log Types
System logs, audit logs, and chat logs are kept separate to support future growth and make each easier to analyse independently.

### Version-Aware Knowledge Base
When documents are ingested — whether scraped or loaded — they are tagged with the product version they relate to. This allows Cortex to answer questions in the context of the customer's version while simultaneously surfacing what has changed in later versions.

---

## Privacy and Data Posture

Cortex makes no external calls during a conversation. No telemetry. No third-party data sharing. All model inference happens locally via Ollama. This is the foundational privacy guarantee and the primary differentiator from cloud-based competitors.

Chat logs may contain sensitive data. If Cortex becomes public-facing, chat logs should be reviewed carefully. Future work includes configurable log masking, encryption at rest, and role-based access to log data.

---

## Commercial Potential

The market is proven — Microsoft Copilot, Glean, Guru, and Notion AI all operate in this space. None focus on the fully private, on-premise angle at an accessible price point, and none combine knowledge retrieval with version-aware diagnostics and automated sales signal routing.

**The differentiator:** company data never leaves the building, and every support interaction is also an intelligence and sales opportunity.

### Target Verticals

- Legal — client confidentiality, cannot use cloud AI
- Finance — regulatory compliance, data governance
- Healthcare — patient data, GDPR, information governance
- Defence contractors — security clearance environments
- SaaS companies with versioned products and large customer bases
- Any enterprise with strict data sovereignty requirements

### Commercial Models

- SaaS — monthly fee, company uploads docs, you host infrastructure
- On-premise licence — deploy into their environment, annual fee
- Vertical specific — go deep on one industry, become the knowledge assistant for that sector

---

*Cortex — Enterprise Knowledge Assistant | Internal project document | Brian Kilpatrick | briankilpatrick.dev*
