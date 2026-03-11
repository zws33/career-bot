# Setup Guide

Get career-bot running in under 5 minutes.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and authenticated

## Steps

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/career-bot.git
cd career-bot
```

Or click **Use this template** on GitHub to create your own copy.

### 2. Open in Claude Code

```bash
claude .
```

The agent persona in `CLAUDE.md` is auto-loaded. You're ready to go.

### 3. (Optional) Fill in your profile

Filling in a profile lets the agent skip onboarding questions and go straight to work.

```bash
cp user-profile.template.md user-profile.md
```

Open `user-profile.md` and fill in each section. The file is gitignored — it stays local.

### 4. (Optional) Add your career documents

Drop your documents into a local folder (e.g., `source-material/`). These are also gitignored.

Common documents to include:
- Master resume or work history
- Brag doc or accomplishment notes
- Performance reviews
- Any role-specific notes

### 5. Start a session

Open Claude Code in the `career-bot` directory. The agent will:
- Read `user-profile.md` if it exists (and skip onboarding questions)
- Otherwise ask a few quick onboarding questions
- Guide you to the right slash command for your goal

## Available Slash Commands

| Command | What it does |
|---------|-------------|
| `/resume-build` | Build a master resume from raw career documents |
| `/resume-tailor` | Tailor a resume to a specific job posting |
| `/interview-behavioral` | Behavioral prep, STAR coaching, mock interviews |
| `/interview-technical` | Technical prep, system design, quiz mode |
| `/career-plan` | Skill gap analysis, learning roadmap, path exploration |

## Two-Repo Model (Recommended)

To keep your personal career documents version-controlled without making them public:

1. **`career-bot`** (this repo, public) — agent, skills, no personal data
2. **`career-docs`** (private repo you create) — your resume, source material, and `user-profile.md`

In your private `career-docs` repo, you can symlink or copy `user-profile.md` into the `career-bot` directory, or simply keep them side by side and reference paths when prompting the agent.

This separation means you can pull updates to `career-bot` without touching your personal documents.
