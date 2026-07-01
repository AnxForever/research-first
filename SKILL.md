---
name: research-first
description: >-
  Universal project improvement skill. Before modifying any project, understand its
  architecture and problems (Phase 0), expand the surface question into the complete
  problem space across 10 dimensions (Phase 1), search for existing solutions using
  quality-weighted queries across 7 source types (Phase 2), extract complete patterns
  from at least 2 independent references by reading source code and tests (Phase 3),
  evaluate whether to reuse, adapt, or learn from each reference (Phase 4), verify 10
  readiness criteria before writing any code (Phase 5), and output structured findings
  (Phase 6). Use when the user asks to add features, fix problems, optimize, refactor,
  design architecture, or improve any project. Triggers on feature requests, bug reports,
  architecture questions, tech selection, performance issues, and any non-trivial code
  change. Skip only for one-line fixes, typos, and config value changes.
---

# Research-First Engineering

**Don't write code until you've found how others already solved it.**

This skill works on any project. It forces you to understand the project first,
search the world for proven solutions, and only then implement — following
patterns that production systems have already validated.

---

## Phase 0: Understand the Project

Before searching for solutions, read the project:

1. **Identity files** — CLAUDE.md, README.md, ARCHITECTURE.md, CONTRIBUTING.md
2. **Docs directory** — design documents, API specs, ADRs
3. **Core source** — main modules, entry points, critical paths
4. **Tech stack** — language, framework, database, key dependencies
5. **Conventions** — code style, naming, error handling, test patterns
6. **Known problems** — TODOs, FIXMEs, issue trackers, recent commits

Output a project map:
```
Project: [name]
Stack: [language / framework / database / key deps]
Architecture: [monolith | microservices | ..., key modules]
Conventions: [code style, error handling, testing]
Problems: [what user asked + what you discovered]
```

## Decision Tree

```
Task type:
├─ One-line fix, typo, config value → SKIP research
├─ Familiar pattern in this stack → LIGHT (Phase 2 only)
└─ New feature, design, optimization, unknown domain → FULL (all phases)
```

When in doubt, do full research.

---

## Phase 1: Expand the Problem Space

The user's surface question is never the whole problem.
"Add X" means "add X correctly, securely, efficiently, maintainably."

For any feature X, expand to these 10 dimensions and generate search queries for EACH:

| # | Dimension | Probe Question | Query Template |
|---|-----------|---------------|----------------|
| 1 | Data | Schema, storage, validation, migration? | `"{X} data model schema design"` |
| 2 | Lifecycle | Startup, runtime, shutdown, crash recovery? | `"{X} lifecycle error recovery"` |
| 3 | Integration | How connects to existing systems? Failure modes? | `"{X} integration pattern {stack}"` |
| 4 | Security | Attack vectors? AuthZ? Injection? Data leaks? | `"{X} security best practices OWASP"` |
| 5 | Performance | Bottlenecks? Scaling limits? Resource usage? | `"{X} performance optimization"` |
| 6 | Observability | Monitoring, logging, debugging, auditing? | `"{X} monitoring observability"` |
| 7 | API/UX | Contract? User interaction? Error messages? | `"{X} API design interface"` |
| 8 | Configuration | Configurable vs hardcoded? Env differences? | `"{X} configuration environment"` |
| 9 | Testing | Strategy? Edge cases? Integration tests? | `"{X} testing edge cases"` |
| 10 | Evolution | Versioning? Backward compat? Migration path? | `"{X} versioning migration"` |

**Example: "add skill system to AgentOS"**
```
Surface: "How to load SKILL.md?"
Expanded:
  1. Data       → skill schema, agentskills.io spec, metadata format
  2. Lifecycle  → discover → load → execute → unload → compaction survival
  3. Integration → skill + tool interaction, permissions, MCP bridge
  4. Security   → prompt injection via SKILL.md, marketplace risks
  5. Performance → context budget, description cap, listing budget
  6. Observability → usage tracking, dedup logging
  7. API/UX     → use_skill tool, slash commands, auto-match
  8. Configuration → managed/user/project priority, paths-based conditions
  9. Testing    → parsing, dedup, injection, dependency resolution
  10. Evolution  → versioning, deprecation, migration
```

**Hard rule: expand at least 6 of 10 dimensions before Phase 2.**
This turns 1-2 surface queries into 10-30 targeted searches.

---

## Phase 2: Search with Quality

### 2A. Query Construction

**GitHub qualifiers:**
```
stars:>1000              — community validation
pushed:>2024-01-01       — actively maintained
language:python          — exact tech match
license:mit              — legally reusable
in:readme "production"   — self-described production quality
org:organization-name    — scope to trusted orgs
path:src/                — exclude test/vendor noise
```

**Composite template:**
```
{keyword} language:{lang} stars:>{min} pushed:>{date} license:{compatible}
```

**Always run at least 3 query variations:**
1. By problem: `"{problem}" language:{lang}`
2. By solution: `"{pattern} example" language:{lang} path:src/`
3. By domain: `topic:{domain} language:{lang} stars:>500`

### 2B. Source Priority

| Priority | Source | Method |
|----------|--------|--------|
| 1 | Official docs | context7 MCP FIRST, or `{tech} official docs {topic}` |
| 2 | Specs & standards | RFCs, agentskills.io, OWASP, framework protocol docs |
| 3 | Source code | Read actual .ts/.py/.go/.rs files — NOT just README |
| 4 | Tests | Test files reveal edge cases and correct usage |
| 5 | GitHub issues | Known bugs, design discussions, PR reviews |
| 6 | Stack Overflow | Accepted answers with high votes only, verify recency |
| 7 | Blog posts | Last resort — always cross-reference with official docs |

**Hard rules:**
- Never cite a blog post as primary evidence.
- If a standard/spec exists, read it before implementations.
- For every repo: read ≥ 2 source files + ≥ 1 test file.

### 2C. Quality Signals

Score each repo BEFORE deep-diving:

| Signal | Good | Warning | Dealbreaker |
|--------|------|---------|-------------|
| Last commit | < 1 month | 1–6 months | > 1 year |
| Stars | > 500 | 50–500 | < 50 |
| License | MIT / Apache / BSD | GPL | None |
| Tests | `test/` directory exists | Tests in same files | No tests |
| Contributing | CONTRIBUTING.md | Brief README section | None |
| Releases | Git tags present | Main branch only | No versioning |
| Issue response | Issues get replies | Mixed | All open, no replies |

**2-minute quick check:**
1. Open repo → check last commit + license
2. Skim test directory → real tests?
3. Read one core source file → well-structured?
4. Check 3 recent closed issues → maintainer responsive?

Passes all 4 → worth deep reading. Fails any → deprioritize.

### 2D. Multi-Angle Coverage

Search from 6 angles to avoid blind spots:

| Angle | Query | Finds |
|-------|-------|-------|
| By problem | `"{problem}" language:{lang}` | Direct solutions |
| By technology | `"{lib}" example` | Official/community examples |
| By pattern | `"{pattern}" implementation {lang}` | Architectural references |
| By author | `org:{known-org}` | Authority implementations |
| By dependency | Reverse dependency search | Integration patterns |
| By awesome-list | `awesome-{topic}` | Curated collections |

**Coverage check:** Found repos from different orgs? Both small libs and large frameworks? At least one clearly production-used?

### 2E. Search Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Stopping at first result | Minimum 2 independent sources |
| Keyword-only search | Multi-angle search (2D) |
| No date filter | Always add `pushed:>YYYY-MM-DD` |
| Ignoring license | Check before deep reading |
| GitHub-only search | Start with docs, end with repos |
| Vague queries | Language + domain + qualifiers |
| Copying without reading tests | Read tests before API calls |

---

## Phase 3: Extract Complete Patterns

For each reference, extract ALL 10 dimensions. Missing any = not deep enough.

1. **Data model** — structures, schemas, fields, relationships
2. **Lifecycle** — startup → runtime → shutdown for every component
3. **Error handling** — retry? backoff? circuit breaker? graceful degradation?
4. **Edge cases** — null, empty, race, timeout, large input, concurrent access
5. **Configuration** — configurable vs hardcoded? env-specific behavior?
6. **Tests** — patterns? edge cases covered? what's NOT tested?
7. **Security** — threats? input validation? authN/Z? sanitization? injection?
8. **Integration** — connections to other systems? failure modes?
9. **Performance** — bottlenecks? caching? lazy loading? batching?
10. **Surprise** — the one finding that contradicted your initial assumption

**Self-check before Phase 4:**
> "Can I draw the complete architecture, trace every error path, and name
> 5 edge cases the reference handles that I would have missed alone?"

If no → go back to Phase 2.

---

## Phase 4: Evaluate Reuse Potential

For each reference, decide: REUSE, ADAPT, or LEARN-FROM.

| Criteria | Reuse | Adapt | Learn-from |
|----------|-------|-------|------------|
| License compatible? | ✓ | ✓ | Any |
| Same language/framework? | ✓ | Similar | Any |
| Same scale/requirements? | ✓ | Close | Different |
| Actively maintained? | ✓ | If stable | Any |
| Code quality matches? | ✓ | With cleanup | Patterns only |

Prefer REUSE over ADAPT over LEARN-FROM. Document why.

---

## Phase 5: Verify Readiness

**All 10 boxes must be checked before writing ANY code.**

- [ ] Read the project's docs and key source files (Phase 0)
- [ ] Expanded at least 6/10 problem dimensions (Phase 1)
- [ ] Found ≥ 2 independent production references (Phase 2)
- [ ] Read ≥ 2 source files + 1 test file from each reference (Phase 2)
- [ ] Read official documentation for the core API (Phase 2B)
- [ ] Extracted all 10 pattern dimensions (Phase 3)
- [ ] Identified ≥ 5 edge cases from references (Phase 3)
- [ ] Found ≥ 1 security consideration (Phase 3)
- [ ] Made reuse/adapt/learn-from decision for each reference (Phase 4)
- [ ] Solution fits the project's existing conventions (Phase 0)

**Hard gate: any box unchecked → go back. Do not proceed to Phase 6.**

---

## Phase 6: Report Findings

Use this exact template:

```
## Research Summary: [Problem]

### Project Context
[Phase 0 findings: architecture, conventions, constraints]

### References
1. **[Name](URL)**
   - Files read: [2+ paths actually opened]
   - Key insight: [one sentence]
   - Decision: REUSE | ADAPT | LEARN-FROM — [why]

2. **[Name](URL)**
   - Files read: [2+ paths actually opened]
   - Key insight: [one sentence]
   - Decision: REUSE | ADAPT | LEARN-FROM — [why]

### Complete Pattern
- Data model:
- Lifecycle: startup → runtime → shutdown
- Error handling:
- Security:

### Edge Cases (≥ 5)
1. [Case] → handled by [mechanism]
2. ...

### What I Got Wrong
- [Assumption correction from reading source code]

### Implementation Plan
1. [Step] — following [reference]
2. [Step] — adapted for project conventions
```

Then ask: **"Based on this research, proceed with implementation?"**

---

## Failure Modes

| Failure | Symptom | Hard Gate |
|---------|---------|-----------|
| Skipping Phase 0 | Solution alien to project style | Phase 5 box 1 |
| Surface-only search | Can't fill Phase 3 dimensions | Phase 3 self-check |
| One-source bias | Single reference | Phase 2: ≥ 2 repos |
| Tutorials over source | No error handling in plan | Phase 2B: read source code |
| Ignoring license | Illegal to reuse | Phase 4 license check |
| Missing security | Vulnerable code | Phase 3 item 7 |
| Wrong abstraction | Over/under-engineered | Phase 0: project scale |
| User calls out shallowness | "Still doing surface research" | Re-verify all Phase 5 boxes |

## Self-Improvement

After each use, note failures and update this skill:
1. What went wrong? (too shallow? wrong sources? missed context?)
2. Can a rule change prevent it next time?
3. Add concrete examples to `references/examples.md`

## Tool Reference

| Phase | Tools |
|-------|-------|
| 0 — Understand | Read, Glob, Grep — project files |
| 1 — Expand | Brainstorm all 10 dimensions |
| 2 — Search | context7 MCP (docs), WebSearch (repos), WebFetch (source files) |
| 3 — Extract | Read source files, compare implementations |
| 4 — Evaluate | License check, quality signals (2C) |
| 5 — Verify | Phase 5 checklist |
| 6 — Report | Write to conversation + CLAUDE.md / docs/RESEARCH.md |
