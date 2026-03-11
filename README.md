# career-bot

An agentic AI assistant for navigating a job search — from building resumes to preparing for interviews.

## What It Does

- **Resume building** — Generate polished, well-structured resumes from raw notes and career documents
- **Resume tailoring** — Adapt resumes to specific job postings, surfacing the most relevant experience and skills
- **Interview preparation** — Behavioral coaching, STAR story refinement, technical prep, and system design practice
- **Career planning** — Skill gap analysis, learning roadmaps, and path exploration

## How to Use

1. Clone this repo (or click "Use this template" on GitHub)
2. Open the directory in [Claude Code](https://claude.ai/code)
3. Optionally fill in your profile (see [SETUP.md](SETUP.md))
4. Start a session — the agent will introduce itself and guide you from there

See [SETUP.md](SETUP.md) for the full setup guide, including how to keep your personal career documents in a separate private repo.

## Approach

The agent uses a persona defined in `CLAUDE.md` and a set of slash commands in `.claude/commands/` — one per workflow mode. No build step, no install, no tooling required. Clone and go.

## Project Structure

```
career-bot/
├── CLAUDE.md                    # Agent persona and behavior (auto-loaded by Claude Code)
├── agent.md                     # Human-readable reference copy of the agent definition
├── README.md                    # This file
├── SETUP.md                     # Step-by-step onboarding guide
├── user-profile.template.md     # Copy → user-profile.md and fill in
├── .gitignore                   # Prevents personal docs from being committed
└── .claude/
    └── commands/
        ├── resume-build.md
        ├── resume-tailor.md
        ├── interview-behavioral.md
        ├── interview-technical.md
        └── career-plan.md
```

## For Contributors

This repo is the public agent — no personal career documents live here. If you want to keep your own docs version-controlled, see the two-repo model described in [SETUP.md](SETUP.md).

## Tech Stack

- Claude (Anthropic) — core LLM powering the agent
- Claude Code — runtime environment
