---
name: research-first
description: >-
  Research before doing. Whenever the user wants to create, build, write, design, plan,
  decide, or solve something — code, documents, presentations, workflows, strategies,
  anything — systematically search for how others already did it better. Find what the
  best practitioners do, study their methods, extract reusable patterns, and adapt them.
  Applies to: writing (docs, emails, proposals), designing (UI, workflows, systems),
  building (features, products, tools), planning (projects, roadmaps, architecture),
  deciding (tech choices, strategies, tradeoffs). Does NOT trigger for: simple lookups,
  running commands, viewing files, one-line fixes, or conversational chat. The key
  question: is the user trying to PRODUCE something that could benefit from knowing
  how others already did it?
---

# Research-First

**Before you create anything, find how others already did it better.**

This skill applies to ANY task — writing, designing, building, planning, deciding.
The methodology is the same; only the sources change.

## TL;DR (30 seconds)

```
0. UNDERSTAND project identity        → Phase 0 (WHO? WHY?)
1. EXPAND the question (10 angles)    → Phase 1 (through identity lens)
2. SEARCH — backend: source code,     → Phase 2 (2A-2E)
   frontend: big players, components, → Phase 2F (design research)
   design systems, open source reuse
3. EXTRACT patterns from ≥2 refs      → Phase 3
4. DECIDE: reuse, adapt, or learn?    → Phase 4
5. CHECK 11 boxes before coding       → Phase 5
6. REPORT findings to user            → Phase 6
7. SELF-AUDIT before saying "done"    → Phase 7
```

## Frontend/Design Research (Phase 2b)

When the task involves UI design, frontend components, or visual layout, add
this sub-phase after Phase 2 (Search). Design is NOT purely aesthetic — it
directly impacts usability, trust, and conversion.

### 2b.1 Research "Who Already Solved This UI Problem"

For ANY frontend task, search these dimensions in parallel:

| Dimension | Search For | Example Queries |
|-----------|-----------|----------------|
| **Big players** | How do ChatGPT/Claude/Gemini design this? | "ChatGPT chat interface layout components 2025" |
| **Design systems** | Existing style guides, component libraries | "Ant Design chat component", "shadcn/ui chat bubble" |
| **Competitors** | How do similar products solve this? | "open source AI data analysis platform UI" |
| **Design trends** | What's the 2025 standard for this pattern? | "AI chat interface design patterns 2025 best practices" |
| **Open source** | Can we reuse existing components? | "React chat UI component MIT license" |

### 2b.2 Extract Design Patterns

From ≥2 references, extract:

- **Layout**: sidebar + main + input? Full-screen chat? Dashboard widgets?
- **Component hierarchy**: what components are used, how are they nested?
- **Interaction patterns**: streaming, drag-drop, keyboard shortcuts, mobile
- **Visual language**: colors, typography, spacing, shadows, rounded corners
- **States**: loading, empty, error, success — how does each look?

### 2b.3 Frontend-Specific Decision Framework

| If... | Then... |
|-------|---------|
| Major AI products all use the same pattern | **Adopt it.** Users expect familiarity (Jakob's Law) |
| Open source component exists (MIT/Apache) | **Reuse or adapt.** Don't rebuild chat bubbles from scratch |
| Pattern is unique to one product | **Evaluate.** Is it core to their brand or a UX innovation? |
| No clear standard exists | **Simplify.** Default to minimal, add complexity only when needed |

### 2b.4 Anti-Patterns (Frontend)

- ❌ Designing UI without first checking how ChatGPT/Claude do it
- ❌ Building custom chat bubbles when shadcn/ui has them
- ❌ Ignoring the "left sidebar + chat + bottom input" standard layout
- ❌ Skipping mobile/tablet layout planning
- ❌ No empty/loading/error state design before coding
- ❌ Dark mode as afterthought — it's expected in 2025

## Adaptive Depth

Not every task needs full research. Match depth to situation:

| Scenario | Time | Depth | Approach |
|----------|------|-------|----------|
| Quick task (fix, tweak, short doc) | < 5 min | Quick search, one ref | Phase 2 only |
| Standard task (feature, doc, design) | 15-30 min | Two refs, key dimensions | Full phases |
| Major work (architecture, strategy) | 1-2 hours | Full 10-dimension, ≥3 refs | All phases + deep dive |
| Creative work (writing, design, planning) | +15 min extra | Phase 2F — study best examples first | Add creative research |
| Unknown domain | +30 min extra | Exploratory search first | Add before Phase 1 |

**Default**: if unsure, start medium. If Phase 2 finds nothing useful within 3 searches, ask the user whether to expand or proceed with best-effort.

## Phase 0: Understand the Project Identity

Don't just read files — understand what this project IS. The project's identity
determines what "good" looks like for every feature you add.

### 0A. Identity Questions

Answer these before any research. Don't guess — find answers in the codebase:

| Question | Look in |
|----------|---------|
| **What problem does this solve?** | README, docs, landing page |
| **Who uses it? At what scale?** | Config, deployment docs, user guides |
| **What are the hard constraints?** | Security, performance, compliance, budget |
| **What makes it different?** | ARCHITECTURE.md, design docs, ADRs |
| **What's the team's expertise?** | Tech stack choices, code conventions |
| **What keeps the maintainer up at night?** | Issues, TODOs, error handling patterns |

### 0B. Output: Project Identity Card

```
Project: [name]
Problem it solves: [one sentence — the WHY, not the WHAT]
Users & scale: [who, how many, what context]
Hard constraints: [security? performance? compliance? cost?]
Differentiators: [what makes this project unique vs alternatives]
Tech DNA: [stack + why they chose it]
Pain points: [what breaks most often? what's the hardest part?]
```

### 0C. Identity as a Research Lens

The identity card is NOT just documentation. It's a LENS you use in every subsequent phase.
For every search query, every reference evaluation, every design decision — ask:

> "Given that this project is [identity], does this solution fit?"

**Example: Same feature, different projects → different research**

```
Feature: "Add caching layer"

Project A: AgentOS (AI agent platform)
→ Search: "caching LLM responses agent platform"
→ Search: "context window cache strategy AI agents"
→ Search: "multi-tenant cache isolation agent systems"
→ Concern: cache invalidation when agent state changes

Project B: E-commerce (high-concurrency transactions)
→ Search: "Redis hotkey solution production e-commerce"
→ Search: "cache-stock consistency pattern"
→ Search: "flash sale cache warming strategy"
→ Concern: data consistency during concurrent writes
```

Same feature. Same tech stack. But the project identity changes WHAT you search for
and WHICH patterns are relevant.

**Rule: Before every search query, prefix it mentally with "For a [project type] that [solves X]..."**


## Decision Tree

```
├─ One-line fix, typo, config? → SKIP
├─ Familiar pattern? → LIGHT (Phase 2 only, one ref)
└─ New feature, design, unknown? → FULL (all phases)
```

## Phase 1: Expand the Problem (through the identity lens)

The surface question is never the whole problem. "Add X" = "add X correctly, securely, efficiently, maintainably." Expand across these dimensions, filtering each through the project identity from Phase 0:

| # | Dimension | Ask |
|---|-----------|-----|
| 1 | Data | Schema? Storage? Validation? Migration? |
| 2 | Lifecycle | Startup? Shutdown? Crash recovery? |
| 3 | Integration | How connect to existing? Failure modes? |
| 4 | Security | Attack vectors? AuthZ? Injection? |
| 5 | Performance | Bottlenecks? Scaling limits? |
| 6 | Observability | Monitoring? Logging? Debugging? |
| 7 | API/UX | Contract? User interaction? |
| 8 | Configuration | Configurable? Env differences? |
| 9 | Testing | Strategy? Edge cases? |
| 10 | Evolution | Versioning? Backward compat? |

Expand at least 6 dimensions. Each generates 1-3 search queries.
→ If unfamiliar with the domain, read [problem-expansion.md](references/problem-expansion.md) for detailed examples.

## Phase 2: Search with Quality

Search ≥3 sources. Priority: official docs → specs → source code → tests → issues → Stack Overflow → blogs (last resort).

**Rules**: ≥2 independent repos. Read ≥2 source files + ≥1 test file per repo. Never cite blogs as primary evidence.

**Quality filter** (before deep-diving): last commit < 1yr? license compatible? tests exist? maintainer responsive?

→ Full query construction, quality signals matrix, multi-angle coverage, and anti-patterns: [search-quality.md](references/search-quality.md)

**If search finds nothing**: after 3 varied queries with no good results, report to user: "No production references found for [topic]. Options: (1) broaden search, (2) proceed with best-effort from first principles, (3) reconsider approach." Do not silently proceed.

### 2F. Creative/Design Research (when task involves creating, not just coding)

When the task involves writing, designing, planning, or any creative output — not just code —
add this sub-phase. The best creators study the best work before making their own.

**Research "Who Already Did This Well"** — search these angles in parallel:

| Angle | What to Search | Example |
|-------|---------------|---------|
| **Best examples** | Who does this best? Study them. | "best developer documentation examples", "award-winning presentation design" |
| **Templates & frameworks** | Existing templates, structures, formats | "technical documentation template", "project plan framework" |
| **Style guides** | Established conventions and standards | "Google developer documentation style guide", "Apple HIG" |
| **Comparable work** | How do similar products/projects do this? | "open source project README examples", "startup pitch deck examples" |
| **Reusable assets** | Can we start from something existing? | "MIT licensed presentation template", "open source documentation theme" |

**Extract Patterns** — from ≥2 examples, extract:

- **Structure**: How is it organized? What's the information hierarchy?
- **Format**: What format works best? (markdown? slides? interactive? video?)
- **Tone & voice**: Formal? Casual? Technical? Accessible?
- **Visual approach**: Minimal? Rich? Data-heavy? Illustration-driven?
- **What makes the best examples stand out**: The ONE thing that elevates them

**Rules for creative research:**
- If a widely-adopted standard exists (e.g., Google style guide for docs) → follow it
- If an open-source template exists with compatible license → start from it
- If no standard exists → study 3 best examples and synthesize
- Never write from scratch when templates exist
- The best work always steals from the best — be deliberate about it

## Phase 3: Extract Complete Patterns

For each reference, extract: data model, lifecycle, error handling, edge cases, configuration, tests, security, integration, performance, and the one finding that surprised you.

→ Full 10-dimension checklist: [problem-expansion.md](references/problem-expansion.md)

**When two references disagree**: prioritize the one that (1) matches the project's language/framework, (2) is more actively maintained, (3) has better test coverage. Document the conflict and your choice in Phase 6.

## Phase 4: Evaluate Reuse

For each reference: **REUSE** (same stack, compatible license)→ **ADAPT** (similar stack, needs adjustment) → **LEARN-FROM** (different stack, patterns only).

→ License compatibility guide and decision matrix: [adapting-depth.md](references/adapting-depth.md)

## Phase 5: Verify Readiness

All boxes before any code:

- [ ] Read project docs and source (Phase 0)
- [ ] Expanded ≥6/10 dimensions (Phase 1)
- [ ] Found ≥2 independent references (Phase 2)
- [ ] Read ≥2 source files + 1 test file per reference
- [ ] Read official docs for core API
- [ ] Extracted all pattern dimensions (Phase 3)
- [ ] Identified ≥5 edge cases
- [ ] Found ≥1 security consideration
- [ ] Made reuse/adapt/learn-from decision (Phase 4)
- [ ] Solution fits project conventions

**Any box unchecked → go back. Do not proceed to Phase 6.**

## Phase 6: Report Findings

```
## Research Summary: [Problem]

### Project Context
[One paragraph from Phase 0]

### References
1. [Name](URL) — files read: [paths] — key insight — decision: REUSE|ADAPT|LEARN-FROM
2. [Name](URL) — files read: [paths] — key insight — decision: REUSE|ADAPT|LEARN-FROM

### Edge Cases (≥5)
1. [Case] → [mechanism]

### What I Got Wrong
[Assumption corrected by reading source code]

### Plan
1. [Step] — following [ref]
```

Then ask: **"Proceed with implementation?"**

## Phase 7: Self-Audit (BEFORE reporting done)

After implementation but BEFORE telling the user "done," run this audit.
The user should never have to catch these — you catch them first.

### 7A. Proactivity Check

Ask yourself honestly:

- [ ] Did the user have to point out anything I should have noticed myself?
- [ ] Did I stop at the surface question, or did I expand to the full problem space?
- [ ] Did I research before coding, or did I jump straight to implementation?
- [ ] Did I find and read source code from reference implementations?
- [ ] Are there remaining issues I know about but didn't mention?

**If the user would need to say "you forgot X" or "this is still shallow" → fix it NOW, before reporting.**

### 7B. Completeness Check

- [ ] All Phase 5 readiness boxes still hold after implementation?
- [ ] Did I handle all 10 problem dimensions, not just the obvious ones?
- [ ] Did I test my changes? (run tests, verify they pass)
- [ ] Did I update project documentation (CLAUDE.md, RESEARCH.md) with findings?
- [ ] Are there any TODO comments or stubs I left behind?

### 7C. Quality Check

- [ ] If a picky user reviewed this, would they find obvious gaps?
- [ ] Did I follow the project's existing code style and patterns?
- [ ] Did I handle error cases, not just the happy path?
- [ ] Is there anything I'm hoping the user won't notice?

### 7D. Red Flags

If ANY of these are true, do NOT report done. Fix first:

| Red Flag | Action |
|----------|--------|
| User previously said "you're still being shallow" | Double research depth. Re-verify all Phase 5 boxes. |
| I only searched one source | Go back to Phase 2. Find at least one more reference. |
| I didn't read any source code | Read at least 2 core files from a reference implementation. |
| I'm about to say "should I proceed?" without a research summary | Write the Phase 6 summary first. |
| There are tests I didn't run | Run them now. |
| I know about a related problem but didn't research it | Research it now. Don't wait for the user to ask. |

**If the audit reveals issues → fix them first. Only report done when all checks pass.**

---

## When Things Go Wrong

| Situation | Response |
|-----------|----------|
| No good references found | Report to user with options. Don't silently proceed. |
| References contradict | Follow [contradictions.md](references/contradictions.md): prioritize by stack match, maintenance, test coverage. |
| Time running out | Drop to lighter depth tier. Focus on highest-risk dimensions (security, lifecycle). |
| Completely unfamiliar domain | Add exploratory phase: search `"{domain} fundamentals architecture"` before Phase 1. |
| User says "still too shallow" | Re-verify ALL Phase 5 checkboxes immediately. Expand to 10/10 dimensions. |

→ Full failure mode catalog: [adapting-depth.md](references/adapting-depth.md)
