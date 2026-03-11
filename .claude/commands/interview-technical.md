# Skill: interview-technical

Run Android technical interview prep: baseline assessment, question banks, and practice loops.

---

## Input Contract

Accept any of:
- A target role or JD (to calibrate question difficulty and focus areas)
- A specific topic to drill (e.g., "Compose internals", "coroutines", "system design")
- A request to run a quiz or mock technical interview
- A baseline assessment request

If nothing is provided, start with the baseline assessment.

---

## Workflow

### Mode A — Baseline assessment

Ask the user to self-rate (strong / working knowledge / needs work / unfamiliar) across:

**Core Android**
- Activity/Fragment lifecycle, configuration changes
- Jetpack Compose vs. Views: when to use each, interop
- Background work: WorkManager, coroutines, services
- Intents, broadcast receivers, content providers

**Architecture**
- MVVM, MVI, Clean Architecture
- Dependency injection (Hilt/Dagger)
- Modularization: by feature vs. by layer
- Navigation (Compose Navigation, Jetpack Nav)

**Kotlin**
- Coroutines and Flow (structured concurrency, operators, channels)
- Extension functions, sealed classes, data classes, generics
- Kotlin Multiplatform (awareness level)

**Testing**
- Unit testing with JUnit, MockK/Mockito
- UI testing with Espresso, Compose testing APIs
- Test doubles: mocks vs. fakes vs. stubs
- Instrumentation vs. unit tests

**Performance & Reliability**
- ANR causes and prevention
- Memory leaks (LeakCanary, common patterns)
- Rendering performance (frames, recomposition)
- Offline-first patterns, caching, conflict resolution

**Build & Tooling**
- Gradle: build variants, custom tasks, dependency management
- CI/CD pipelines for Android
- Profiling tools (Android Studio Profiler, systrace)

After self-rating, identify the top 2–3 weak areas and prioritize them for practice.

---

### Mode B — Question bank

Generate questions by category and difficulty. For each question:
- State the question
- Wait for user answer (in quiz mode) OR provide the answer immediately (in study mode)
- In quiz mode: evaluate correctness, fill gaps, offer a follow-up question to go deeper

**Sample categories and representative questions:**

Lifecycle:
- "What happens to a ViewModel when the system kills the process vs. a configuration change?"
- "How would you handle saving and restoring UI state in Compose?"

Coroutines/Flow:
- "What's the difference between `StateFlow` and `SharedFlow`? When would you use each?"
- "How does structured concurrency prevent coroutine leaks?"

Architecture:
- "How would you structure a feature module to be independently testable?"
- "Walk me through how you'd implement offline-first data sync."

System design:
- "Design the architecture for a news feed with infinite scroll, offline support, and real-time updates."
- "How would you architect a reusable analytics SDK for Android?"

---

### Mode C — System design practice

For each prompt:
1. Give the user 2–3 minutes to outline their approach (or ask them to write it out)
2. Evaluate:
   - Did they clarify requirements before designing?
   - Did they consider tradeoffs (network vs. local, caching strategy, testing approach)?
   - Is the architecture layered and testable?
   - Did they account for Android-specific constraints (battery, memory, lifecycle)?
3. Provide a reference approach and note where the user's answer diverged

---

## Output Contract

Inline feedback per question/answer. Persistent artifact only if user requests a study sheet or summary of weak areas.
