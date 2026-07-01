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

## Phase 1.5: Problem Space Expansion (MANDATORY for FULL research)

**The user's surface question is never the whole problem.** A feature like "add X" actually
means "add X, correctly, securely, efficiently, maintainably, in a way that fits the project,
handles edge cases, and won't need rewriting next month."

Before searching, expand the surface question into the complete problem tree. For ANY feature X,
systematically ask these 10 probe questions and generate search queries for EACH one:

| # | Probe Question | Search Query Template |
|---|---------------|----------------------|
| 1 | **Data** — What data does X need? Schema, storage, validation, migration? | `"{X} data model schema design"` |
| 2 | **Lifecycle** — How does X start, run, stop, restart, recover from crash? | `"{X} lifecycle startup shutdown error recovery"` |
| 3 | **Integration** — How does X connect to existing systems? Failure modes when dependencies are down? | `"{X} integration pattern {tech stack}"` |
| 4 | **Security** — What attacks is X vulnerable to? AuthZ? Injection? Data leaks? | `"{X} security best practices OWASP"` |
| 5 | **Performance** — Bottlenecks? Scaling limits? Resource usage? | `"{X} performance optimization bottleneck"` |
| 6 | **Observability** — How to monitor, log, debug, audit X? | `"{X} monitoring logging observability"` |
| 7 | **API/UX** — How do users/code interact with X? What's the contract? | `"{X} API design interface contract"` |
| 8 | **Configuration** — What's configurable? Environment differences? Feature flags? | `"{X} configuration options environment"` |
| 9 | **Testing** — How to test X? What edge cases? Integration tests? | `"{X} testing strategy edge cases"` |
| 10 | **Evolution** — How will X change over time? Versioning? Backward compatibility? Deprecation? | `"{X} versioning backward compatibility migration"` |

**Example: User says "add skill system to AgentOS"**

Surface question: "How to load a SKILL.md file?"

Problem space expansion:
```
1. Data       → skill schema, metadata format, agentskills.io spec
2. Lifecycle  → discovery → load → execute → unload → compaction survival → reload
3. Integration → skill + tool interaction, skill permissions, MCP skill bridge
4. Security   → prompt injection via SKILL.md, malicious marketplace skills
5. Performance → context budget per skill, 250-char description cap, 1% listing budget
6. Observability → skill usage tracking, dedup logging, loaded skills state
7. API/UX     → use_skill tool, slash commands, auto-match by description
8. Configuration → managed/user/project priority, paths-based conditional skills
9. Testing    → skill parsing tests, dedup tests, injection tests
10. Evolution  → skill versioning, deprecation, migration between versions
```

**Each dimension generates 1-3 search queries. That's 10-30 queries instead of 1-2.**
This is the difference between finding "how to load a file" and finding the COMPLETE
architecture that Claude Code, OpenCode, and Google ADK all independently converged on.

**HARD RULE: For FULL research, expand to at least 6 of the 10 dimensions before
moving to Phase 2. If you only search the surface question, you WILL miss critical
problems that the user will have to find later.**

## Phase 2: Multi-Source Search — WITH QUALITY

### 2A. Query Construction

Bad queries find bad references. Good queries use specific qualifiers.

**GitHub search qualifiers:**
```
stars:>1000                    — community validation
pushed:>2024-01-01             — actively maintained (not dead)
language:python                — exact tech match
license:mit                    — legally reusable
in:readme "production"         — self-described production quality
org:organization-name          — scope to trusted orgs
path:src/                      — exclude test/vendor noise
topic:web-framework            — GitHub topics
```

**Composite query template:**
```
{keyword} language:{lang} stars:>{min_stars} pushed:>{recent_date} license:{compatible_license}
```

**Query variations (always run at least 3):**
1. By problem: `"{problem description}" language:{lang}`
2. By solution: `"{solution pattern} example" language:{lang} path:src/`
3. By domain: `topic:{domain} language:{lang} stars:>500`

**Plain WebSearch queries:**
```
"{tech stack} {feature} production implementation github 2025"
"{tech stack} {problem} best practice pattern"
"{tech stack} {component} architecture reference"
site:github.com "{tech} {pattern}"
```

### 2B. Source Prioritization

Not all sources are equal. Follow this priority order:

| Priority | Source | How to access |
|----------|--------|---------------|
| 1 | **Official docs** | context7 MCP (FIRST), or `{tech} official docs {topic}` |
| 2 | **Specs & standards** | RFCs, agentskills.io, OWASP, framework protocol docs |
| 3 | **Reference source code** | Read actual .ts/.py/.go/.rs files in repos |
| 4 | **Reference tests** | Test files reveal edge cases and actual usage |
| 5 | **GitHub issues** | Known bugs, design discussions, PR reviews |
| 6 | **Stack Overflow** | Only accepted answers with high votes, verify recency |
| 7 | **Blog posts** | LAST resort — cross-reference with official docs |

**HARD RULES:**
- NEVER cite a blog post as primary evidence. Always trace back to source code.
- For any repo found: read at least 2 source files + 1 test file. Not just README.
- If a standard/spec exists, read it BEFORE looking at implementations.

### 2C. Quality Signals — Evaluate BEFORE Deep-Diving

Before spending time reading a repo, score it on these signals:

| Signal | Good | Warning | Dealbreaker |
|--------|------|---------|-------------|
| Last commit | < 1 month | 1-6 months | > 1 year |
| Stars | > 500 | 50-500 | < 50 (unless niche) |
| License | MIT/Apache/BSD | GPL | None |
| Test directory | `test/` or `__tests__/` exists | Tests in same files | No tests |
| Contributing guide | CONTRIBUTING.md exists | Brief section in README | None |
| Release/tags | Git tags or releases | Only main branch | No versioning |
| Issue response | Issues get replies | Some open, some closed | All open, no replies |

**Quick quality check (2 minutes before committing to deep read):**
1. Open the repo → check last commit date and license
2. Skim the test directory → are there actual tests?
3. Read one core source file → is it well-structured and documented?
4. Check 3 recent closed issues → how does the maintainer respond?

**Passes all 4 checks → worth deep reading. Fails any → deprioritize.**

### 2D. Multi-Angle Coverage Verification

After initial search, verify you haven't missed important sources by searching from different angles:

| Angle | Query pattern | What it finds |
|-------|--------------|---------------|
| **By problem** | `"{problem}" language:{lang}` | Direct solutions |
| **By technology** | `"{library/framework}" example` | Official/community examples |
| **By pattern** | `"{design pattern}" implementation {lang}` | Architectural references |
| **By author** | `org:{known-org}` or author's repos | Authority implementations |
| **By dependency** | repos that depend on the target library | Integration patterns |
| **By awesome-list** | `awesome-{topic}` repos | Curated collections |

**Coverage check**: After searching, ask yourself:
- "Did I find repos from different organizations/authors?" (not all from same person)
- "Did I find both small focused libs AND large framework examples?"
- "Did I find at least one repo that's clearly used in production?"

### 2E. Search Anti-Patterns

| Anti-Pattern | Why it fails | Fix |
|-------------|-------------|-----|
| Stopping after first result | Confirmation bias | Minimum 2 independent sources |
| Searching only by keyword | Misses alternative approaches | Use multi-angle search (2D) |
| Not filtering by date | Finds dead/outdated projects | Always add `pushed:>YYYY-MM-DD` |
| Ignoring license | Can't legally reuse code | Check license BEFORE deep reading |
| Using only GitHub search | Misses official docs, specs, papers | Start with docs, end with repos |
| Vague queries | Returns noise, not signal | Include language + domain + quality qualifiers |
| Copying code without reading tests | Misses edge cases and correct usage | Read tests before copying API calls |

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
