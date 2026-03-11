# Skill: resume-tailor

Generate a tailored resume for a specific job posting, derived from the master resume.

---

## Input Contract

Required:
- A job description (paste inline or attach)
- A master resume (from `resume-build`) — if not available, stop and ask the user to provide one or run `resume-build` first

Optional:
- Company name and any known context (stage, team size, product area)
- User's notes on why they want this role or what to emphasize

---

## Workflow

### Step 1 — Analyze the job description

Extract and organize:

**Must-haves** — explicit requirements (years of experience, specific tech, platforms)
**Nice-to-haves** — preferred or bonus qualifications
**Key responsibilities** — what will this person actually do day-to-day?
**Themes** — underlying priorities of the role (e.g., performance, product ownership, platform scale, technical leadership, cross-functional collaboration)
**Keywords** — exact terms likely used by ATS (e.g., "Jetpack Compose", "coroutines", "modular architecture", "A/B testing", "CI/CD")

Present this analysis to the user before proceeding. Ask: "Does this match your read of the role? Anything to add?"

### Step 2 — Map master resume to JD

From the master resume:
- Select the roles and bullets that best match the JD themes and requirements
- Identify bullets that can be rephrased to mirror JD language — do this only where honest and accurate
- Identify content to deprioritize or cut (less relevant roles, skills not mentioned in JD)

Flag any JD requirements that have no clear match in the master resume. Ask the user: "I didn't find strong coverage for [X] — do you have relevant experience not captured in your master resume?"

### Step 3 — Draft the tailored resume

Rules:
- Keep the same structure as the master resume
- Reorder bullets within a role to lead with most JD-relevant content
- Adjust the Summary to speak directly to the role's themes
- Adjust the Skills section to lead with tech mentioned in the JD
- Do not add experience or skills that don't exist in the master resume
- Keep format ATS-friendly: plain headings, no tables, no columns, consistent bullet style

### Step 4 — Deliver with diff and rationale

Write two separate files:

1. `resume-[company-or-role].md` — the tailored resume only, no change notes
2. `resume-[company-or-role]-changes.md` — change summary including:
   - Keywords incorporated
   - Bullets rewritten or reordered
   - Content removed or deprioritized
   - Any gaps flagged (JD requirements not covered)

---

## Output Contract

- `resume-[company-or-role].md` — tailored resume (clean, no annotations)
- `resume-[company-or-role]-changes.md` — change rationale and gap flags
