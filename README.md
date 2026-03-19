# Career Bot

A Claude Code agent that helps software engineers navigate their job search. It turns raw career materials (brag docs, performance reviews, old resumes) into polished outputs and provides structured interview preparation.

## Setup

1. Clone this repo
2. Copy `user-profile.template.md` to `user-profile.md` and fill in your details
3. Open the project with [Claude Code](https://claude.com/claude-code)

The agent reads `user-profile.md` at the start of each session to tailor its guidance. If the file doesn't exist, it will ask you onboarding questions instead.

## Skills

| Skill                    | Slash command           | What it does                                                                                |
| ------------------------ | ----------------------- | ------------------------------------------------------------------------------------------- |
| **Resume Build**         | `/resume-build`         | Extracts achievements from raw docs and assembles a master resume (`base-resume.md`)        |
| **Resume Tailor**        | `/resume-tailor`        | Analyzes a job description against your resume and suggests targeted improvements           |
| **Interview Behavioral** | `/interview-behavioral` | Builds a STAR story bank and runs mock behavioral interviews                                |
| **Interview Technical**  | `/interview-technical`  | Runs technical interview prep — baseline assessment, question banks, system design practice |
| **Career Plan**          | `/career-plan`          | Skill gap analysis and week-by-week learning roadmap for a target role                      |

## Output Format

Resume files are produced as Markdown with YAML front matter, designed to be consumed by downstream conversion tools (e.g., PDF pipelines). See the Output Format section in `CLAUDE.md` for the full specification.

## Project Structure

```
.
├── CLAUDE.md                    # Agent definition
├── .claude/skills/              # Skill workflows
├── user-profile.template.md     # Profile template (copy to user-profile.md)
├── base-resume.md               # Master resume (created by resume-build)
├── resume-<company>.md          # Tailored variants (created by resume-tailor)
└── source-material/             # Raw input docs (brag docs, old resumes, JDs)
```
