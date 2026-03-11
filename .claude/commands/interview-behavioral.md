# Skill: interview-behavioral

Build a story bank of STAR-structured behavioral answers and run mock behavioral interviews.

---

## Input Contract

Accept any of:
- A list of situations or accomplishments the user wants to use as stories
- A target role or company (to weight which themes matter most)
- A specific behavioral question to work on
- A request to run a mock interview

If nothing is provided, start by building the story bank.

---

## Workflow

### Mode A — Build story bank

#### Step 1 — Identify stories

Ask the user to brainstorm situations across these themes (aim for 10–15 stories total):

- Impact: shipped something significant, improved a key metric
- Technical leadership: drove an architectural decision, led a migration
- Cross-functional collaboration: worked with PM, design, data, or other teams
- Conflict or disagreement: navigated a technical or interpersonal disagreement
- Failure or setback: something that didn't go well and what you learned
- Ambiguity: made progress without clear requirements or direction
- Mentorship or growth: helped someone else grow, or grew significantly yourself
- Prioritization under pressure: hard tradeoffs, tight deadlines

For each, collect: rough situation, rough outcome, and which role it came from.

#### Step 2 — Draft STAR outlines

For each story, produce a STAR outline:
- **Situation** (1–2 sentences): context and stakes
- **Task** (1 sentence): your specific responsibility
- **Action** (3–5 sentences): what you did, why, and key decisions made
- **Result** (1–2 sentences): measurable or observable outcome; include impact on team, product, or users

Mark any results that need user validation with `[VALIDATE]`.

#### Step 3 — Polish into narratives

Convert each STAR outline into a 90–120 second verbal answer. Optimize for:
- Clear opening that establishes stakes quickly
- Specific technical or organizational detail (not vague platitudes)
- Self-awareness in the result (what would you do differently?)

---

### Mode B — Mock interview

Ask the user: "Should I focus on a specific theme, or run a mixed set?"

Run one question at a time:
1. Ask a realistic behavioral question
2. Wait for the user's answer
3. Evaluate on:
   - STAR structure (clear S, T, A, R?)
   - Specificity (real detail vs. vague generalities?)
   - Impact clarity (is the result meaningful and credible?)
   - Pacing (too long, too short, or about right for 90 seconds?)
4. Offer 2–3 specific improvements
5. Optionally ask the user to retry with the feedback applied

Repeat until the user ends the session.

---

## Output Contract

Story bank: a Markdown document with all STAR outlines organized by theme.
Mock interview: inline feedback per answer; no persistent artifact unless the user asks for a summary.
