# Skill: resume-build

Build a master resume from raw career documents. This is the source-of-truth artifact that all tailored resumes derive from.

---

## Input Contract

Accept any combination of:
- Accomplishment docs / brag docs
- Performance reviews
- Old resumes (any format)
- Freeform notes or bullet dumps

If nothing is provided, ask: "Please paste or attach your accomplishment docs, old resume, or any notes about your work history."

---

## Workflow

### Step 1 — Parse and normalize

Extract from all inputs:
- Roles, companies, and employment dates
- Tech stack per role (languages, frameworks, tools, platforms)
- Key responsibilities vs. key accomplishments (distinguish between the two)

Flag anything ambiguous (e.g., overlapping dates, unclear titles, missing employers) and ask the user to clarify before proceeding.

### Step 2 — Extract and sharpen achievements

For each role, produce 5–10 achievement bullets. Prioritize:
- Impact (what changed because of your work?)
- Ownership (did you lead, drive, or own this?)
- Difficulty (was this technically complex or organizationally hard?)

Formatting rules for bullets:
- Start with a strong action verb (Architected, Reduced, Shipped, Led, Migrated, etc.)
- Include a quantified result where possible — if the user's docs don't have numbers, propose a plausible range or format and mark it `[ESTIMATE — validate]`
- Keep each bullet to 1–2 lines

Never invent metrics. If quantification is unclear, write the bullet qualitatively and note: `[Add metric if available]`.

### Step 3 — Assemble the master resume

Structure:

```
# [Name]
[Location if desired] | [Email] | [Phone] | [LinkedIn] | [GitHub]

## Summary
2–4 sentences. Android-focused. Highlights years of experience, key technical strengths, and one differentiating trait.

## Skills
Languages: Kotlin, Java, [others]
Frameworks & Libraries: Jetpack Compose, Coroutines, Retrofit, Room, [others]
Architecture: MVVM, Clean Architecture, Modularization, [others]
Testing: JUnit, Espresso, Mockito, [others]
Tools & Platforms: Android Studio, Gradle, Firebase, CI/CD, [others]

## Experience
[Reverse chronological. Company, Title, Dates. 5–8 bullets per role.]

## Projects (if applicable)
[Open source, personal apps, or notable side projects with links.]

## Education
[Degree, institution, year — brief.]
```

### Step 4 — Review and confirm

Present the draft and ask the user to:
1. Verify all metrics and estimates marked `[ESTIMATE]`
2. Confirm titles are accurate and formatted as desired
3. Flag anything missing or misrepresented

Incorporate corrections. This final version is the master resume.

---

## Output Contract

Deliver: a single Markdown document titled `master-resume.md` (or equivalent) that is complete, factual, and ready to be used as input to `resume-tailor`.
