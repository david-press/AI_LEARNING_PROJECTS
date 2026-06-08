# 🤖 AI Engineering Projects — Krish

> A collection of applied AI projects built while learning AI engineering from first principles. Each project targets a real use case, uses production-grade patterns.
---

## 🧭 What This Repository Is

This isn't a tutorial repo. Every project here is:
- **Built before studied** — real problems first, theory second
- **Deployed or deployable** — no unfinished demos
- **Designed to compound** — skills stack compound

Stack defaults: **Python · FastAPI · Groq SDK · Pydantic · PostgreSQL**

---

## 📁 Projects

| # | Project | Concepts | Status |
|---|---------|----------|--------|
| 01 | [Business Card Extractor](#01-business-card-extractor) | Groq completions, streaming, Pydantic validation, QR generation | ✅ Complete |
| 02 | *(coming soon)* | — | 🔄 In progress |

---

## 🔍 Project Breakdowns

### 01 · Business Card Extractor
**Folder:** `01-business-card-extractor/`

Extracts structured contact data from plain-text business card descriptions using LLM inference, validates the output with Pydantic, generates QR codes, and logs every interaction to JSONL.

**Key concepts:**
- Groq SDK chat completions with streaming
- System prompt engineering for structured JSON output
- Pydantic BaseModel validation with typed optional fields
- QR code generation from extracted phone numbers
- JSONL logging for persistent interaction records
- Secure API key management with `python-dotenv`

---

## 🧱 Core AI Patterns Being Built

These patterns repeat across all projects — deliberately:

| Pattern | Description |
|---------|-------------|
| **Structured Outputs** | Forcing LLMs to return typed JSON via system prompts |
| **Pydantic Validation** | Treating LLM output as untrusted data requiring validation |
| **Streaming** | Real-time token delivery for better UX |
| **Prompt Engineering** | System vs user role separation, temperature control |
| **Logging** | JSONL interaction logs for debugging and eval |
| **LLM-as-Judge** *(upcoming)* | Using AI to evaluate AI outputs |
| **Tool Calling** *(upcoming)* | Giving models access to external functions |
| **Context Management** *(upcoming)* | Multi-turn conversation with controlled memory |

---

## 🛠️ Local Setup (General)

Each project has its own `README.md` and `requirements.txt`. General pattern:

```bash
git clone https://github.com/yourusername/ai-projects.git
cd ai-projects/01-business-card-extractor

pip install -r requirements.txt
cp .env.example .env  # Add your GROQ_API_KEY

python main.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 📄 License

MIT — open to learn from, fork, and build on.
