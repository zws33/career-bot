---
name: resume-tailor
description: Analyze a job description against an existing resume, suggest targeted improvements, and apply approved changes.
disable-model-invocation: true
---

Analyze a job description against the user's current resume. Suggest specific, justified changes that improve alignment with the target role. Apply only what the user approves.

---

## Input Contract

Gather three inputs from the user before starting analysis. Prompt for each if not already provided.

1. **Job description** (required) — The full text of the job posting. Ask the user to paste it or provide a file path.
2. **Current resume** (required) — The resume to tailor. Ask the user to paste it, provide a file path, or point to a file in the project.
3. **Supplementary material** (optional) — Any additional context that may surface relevant experience not captured in the current resume: brag docs, accomplishment lists, performance reviews, project notes, etc. Ask: "Do you have any additional documents (brag sheet, accomplishment list, project notes) that might contain relevant experience not in your current resume? If not, we'll work with what's in the resume."

Do not proceed to analysis until inputs 1 and 2 are confirmed.

---

## Workflow

### Step 1 — Analyze the job description

Extract and organize:

- **Must-haves** — explicit requirements (years of experience, specific technologies, credentials)
- **Nice-to-haves** — preferred or bonus qualifications
- **Key responsibilities** — what will this person actually do day-to-day?
- **Themes** — underlying priorities (e.g., performance, product ownership, scale, technical leadership, cross-functional work)
- **Keywords** — exact terms likely used by ATS or hiring managers

Present this analysis to the user. Ask: "Does this match your read of the role? Anything to add or correct?"

Wait for confirmation before proceeding.

### Step 2 — Assess the current resume

Review the resume against the JD analysis from Step 1. Produce:

- **Strengths** — where the resume already aligns well with the JD (be specific: cite the bullet or section)
- **Gaps** — JD requirements that have weak or no coverage in the resume
- **Noise** — resume content that is irrelevant to this role and could be cut or deprioritized to make room

For each gap, check the supplementary material (if provided) for relevant experience that could fill it. Note which gaps can be addressed with existing material and which cannot.

Present this assessment to the user before proceeding.

### Step 3 — Propose changes

Produce a numbered list of suggested changes. Each suggestion must include:

1. **What** — the specific change (reword, add, remove, reorder)
2. **Where** — which section or bullet it applies to (quote the original text)
3. **Proposed text** — the new or revised wording (if applicable)
4. **Why** — how this change improves alignment with the JD (reference the specific requirement, theme, or keyword it addresses)

Categories of changes:

- **Reword** — rephrase existing bullets to mirror JD language or emphasize relevant impact
- **Add** — new bullets drawn from supplementary material to fill identified gaps
- **Remove** — cut or shorten content that is not relevant to this role
- **Reorder** — move bullets or sections to lead with the most JD-relevant content
- **Summary/Skills adjustment** — update summary or skills sections to speak to the role's themes

Rules:
- Never fabricate experience, metrics, titles, or credentials
- If proposing a metric that isn't in the source material, mark it `[ESTIMATE — validate]`
- Rewordings must preserve the factual content of the original bullet
- Keep format ATS-friendly: plain headings, no tables, no columns, consistent bullet style

Present the full list and ask the user to approve, reject, or modify each suggestion. Use the numbering for easy reference (e.g., "approve 1-3, 5; reject 4; modify 6 to ...").

### Step 4 — Apply approved changes

After the user has approved (or modified) the suggestions:

1. Ask: "Should I apply these changes to your existing resume file, or create a new version?" If creating a new version, ask what the file should be named.
2. Apply only the approved changes. Do not make additional edits beyond what was approved.
3. Present the final result for review.

---

## Output Contract

- A modified or new resume file containing only approved changes
- No separate "changes" file — all rationale is discussed during the conversation
