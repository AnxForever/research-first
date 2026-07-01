# Search Quality — Complete Guide

## Query Construction

### GitHub Qualifiers

```
stars:>1000              — community validation
stars:100..500           — niche but validated
pushed:>2024-06-01       — actively maintained
pushed:<2023-01-01       — find legacy (for migration research)
language:python          — exact tech match
language:typescript      — exact tech match
license:mit              — permissive, easy to reuse
license:apache-2.0       — permissive with patent grant
in:readme "production"   — self-described production quality
in:name {keyword}        — keyword in repo name
in:description {keyword} — keyword in description
org:{org-name}           — scope to trusted org
user:{username}          — scope to known author
path:src/                — exclude test/vendor noise
-path:test/ -path:dist/  — aggressive noise exclusion
topic:{tag}              — GitHub topics
```

### Composite Templates

```
Basic:      {keyword} language:{lang} stars:>{min} pushed:>{date}
Production: {keyword} language:{lang} stars:>1000 pushed:>2024-01-01 license:mit
Niche:      {keyword} language:{lang} stars:10..500 topic:{domain}
Docs-first: site:github.com "{tech} {topic}" in:readme
```

### Query Variations

Always run at least 3:

1. By problem: `"{problem description}" language:{lang}`
2. By solution: `"{solution pattern} example" language:{lang} path:src/`
3. By domain: `topic:{domain} language:{lang} stars:>500`

### Plain WebSearch Queries

```
"{tech stack} {feature} production implementation github 2025"
"{tech stack} {problem} best practice pattern"
"{tech stack} {component} architecture reference"
site:github.com "{tech} {pattern}"
```

## Source Priority Hierarchy

| Priority | Source | How | When to Skip |
|----------|--------|-----|-------------|
| 1 | Official docs | context7 MCP FIRST, else WebSearch `{tech} docs {topic}` | Never skip |
| 2 | Specs & standards | RFCs, agentskills.io, OWASP, protocol docs | If no standard exists |
| 3 | Source code | Read .ts/.py/.go/.rs files in repos | Never skip for FULL |
| 4 | Tests | Test files in reference repos | Skip for LIGHT only |
| 5 | GitHub issues | Known bugs, discussions, PR reviews | Skip if time < 15min |
| 6 | Stack Overflow | Accepted answers, high votes, recent | Skip if official docs sufficient |
| 7 | Blog posts | Cross-reference with docs | Skip whenever possible |

## Quality Signals Matrix

| Signal | Green | Yellow | Red |
|--------|-------|--------|-----|
| Last commit | < 1 month | 1-6 months | > 1 year |
| Stars | > 500 | 50-500 | < 50 |
| License | MIT/Apache/BSD | GPL/LGPL | None |
| Test directory | `test/` exists | Tests in source | No tests |
| Contributing guide | CONTRIBUTING.md | README section | None |
| Releases/tags | Git tags | Main only | No versioning |
| Issue response | Active replies | Mixed | All open |
| CI/CD | Green badge | No badge | Red/failing |
| Dependencies | Up to date | Minor outdated | Major vulnerable |
| Docs quality | Comprehensive | Minimal | README only |

## 2-Minute Quick Check

1. Open repo → last commit date? license file?
2. Skim test directory → real tests or placeholder?
3. Read one core source file → well-structured? documented?
4. Check 3 recent closed issues → maintainer responsive? problems acknowledged?

Passes all 4 → deep read. Fails any → deprioritize unless it's the only reference.

## Multi-Angle Coverage

| Angle | Query Pattern | Finds |
|-------|--------------|-------|
| By problem | `"{problem}" language:{lang}` | Direct solutions |
| By technology | `"{lib}" example production` | Official/community examples |
| By pattern | `"{pattern}" implementation {lang}` | Architectural references |
| By author | `org:{known-org}` or known author | Authority implementations |
| By awesome-list | `awesome-{topic}` | Curated collections |
| By paper | `"{algorithm}" code github` | Academic implementations |

Coverage check:
- Repos from ≥2 different orgs/authors?
- Both small focused libs AND large framework examples?
- At least one clearly used in production (issues, users, testimonials)?

## Search Anti-Patterns

| Mistake | Why | Fix |
|---------|-----|-----|
| First result only | Confirmation bias | ≥2 independent sources |
| Keyword-only | Misses alternatives | Multi-angle coverage |
| No date filter | Dead projects | `pushed:>YYYY-MM-DD` |
| License ignored | Illegal reuse | Check before deep reading |
| GitHub-only | Misses docs/specs | Start with docs |
| Vague queries | Noise | Language + domain + qualifiers |
| No test reading | Wrong API usage | Read tests |
| Stars-only sorting | Popular ≠ good pattern | Cross-reference quality signals |
