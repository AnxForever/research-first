# Research Summary: [Problem Being Solved]

## Project Identity (Phase 0)
> What problem does this project solve? Who uses it? What are the hard constraints?

[Brief: this project is a ____ that solves ____ for ____. Key constraint: ____.]

## References Found (Phase 2)

### 1. [Project Name](URL)
- **Files read**: `[path/to/core.ts]`, `[path/to/handler.py]`
- **Key insight**: [One sentence — the most important thing you learned]
- **Decision**: REUSE | ADAPT | LEARN-FROM
- **Why**: [License: MIT | Stack: matches ours | Maintained: yes, last commit <1mo]

### 2. [Project Name](URL)
- **Files read**: `[path/to/main.go]`, `[path/to/service.rs]`
- **Key insight**: [One sentence]
- **Decision**: REUSE | ADAPT | LEARN-FROM
- **Why**: [reasoning]

## Complete Pattern (Phase 3)

### Data Model
[Structures, schemas, fields, relationships]

### Lifecycle
```
startup → [what happens] → runtime → [what happens] → shutdown → [cleanup]
Error path: [what fails] → [how it recovers]
```

### Error Handling
- **Strategy**: [retry with backoff? circuit breaker? graceful degradation?]
- **Specific cases**:
  - [Error type] → [how handled]

### Security
- **Threats identified**: [list]
- **Defenses**: [list]

## Edge Cases (≥5, Phase 3)

| # | Edge Case | How Reference Handles It |
|---|-----------|-------------------------|
| 1 | [e.g., empty input] | [mechanism] |
| 2 | [e.g., concurrent access] | [mechanism] |
| 3 | [e.g., network timeout] | [mechanism] |
| 4 | [e.g., large payload] | [mechanism] |
| 5 | [e.g., invalid credentials] | [mechanism] |

## What I Initially Got Wrong
- [The assumption I had before reading source code]
- **Correction**: [What I learned from the reference that changed my approach]

## Implementation Plan
1. [Step] — following `[reference]`
2. [Step] — adapted for our conventions
3. [Step] — from official docs

---

**Ready to proceed?** [Ask user before writing code]
