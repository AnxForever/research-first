---
name: research-first
description: >-
  Research before coding. Whenever the user wants to build, improve, fix, or design
  something in the codebase — any task that involves writing or modifying code beyond
  a trivial change — systematically search for how others already solved it. Find
  production references, read their source code, learn the complete pattern, and
  decide whether to reuse or adapt before implementing. Does NOT trigger for: running
  tests, viewing files, git operations, explaining code, one-line fixes, or operational
  commands (start/stop/restart). The key question: is the user about to write or
  design code for something they haven't built before?
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
