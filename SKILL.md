---
name: research-first
description: >-
  Research-first engineering. Before designing features or solving problems,
  systematically search for existing solutions in official docs, open source repos,
  and reference implementations. Learn the COMPLETE pattern (lifecycle, error handling,
  edge cases) by reading source code, not just blog posts. Output structured research
  summaries before writing code. Use when the user proposes new features, system
  design, technology selection, or any non-trivial implementation task. Triggers on
  feature requests, architecture questions, tech selection, how-to questions, and
  problem solving. Skip for trivial fixes (typos, config values, one-line changes).
---

# Research-First Engineering

## Core Principle

**Before writing code, exhaust existing knowledge.**

Every non-trivial task has been solved before. The biggest mistake is building from
mental models instead of reading reference implementations.

## Decision Tree: Should I Research?

```
Is the task...
├─ A one-line fix, typo, or config value change? → SKIP
├─ A well-known pattern I've done many times? → LIGHT (Phase 2 only)
└─ A new feature, design, tech choice, or unknown domain? → FULL (all phases)
```

If in doubt, do full research.

## Research Workflow

### Phase 1: Define the Question

1. **What are we building?** — one sentence
2. **What's the hard part?** — the unknown or risky parts
3. **What would "done" look like?** — concrete success criteria

### Phase 2: Multi-Source Search

Search ALL sources. Minimum 3 different sources for FULL research:

| Priority | Source | Method | Required for FULL? |
|----------|--------|--------|--------------------|
| 1 | **Official docs** | WebSearch `{tech} official docs {topic}`, context7 MCP | YES |
| 2 | **Reference implementations** | WebSearch `github {topic} production` | YES — at least 2 |
| 3 | **Specs & standards** | agentskills.io, RFCs, protocol specs | If exists |
| 4 | **Source code** | Read actual repo files (NOT README, NOT blog) | YES — at least 2 core files |
| 5 | **Community** | GitHub issues, official forums | Optional |

**Rules**:
- NEVER cite a blog post as primary evidence
- For FULL research: at least 2 independent implementations, at least 2 source files read
- If you can't find 2 references, say so explicitly — don't pretend one tutorial is enough

### Phase 3: Learn the COMPLETE Pattern

For each reference, extract ALL of these. If you can't fill in every item, you haven't gone deep enough:

1. **Data model** — What structures/schemas/fields exist?
2. **Lifecycle** — What happens at startup → runtime → shutdown?
3. **Error handling** — What errors are caught? Retry strategy? Circuit breaker?
4. **Edge cases** — Empty input? Null? Race conditions? Timeouts? Large data?
5. **Configuration** — What's configurable vs hardcoded?
6. **Tests** — What test patterns? What edge cases do tests cover?
7. **Security** — What threats does it defend against? What attacks is it vulnerable to?
8. **What I would have missed** — The single most surprising finding from this reference

**DEPTH CHECK — Before moving to Phase 4, ask yourself:**
> "If the user asked me to explain this system's COMPLETE architecture right now,
> could I draw the lifecycle diagram, list all error paths, and name 5 edge cases?"

If the answer is NO, you haven't gone deep enough. Go back to Phase 2.

### Phase 4: Judge Readiness

ALL boxes must be checked before writing code:

- [ ] Found at least 2 independent production-grade references (NOT tutorials)
- [ ] Read source code from at least 2 core files in the reference
- [ ] Read the official documentation for the core API
- [ ] Identified at least 5 edge cases I would have missed without research
- [ ] Understand the complete lifecycle (startup → runtime → shutdown)
- [ ] Know the error handling strategy (what fails, how it recovers)
- [ ] Can name at least ONE thing the reference does DIFFERENTLY from my initial plan
- [ ] Found at least ONE security consideration or attack vector

**If any box is unchecked → go back to Phase 2. Do NOT start Phase 5.**

### Phase 5: Output Structured Findings

Use this EXACT template:

```
## Research Summary: [Topic]

**References (minimum 2):**
- [Project Name](URL)
  - Core files read: [list 2+ file paths you actually read]
  - Key insight: [one sentence]
- [Project Name](URL)
  - Core files read: [list 2+ file paths you actually read]
  - Key insight: [one sentence]

**Complete architecture pattern:**
1. Data model: [describe]
2. Lifecycle: [startup → runtime → shutdown]
3. Error handling: [retry? backoff? circuit breaker?]
4. Security: [threats + defenses]

**Edge cases discovered (minimum 5):**
1. [Edge case] — how reference handles it
2. ...

**What I initially got wrong (minimum 1):**
- [Mental model correction]

**Implementation approach:**
[Which reference to follow, what to adapt, what to skip]
```

Then ask: "Based on this research, should I proceed?"

## Failure Modes — How This Skill Goes Wrong

| Failure | Symptom | Prevention |
|---------|---------|-----------|
| Surface-level research | Phase 3 items left blank, no source code read | Phase 4 box 2: "Read source code from at least 2 core files" |
| One-source bias | Only found one reference | Phase 2 minimum: 2 independent implementations |
| Skipping official docs | "I'll figure it out from examples" | Phase 2 priority 1: docs BEFORE repos |
| Premature action | Starting to code before Phase 4 all checked | HARD GATE: any box unchecked → go back |
| Ignoring security | No security row in Phase 5 template | Phase 3 item 7: security mandatory |
| User has to call it out | User says "you're still surface-level" | Self-check after Phase 5: re-verify Phase 4 checklist |

## Self-Improvement

This skill should improve itself. After completing research:

1. Note what went wrong — was research too shallow? wrong sources? missed edge cases?
2. Update this SKILL.md if a pattern can prevent the same mistake next time
3. Add examples to `references/research-examples.md` for new failure modes

## Tool Usage

- **context7 MCP**: Official docs for any library. Use FIRST.
- **WebSearch + WebFetch**: Find and read reference source files
- **agentskills.io spec**: [Client implementation guide](https://github.com/agentskills/agentskills/blob/main/docs/client-implementation/adding-skills-support.mdx) for skill system design
- **Explore agent**: Fan-out search across reference repos
