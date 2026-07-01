---
name: research-first
description: >-
  Research-first engineering. Before designing features or solving problems,
  systematically search for existing solutions in official docs, open source repos,
  and reference implementations. Learn the COMPLETE pattern (lifecycle, error handling,
  edge cases) not just surface APIs. Record findings as knowledge cards. Use when the
  user proposes new features, system design, technology selection, or any non-trivial
  implementation task. Triggers on feature requests, architecture questions, tech
  selection, problem solving.
---

# Research-First Engineering

## Core Principle

**Before writing a single line of code, exhaust existing knowledge.**

Every non-trivial task has been solved before — in official docs, open source repos, or production systems.
The biggest engineering mistake is building from mental models instead of reference implementations.

If you are reading this, the skill already triggered. Follow the workflow below.

## Research Workflow

### Phase 1: Define the Question

Before searching, clarify:

1. **What are we building?** — one sentence
2. **What's the hard part?** — the unknown or risky parts  
3. **What would "done" look like?** — concrete success criteria

### Phase 2: Multi-Source Search

Search ALL sources, not just one. Priority order:

| Priority | Source | Method |
|----------|--------|--------|
| 1 | **Official docs** | WebSearch for `{tech} official docs {topic}` or context7 MCP |
| 2 | **Reference implementations** | WebSearch for `github {topic} production example 2025` |
| 3 | **Source code** | Clone/read the actual repo. NOT blog summaries. |
| 4 | **Specs & RFCs** | If a protocol/standard exists, read the spec |
| 5 | **Community** | GitHub issues, official forums. Blog posts as LAST resort. |

**Rule**: Never cite a blog post as primary evidence. Always trace back to source code or official docs.

### Phase 3: Learn the COMPLETE Pattern

After finding reference implementations, extract the COMPLETE pattern:

1. **Data model** — What tables/fields/schemas exist?
2. **Lifecycle** — What happens at startup → runtime → shutdown?
3. **Error handling** — What errors are caught? How recovered?
4. **Edge cases** — What boundary conditions are handled? (empty, null, race, timeout)
5. **Configuration** — What's configurable vs hardcoded?
6. **Tests** — What does the test suite cover?
7. **Dependencies** — What does it depend on? What depends on it?

### Phase 4: Judge Readiness

Before starting implementation, check ALL boxes:

- [ ] Found at least ONE production-grade reference (not a tutorial)
- [ ] Read the official docs for the core API
- [ ] Identified at least 3 edge cases from the reference
- [ ] Understand the error handling strategy
- [ ] Know what the reference does DIFFERENTLY from my initial mental model

If any box is unchecked, go back to Phase 2.

### Phase 5: Record Findings as Knowledge Cards

After research, create knowledge cards (via mcp-enterprise API):

```bash
curl -X POST :8080/api/v1/knowledge-cards -H "Authorization: Bearer sk-mcp-dev" \
  -d '{"card_type":"technical","title":"[Topic] - key finding","content":"...","project_key":"agentos"}'
```

Card types: `decision` (why we chose X), `technical` (implementation pattern), `bug_fix` (gotcha to avoid)

## Depth Checklist

For each reference implementation:

```
Project: [name + GitHub URL]
Core files: [3-5 key source files]
Key patterns:
  - Data model:
  - Lifecycle: startup → runtime → shutdown
  - Error handling: retry? backoff? circuit breaker?
  - Edge cases handled: [list 3+]
  - What I would have missed: [most important finding]
Relevance: [1-5]
```

## Common Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Reading only README | Read source code + test files |
| Copying API without lifecycle | Find production deployment configs |
| Learning one implementation | Find 2+ independent implementations |
| Skipping official docs | RTFM first, examples second |
| Not recording findings | Write knowledge card immediately |

## Tool Usage

- **context7 MCP**: Query official docs for any library. Use FIRST.
- **WebSearch + WebFetch**: Find reference implementations, read source files
- **Explore agent**: Fan-out search across reference repos for patterns
- **mcp-enterprise**: Record findings as structured knowledge cards
