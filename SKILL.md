---
name: research-first
description: >-
  Research-first engineering. Before designing features or solving problems,
  systematically search for existing solutions in official docs, open source repos,
  and reference implementations. Learn the COMPLETE pattern (lifecycle, error handling,
  edge cases) not just surface APIs. Use when the user proposes new features, system
  design, technology selection, or any non-trivial implementation task. Triggers on
  feature requests, architecture questions, tech selection, how-to questions, and
  problem solving. Skip for trivial fixes (typos, config values, one-line changes).
---

# Research-First Engineering

## Core Principle

**Before writing code, exhaust existing knowledge.**

Every non-trivial task has been solved before. The biggest mistake is building from
mental models instead of reference implementations.

## Decision Tree: Should I Research?

Before starting, assess the task:

```
Is the task...
├─ A one-line fix, typo, or config value change? → SKIP research, just do it
├─ A well-known pattern I've done many times before? → LIGHT research (Phase 2 only)
└─ A new feature, design, tech choice, or unknown domain? → FULL research (all phases)
```

If in doubt, do full research. The cost of researching before building is always lower
than the cost of rewriting after discovering a reference implementation.

## Research Workflow

### Phase 1: Define the Question

Clarify before searching:

1. **What are we building?** — one sentence
2. **What's the hard part?** — the unknown or risky parts
3. **What would "done" look like?** — concrete success criteria

### Phase 2: Multi-Source Search

Search ALL sources in priority order:

| Priority | Source | Method |
|----------|--------|--------|
| 1 | **Official docs** | WebSearch `{technology} official docs {topic}` or use context7 MCP |
| 2 | **Reference implementations** | WebSearch `github {topic} production example` |
| 3 | **Source code** | Read the actual repo files. NOT blog summaries. |
| 4 | **Specs & RFCs** | If a protocol/standard exists, read the spec |
| 5 | **Community** | GitHub issues, official forums, Stack Overflow (last resort) |

**Rule**: Never cite a blog post as primary evidence. Trace back to source code or official docs.
**Rule**: Find at least TWO independent reference implementations for important decisions.

### Phase 3: Learn the COMPLETE Pattern

Extract the full pattern from references, not just the happy path:

1. **Data model** — What tables/fields/schemas/structures exist?
2. **Lifecycle** — What happens at startup → runtime → shutdown?
3. **Error handling** — What errors are caught? How are they recovered?
4. **Edge cases** — What boundary conditions does it handle? (empty, null, race, timeout, large input)
5. **Configuration** — What's configurable vs hardcoded?
6. **Tests** — What does the test suite cover? What test patterns are used?
7. **Dependencies** — What does it depend on? What depends on it?

### Phase 4: Judge Readiness

Before implementing, check ALL boxes:

- [ ] Found at least ONE production-grade reference (not a tutorial)
- [ ] Read the official docs for the core API
- [ ] Identified at least 3 edge cases I would have missed
- [ ] Understand the error handling strategy (retry? backoff? circuit breaker?)
- [ ] Know what the reference does DIFFERENTLY from my initial mental model

**If any box is unchecked → go back to Phase 2.**

### Phase 5: Output Findings

After research, output a structured summary before writing code:

```
## Research Summary: [Topic]

**References found:**
- [Project Name](URL) — [one-line description of relevance]
- [Project Name](URL) — [one-line description of relevance]

**Key patterns to adopt:**
1. [Pattern] — from [source]
2. [Pattern] — from [source]

**Edge cases to handle:**
1. [Edge case] — how reference handles it
2. [Edge case] — how reference handles it

**What I initially got wrong:**
- [Mental model correction based on research]

**Implementation approach:**
[Brief summary of the approach, citing which reference to follow]
```

Then ask the user: "Based on this research, should I proceed with implementation?"

## Depth Checklist (for each reference)

```
Project: [name + GitHub URL]
Core files: [3-5 key source files]
Key patterns:
  - Data model:
  - Lifecycle: startup → runtime → shutdown
  - Error handling: retry? backoff? circuit breaker?
  - Edge cases handled: [list 3+]
  - What I would have missed: [most important finding]
Relevance: [1-5, how applicable to our task]
```

## Common Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Reading only README | Read source code + test files |
| Copying API without lifecycle | Find production deployment configs |
| Learning one implementation | Find 2+ independent implementations |
| Skipping official docs | RTFM first, examples second |
| Building from blog posts | Trace back to source code |
| Not recording findings | Write structured research summary immediately |
| Researching forever without acting | Phase 4 checklist is the gate — when all boxes checked, START |

## Tool Usage During Research

- **context7 MCP**: Query official docs for any library/framework. Use FIRST.
- **WebSearch + WebFetch**: Find reference implementations, read source files
- **Explore agent**: Fan-out search across reference repos for specific patterns
- **Knowledge cards / project docs**: Record findings in whatever documentation system the project uses
