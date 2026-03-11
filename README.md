# career-bot

An AI-powered career coaching agent for Android engineers. **career-bot** uses
LLM-backed agent personas to help you build your resume, tailor it to job
postings, and prepare for technical interviews.

---

## Features

| Command | What it does |
|---|---|
| `ingest` | Load your personal career documents into a local vector store |
| `build-resume` | Generate an ATS-friendly resume from your documents |
| `tailor` | Rewrite your resume to match a specific job posting |
| `interview` | Start an interactive Android interview coaching session |

---

## Quick Start

### 1 – Prerequisites

- Python 3.11 or newer
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 2 – Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3 – Configure

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

### 4 – Add your documents

Place your personal career documents in the `docs/` directory.
Supported formats: **PDF**, **DOCX**, **TXT**, **MD**.

```
docs/
├── accomplishments.txt   ← recent wins (quantified impact)
├── skills.txt            ← technical & soft skills
├── experience.txt        ← work history
├── projects.txt          ← notable side/work projects
└── education.txt         ← degrees, certs, courses
```

### 5 – Ingest documents

```bash
python main.py ingest
```

Only new or changed files are embedded, so re-ingestion is fast.

---

## Usage

### Build a resume

```bash
# Basic build
python main.py build-resume

# With guidance
python main.py build-resume --instructions "target a senior Android engineer role at a startup"

# Save to a custom filename and skip the interactive refinement loop
python main.py build-resume --output my_resume.md --no-interactive
```

Generated files are saved to `output/`.

### Tailor a resume to a job posting

```bash
# From a job-posting file
python main.py tailor --resume output/resume.md --job-file job.txt

# Inline job text
python main.py tailor --resume output/resume.md \
  --job-text "We are looking for a senior Android engineer experienced in Compose…"
```

The output includes:
1. A tailored resume with job-specific keywords woven in.
2. A **Match Analysis** section: key matches, skill gaps, and suggested talking
   points.

### Interview coaching

```bash
python main.py interview
```

The coach reads your career documents and opens an interactive session.
Example prompts:

- *"Give me a hard Kotlin coroutines question."*
- *"Let's do a 30-minute mock interview for a senior role."*
- *"Explain Jetpack Compose state management."*
- *"Help me craft a STAR story about improving app performance."*
- *"Prep me for an interview at a fintech startup."*

Type `quit` or press `Ctrl-C` to exit.

---

## Project Layout

```
career-bot/
├── main.py                          # CLI entry point
├── requirements.txt
├── .env.example                     # Configuration template
├── docs/                            # ← your personal career documents
├── output/                          # ← generated resumes saved here
├── career_bot/
│   ├── config.py                    # Settings (loaded from .env)
│   ├── agents/
│   │   ├── resume_builder.py        # ResumeBuilderAgent persona
│   │   ├── job_tailor.py            # JobTailorAgent persona
│   │   └── interview_coach.py       # InterviewCoachAgent persona
│   ├── tools/
│   │   └── document_processor.py   # Document ingestion & retrieval
│   └── prompts/
│       ├── resume_prompts.py
│       ├── job_tailor_prompts.py
│       └── interview_prompts.py
└── tests/
    ├── test_config.py
    ├── test_document_processor.py
    └── test_agents.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Configuration Reference

All settings can be overridden in `.env`:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | Model used by all agents |
| `CHROMA_PERSIST_DIR` | `.chroma` | ChromaDB persistence directory |
| `CHROMA_COLLECTION` | `career_docs` | Vector store collection name |
| `DOCS_DIR` | `docs` | Directory scanned for personal documents |
| `OUTPUT_DIR` | `output` | Directory where generated files are saved |

