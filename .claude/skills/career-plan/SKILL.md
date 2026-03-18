---
name: career-plan
description: Analyze career position, identify skill gaps against target roles, and produce a concrete learning and job search roadmap.
disable-model-invocation: true
---

Analyze career position, identify skill gaps against target roles, and produce a concrete learning and job search roadmap.

---

## Input Contract

Accept any of:
- Target role(s) or job descriptions
- Current resume or skills summary
- A timeline or constraint ("I want to be interviewing in 8 weeks")
- An open-ended request ("help me figure out what to do next")

If nothing is provided, ask: "What kind of role are you targeting, and how much runway do you have before you need to be interviewing?"

---

## Workflow

### Step 1 — Define the target

Confirm or establish:
- Primary target role (e.g., Senior Android Engineer at a product company)
- Secondary targets (if any — e.g., Mobile TL, platform/SDK roles, cross-platform)
- Company profile preferences (startup vs. large tech, domain, stage)
- Timeline: weeks until target interview-ready

If multiple targets, ask the user to rank them and work from the top.

### Step 2 — Skill gap analysis

Compare the user's current skills (from resume or self-report) against typical requirements for the target role.

Organize gaps into three tiers:
- **Blocking gaps** — required skills the user lacks or is weak in (address first)
- **Competitive gaps** — skills that would meaningfully differentiate vs. other candidates
- **Nice-to-have gaps** — worth knowing but not critical for the job search timeline

For each blocking or competitive gap, propose:
- A specific resource (course, doc, book, open source project)
- An estimated time investment
- A way to demonstrate the skill (project, PR, blog post, or portfolio piece)

### Step 3 — Build the roadmap

Given the timeline, produce a week-by-week plan. Structure:

```
Week 1–2: [Foundation / quick wins]
Week 3–4: [Core skill area 1]
Week 5–6: [Core skill area 2 + resume polish]
Week 7–8: [Interview prep + applications]
```

Adjust depth and scope to fit the actual timeline. If the timeline is very short (< 4 weeks), prioritize ruthlessly: resume + interview prep only.

Include in the roadmap:
- Specific learning tasks with concrete outputs
- Resume and LinkedIn milestones
- Application volume targets (e.g., 5–10 applications/week)
- Mock interview checkpoints

### Step 4 — Alternative path exploration (optional)

If the user is open to it, explore adjacent roles that leverage existing Android/mobile skills:
- Mobile platform or infrastructure engineer
- Developer tools / SDK engineer
- Kotlin Multiplatform / cross-platform roles
- Technical program manager (mobile focus)
- Developer advocate or solutions engineer

For each, briefly describe: what changes, what transfers, and how to position the resume differently.

---

## Output Contract

Deliver a Markdown roadmap document with:
- Target role summary
- Skill gap table (blocking / competitive / nice-to-have)
- Week-by-week plan
- Resource list with links or titles
- Optional: alternative path summaries
