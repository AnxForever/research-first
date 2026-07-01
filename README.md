# research-first

> Universal project improvement skill for AI coding agents.
> Before writing code, find how others already solved it.

## What It Does

When an AI agent is asked to "add X feature" or "fix Y problem", this skill forces it to:

1. **Understand the project first** (read docs, map architecture)
2. **Expand the surface question** into the full problem space (10 dimensions)
3. **Search with quality** (GitHub qualifiers, multi-angle coverage, quality signals)
4. **Extract complete patterns** from ≥2 independent production references
5. **Evaluate reuse potential** (REUSE / ADAPT / LEARN-FROM)
6. **Verify 10 readiness criteria** before writing any code
7. **Output structured findings** for user approval

No more "I found a Medium article, here's my implementation."

## Install

```bash
npx skills add AnxForever/research-first
```

Or manually:

```bash
git clone https://github.com/AnxForever/research-first.git ~/.agents/skills/research-first
```

## Structure

```
research-first/
├── SKILL.md                          # Core workflow (Tier 1+2)
└── references/                       # Deep guides (Tier 3, on-demand)
    ├── search-quality.md             # Query construction, quality signals
    ├── problem-expansion.md          # 10-dimension framework with examples
    ├── adapting-depth.md             # Time pressure, risk levels, failure modes
    └── contradictions.md             # When references disagree
```

## Requirements

- Any AI agent that supports the Agent Skills standard (Claude Code, Codex, Cursor, etc.)
- No dependencies, no API keys, no configuration needed

## License

MIT — see [LICENSE](LICENSE)
