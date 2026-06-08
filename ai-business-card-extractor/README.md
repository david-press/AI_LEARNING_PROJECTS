# 🪪 Business Card Extractor & Analyzer

> Extract structured contact information from plain-text business card descriptions using AI — with automatic QR code generation and persistent logging.

---

## 📌 What This Project Does

You type a business card description (e.g., *"John Doe, CTO at Groq, john@Groq.io, +234-800-0000"*), and the app:

1. Sends it to the **Groq AI API** (LLaMA 3.3 70B model) with a strict JSON system prompt
2. Streams back a structured JSON response in real-time
3. Validates the response using **Pydantic schemas**
4. Displays the extracted contact info in a clean table
5. Optionally generates a **QR code** for the phone number
6. Logs every interaction to a `.jsonl` file for record-keeping

---

## 🗂️ File Structure

```
business-card-extractor/
│
├── main.py          # Core application logic
├── schema.py        # Pydantic data models (validation layer)
├── .env             # API key storage (not committed to Git)
├── requirements.txt # Project dependencies
│
├── qr_codes/        # Auto-generated QR code images (created at runtime)
└── Business_Card_Analysis.jsonl  # Interaction logs (created at runtime)
```

---

## 🧠 Concepts Explained

### 1. Groq SDK + LLM Completions
The app uses the **Groq SDK** to call the `llama-3.3-70b-versatile` model. Groq provides ultra-fast inference via its custom LPU (Language Processing Unit) hardware.

```python
client.chat.completions.create(
    model=model,
    temperature=temperature,
    messages=[{"role": "user", "content": system_prompt}],
    stream=True
)
```

- `messages` follows the OpenAI-compatible chat format (role/content pairs)
- `temperature=0.3` keeps outputs consistent and deterministic — critical when you need reliable JSON

### 2. Streaming
Instead of waiting for the full response, streaming prints each token as it arrives — giving real-time feedback to the user.

```python
for chunk in response:
    delta = chunk.choices[0].delta.content or ""
    content += delta
    print(delta, end="", flush=True)
```

Each `chunk` contains a partial token. Concatenating them rebuilds the full response.

### 3. Structured Outputs via System Prompt Engineering
The system prompt forces the LLM to return **only valid JSON** in a fixed schema. No preamble, no explanation — just the object.

```python
system_prompt = f"""
ONLY RETURN THE JSON IN THE EXACT FORMAT MENTIONED BELOW:
{{
    "card": {{
        "full_name": "...",
        "email": "...",
        ...
    }}
}}
"""
```

This is a core AI engineering pattern: **constraining LLM output format** through explicit system instructions.

### 4. Pydantic Validation (schema.py)
Raw LLM output is a string. Pydantic converts it into a **typed Python object** with validation rules enforced.

```python
class CardAnalysis(BaseModel):
    full_name: Optional[str] = Field(default=None)
    completeness_score: float = Field(ge=0, le=100)
```

- `Optional[str]` — fields can be `None` if the card doesn't have that info
- `Field(ge=0, le=100)` — enforces that score is always between 0 and 100
- `BatchResponse.model_validate_json(request)` — parses and validates the JSON string in one call

### 5. QR Code Generation
The `qrcode` library encodes the phone number into a scannable QR image saved as a `.png` file.

```python
qr.add_data(f"tel:{phone_number}")
img.save(filename)
```

The `tel:` prefix is a URI scheme — when scanned, most phones will prompt to call the number directly.

### 6. JSONL Logging
Every interaction is saved to `Business_Card_Analysis.jsonl` — one JSON object per line. JSONL (JSON Lines) is preferred over a plain JSON array for logs because:
- Each line is independently readable
- Safe to append without rewriting the full file
- Easy to stream or grep through large logs

### 7. `.env` + `python-dotenv`
API keys are never hardcoded. They're stored in a `.env` file and loaded at runtime:

```python
load_dotenv(override=True)
API_KEY = os.getenv("GROQ_API_KEY")
```

`override=True` ensures `.env` values take precedence over system environment variables.

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/business-card-extractor.git
cd ai-business-card-extractor

# 2. Install dependencies
pip install groq pydantic python-dotenv qrcode[pil]

# 3. Create your .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run
python main.py
```

---

## 💡 Example Usage

```
You: Sarah Ahmed, Head of Partnerships at Paystack, sarah@paystack.com, +234-801-234-5678

Groq Response: {"card": {"full_name": "Sarah Ahmed", "job_title": "Head of Partnerships", ...}}

Full Name............ Sarah Ahmed
Job Title............ Head of Partnerships
Company.............. Paystack
Email................ sarah@paystack.com
Phone................ +234-801-234-5678
Completeness......... 98.0%

Generate QR code for this phone number? (yes/no): yes
✓ QR code saved: qr_codes/qr_SarahAhmed_20260608_143022.png
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `groq` | LLM inference via Groq API |
| `pydantic` | Response validation & type safety |
| `python-dotenv` | Secure API key management |
| `qrcode` | QR code image generation |
| `pathlib` | Cross-platform file path handling |
| `json` / `jsonl` | Structured logging |

---

## 📄 License

MIT — free to use, modify, and build on.
