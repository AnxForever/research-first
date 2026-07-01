---
name: research-first
description: >-
  Universal project improvement skill. Before modifying any project, first understand
  its features, architecture, and problems by reading its docs and source code. Then
  proactively search for existing solutions — official documentation, open source
  implementations, reference architectures — and reuse proven code instead of writing
  from scratch. Learn the COMPLETE pattern (lifecycle, error handling, edge cases, security)
  from at least 2 independent references before implementing. Use when the user asks to
  add features, fix problems, optimize, refactor, or improve any project. Triggers on
  feature requests, bug reports, architecture questions, performance issues, and any
  non-trivial code change.
---

# Research-First Project Improvement

## Core Principle

**Don't write code until you've found how others already solved it.**

Every project problem has been solved before — in official docs, open source repos,
or production systems. The cost of reading references is always lower than the cost
of rewriting bad code.

This skill works on ANY project: read the project first, then search the world for
answers, then implement based on proven patterns.

## Phase 0: Understand the Project

Before researching solutions, understand what you're working with:

1. **Read project identity files**: CLAUDE.md, README.md, CONTRIBUTING.md, ARCHITECTURE.md
2. **Read key docs**: Look for `docs/` directory, design documents, API specs
3. **Scan core source files**: Identify the main modules, entry points, and critical paths
4. **Identify the tech stack**: Language, framework, database, key dependencies
5. **Note existing patterns**: Code style, naming conventions, error handling patterns, test style
6. **Find known problems**: Check TODO comments, FIXME markers, issue trackers, recent commits

Output a brief project map:
```
Project: [name]
Stack: [language, framework, database, key deps]
Architecture: [monolith/microservices/etc., key modules]
Existing patterns: [code style, error handling, testing]
Problems to solve: [what user asked + what you found]
```

## Decision Tree: How Deep to Research?

```
Is the task...
├─ A one-line fix, typo, config value? → SKIP research, just do it
├─ A well-known pattern in the project's stack? → LIGHT (Phase 2 only)
└─ New feature, design, optimization, or unknown domain? → FULL (all phases)
```

If in doubt, do full research.

## Phase 1: Define What to Search For

Map the project's need to specific search queries:

| Project need | Search queries |
|-------------|---------------|
| "Add X feature" | `"{tech stack} {feature} production implementation github"` |
| "Fix Y problem" | `"{tech stack} {problem} best practice solution"` |
| "Optimize Z" | `"{tech stack} {component} performance optimization pattern"` |
| "Design architecture" | `"{domain} system design architecture reference"` |
| "Add integration" | `"{service} official docs integration guide"` |

Be specific: include the language, framework, and domain in every query.

## Phase 2: Multi-Source Search

Search ALL these sources. For FULL research, minimum requirements are marked:

| Priority | Source | Method | Required? |
|----------|--------|--------|-----------|
| 1 | **Official docs** | WebSearch `{tech} official docs {topic}`, context7 MCP | YES |
| 2 | **Reference implementations** | WebSearch `github {topic} production` | YES — ≥ 2 repos |
| 3 | **Specs & standards** | RFCs, protocol specs, agentskills.io, framework docs | If exists |
| 4 | **Source code** | Read actual files in reference repos. NOT just README. | YES — ≥ 2 core files |
| 5 | **Tests** | Read test files in reference repos. They document edge cases. | Recommended |
| 6 | **Issues & discussions** | GitHub issues, official forums | Optional |

**Rules**:
- Never cite a blog post as primary evidence. Blog posts skip error handling.
- If a standard exists (agentskills.io, RFC, OWASP), read it.
- For any reference repo you find: clone it or read at least 2 source files + 1 test file.

## Phase 3: Learn the COMPLETE Pattern

For each reference implementation, extract ALL dimensions. If you can't fill every field,
you haven't gone deep enough — find another reference or read more source code:

1. **Data model** — Structures, schemas, fields, relationships
2. **Lifecycle** — startup → runtime → shutdown for EVERY component
3. **Error handling** — What errors are caught? Retry? Backoff? Circuit breaker? Graceful degradation?
4. **Edge cases** — Empty/null/missing data, race conditions, timeouts, large inputs, concurrent access
5. **Configuration** — What's configurable vs hardcoded? Environment-specific behavior?
6. **Tests** — What patterns? What edge cases do tests cover? What do they NOT test?
7. **Security** — What threats? Input validation? AuthN/AuthZ? Data sanitization? Injection prevention?
8. **Integration** — How does it connect to other systems? What are the failure modes?
9. **Performance** — Bottlenecks? Caching? Lazy loading? Batching?
10. **What surprised me** — The ONE finding that contradicted my initial assumption

**SELF-CHECK before Phase 4**:
> "Can I draw the complete architecture diagram, trace every error path, and name
> 5 edge cases the reference handles that I would have missed on my own?"

If NO → go back to Phase 2.

## Phase 4: Evaluate and Decide

For each reference, evaluate whether to REUSE, ADAPT, or LEARN-FROM:

| Criteria | Reuse | Adapt | Learn-from |
|----------|-------|-------|-----------|
| License compatible? | ✓ | ✓ | Any |
| Same language/framework? | ✓ | Similar | Any |
| Same scale/requirements? | ✓ | Close | Different |
| Actively maintained? | ✓ | If stable | Any |
| Code quality matches project? | ✓ | With cleanup | For patterns only |

**Decision**: Choose the best reference to follow. Prefer REUSE over ADAPT over LEARN-FROM.
Document WHY you chose this approach.

## Phase 5: Judge Readiness

ALL boxes must be checked before writing a single line of code:

- [ ] Read the project's own docs and key source files (Phase 0)
- [ ] Found at least 2 independent production references (NOT tutorials)
- [ ] Read source code from at least 2 core files in each reference
- [ ] Read the official documentation for the core API/library
- [ ] Identified at least 5 edge cases the references handle
- [ ] Understand the complete lifecycle (startup → runtime → shutdown → error recovery)
- [ ] Can name at least ONE surprising finding that changed my approach
- [ ] Identified at least ONE security consideration
- [ ] Evaluated whether to reuse, adapt, or learn-from each reference (Phase 4)
- [ ] The solution fits the project's existing code style and conventions

**HARD GATE: any box unchecked → go back. Do NOT start Phase 6.**

## Phase 6: Output Structured Findings

Use this EXACT template before writing code:

```
## Research Summary: [Problem Being Solved]

### Project Context
[What I learned from Phase 0 about this project's architecture and conventions]

### References Found
1. **[Project Name](URL)**
   - Files read: [list 2+ file paths you actually opened]
   - Key insight: [one sentence]
   - Reuse/Adapt/Learn-from: [decision + reason]

2. **[Project Name](URL)**
   - Files read: [list 2+ file paths you actually opened]
   - Key insight: [one sentence]
   - Reuse/Adapt/Learn-from: [decision + reason]

### Complete Pattern
- Data model: [describe]
- Lifecycle: [startup → runtime → shutdown]
- Error handling: [strategy]
- Security: [threats + defenses]

### Edge Cases Discovered (minimum 5)
1. [Edge case] → reference handles it by [mechanism]
2. ...

### What I Initially Got Wrong
- [Mental model correction based on reading source code]

### Implementation Plan
1. [Step] — following [reference]
2. [Step] — following [reference]
3. [Step] — adapted for project conventions
```

Then ask: **"Based on this research, proceed with implementation?"**

## Failure Modes

| Failure | Symptom | Prevention (hard gate) |
|---------|---------|----------------------|
| Skipping Phase 0 | Solution doesn't match project style | Phase 5 box 1: read project first |
| Surface research | Can't fill Phase 3 dimensions | Phase 3 self-check question |
| One-source bias | Only found one reference | Phase 2 minimum: 2 repos |
| Tutorials instead of source | No error handling in plan | Phase 2 priority 4: read source code |
| Ignoring license | Can't legally reuse code | Phase 4 license check |
| Ignoring security | Vulnerable implementation | Phase 3 item 7 + Phase 5 box 8 |
| Wrong abstraction level | Over-engineered or too simple | Phase 0: understand project scale |
| User calls out shallowness | "You're still doing surface research" | Re-verify Phase 5 checklist immediately |

## Self-Improvement

This skill improves with use. After each research session:

1. Note what failed — too shallow? wrong sources? missed project context?
2. Update this SKILL.md if a pattern can prevent the same mistake
3. Add examples to `references/examples.md`

## Tool Usage

- **Read/Glob/Grep**: Phase 0 — understand the project
- **context7 MCP**: Official docs for any library. Use FIRST in Phase 2.
- **WebSearch**: Find reference implementations + specs
- **WebFetch**: Read source files from reference repos
- **Explore agent**: Fan-out search across multiple reference repos
