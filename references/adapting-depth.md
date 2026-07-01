# Adapting Research Depth

## Time-Pressure Modes

Not every task can afford 2 hours of research. Match depth to time:

### Quick Scan (< 5 min)
- Skip Phase 0 (assume you know the project)
- Skip Phase 1 (use surface question directly)
- Phase 2: one search, first good result, quick quality check
- Skip Phase 3-4
- Phase 5: only checkboxes 2, 3, 8
- Phase 6: one-paragraph summary

### Standard (15-30 min) — DEFAULT
- Full Phase 0, 1, 2
- Phase 3: 6/10 dimensions
- Phase 4: basic reuse evaluation
- Phase 5: all checkboxes
- Phase 6: full template

### Deep Dive (1-2 hours)
- Full all phases
- Phase 3: 10/10 dimensions
- Phase 4: detailed license + maintenance evaluation
- Additional: read related projects, check issue trackers in depth

## Project Risk Levels

Research depth should scale with project risk:

| Risk | Examples | Min Dimensions | Min References |
|------|----------|---------------|----------------|
| Low | Internal tool, prototype, hackathon | 3 | 1 |
| Medium | Customer-facing feature, API change | 6 | 2 |
| High | Auth, payments, data privacy, core infra | 10 | 3+ |

## When You Know Nothing About the Domain

If you're completely unfamiliar with the problem space:

1. Add an **exploratory phase** before Phase 1:
   - Search `"{domain} fundamentals architecture overview"`
   - Search `"{domain} best practices 2025"`
   - Read the Wikipedia article or introductory docs
   - Find one "awesome list" and skim the categories
2. Then proceed to Phase 1 with basic domain understanding
3. Add 50% to time estimates

## When Search Finds Nothing Useful

After 3 varied queries with no production-quality results:

**Do not silently proceed with best-guess code.** Instead, report:

```
⚠ No production references found for [topic] after searching:
  - [query 1] → [why results weren't useful]
  - [query 2] → [why results weren't useful]
  - [query 3] → [why results weren't useful]

Options:
1. Broaden search (remove language filter, lower star threshold, try different keywords)
2. Best-effort from first principles (acknowledge: this is novel/underserved territory)
3. Reconsider approach (is there a simpler alternative that has abundant references?)
```

## When References Contradict Each Other

See [contradictions.md](contradictions.md)

## Failure Mode Catalog

| Failure | Why | Fix |
|---------|-----|-----|
| Skipping Phase 0 | Solution alien to project | Phase 5 box 1 |
| Surface-only search | Found how but not why | Phase 3 self-check |
| One-source bias | Single reference may be wrong | ≥2 repos |
| Tutorials not source | No error handling | Read source files |
| License ignored | Can't legally use code | Phase 4 check |
| Missing security | Vulnerable code | Phase 3 item 7 |
| Over/under-engineered | Wrong abstraction level | Phase 0 project scale |
| Ignoring search failure | Proceed with guesswork | Report-to-user protocol |
| Domain ignorance | Can't expand problem space | Exploratory phase |
| Time panic | Drops quality instead of scope | Downgrade depth tier |
