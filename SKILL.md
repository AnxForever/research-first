---
name: research-first
description: >-
  Research before coding. When the user is about to DESIGN or WRITE code for a
  non-trivial task, systematically search for existing solutions in official docs,
  open source repos, and reference implementations. Learn complete patterns (lifecycle,
  error handling, edge cases) from at least 2 independent sources before implementing.
  Triggers on: feature requests ("add X", "implement X"), system design, tech selection,
  non-trivial bug fixes, optimization, refactoring, integration tasks, and "how to
  implement X" questions. Does NOT trigger on: running tests, viewing output, git
  operations, explaining code, starting servers, one-line fixes, or config changes.
---

# Research-First Engineering

**Don't write code until you've found how others already solved it.**

## TL;DR (30 seconds)

```
1. READ the project first            → Phase 0
2. EXPAND the question (10 angles)    → Phase 1
3. SEARCH with quality filters        → Phase 2
4. EXTRACT patterns from ≥2 refs      → Phase 3
5. DECIDE: reuse, adapt, or learn?    → Phase 4
6. CHECK 10 boxes before coding       → Phase 5
7. REPORT findings to user            → Phase 6
```

## Adaptive Depth

Not every task needs full research. Match depth to situation:

| Scenario | Time | Depth | Skip Phases |
|----------|------|-------|-------------|
| Hotfix / 5min | < 5 min | Quick search, one ref | 1, 3-5 |
| Feature / 30min | 15-30 min | Two refs, key dimensions | — |
| Architecture / 2hr | 1-2 hours | Full 10-dimension, ≥3 refs | — |
| Unknown domain | +30 min extra | Add exploratory search first | — |

**Default**: if unsure, start medium. If Phase 2 finds nothing useful within 3 searches, ask the user whether to expand or proceed with best-effort.

## Phase 0: Understand the Project

Read: CLAUDE.md, README, ARCHITECTURE.md, core source files, tech stack, code conventions, known issues (TODOs, FIXMEs).

Output: one-paragraph project map (name, stack, architecture, conventions, problems).

## Decision Tree

```
├─ One-line fix, typo, config? → SKIP
├─ Familiar pattern? → LIGHT (Phase 2 only, one ref)
└─ New feature, design, unknown? → FULL (all phases)
```

## Phase 1: Expand the Problem

The surface question is never the whole problem. "Add X" = "add X correctly, securely, efficiently, maintainably." Expand across these dimensions:

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

## When Things Go Wrong

| Situation | Response |
|-----------|----------|
| No good references found | Report to user with options. Don't silently proceed. |
| References contradict | Follow [contradictions.md](references/contradictions.md): prioritize by stack match, maintenance, test coverage. |
| Time running out | Drop to lighter depth tier. Focus on highest-risk dimensions (security, lifecycle). |
| Completely unfamiliar domain | Add exploratory phase: search `"{domain} fundamentals architecture"` before Phase 1. |
| User says "still too shallow" | Re-verify ALL Phase 5 checkboxes immediately. Expand to 10/10 dimensions. |

→ Full failure mode catalog: [adapting-depth.md](references/adapting-depth.md)
