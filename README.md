# research-first

> Before you create anything, find how others already did it better.

A universal research methodology skill for AI agents. Works for any task — writing code, designing UI, drafting documents, planning projects, making decisions.

## What It Does

When asked to create, build, write, design, plan, or decide something, this skill guides the agent through a 7-phase research process:

0. **Understand project identity** — WHO is this for? WHY does it exist?
1. **Expand the problem** — surface question → 10-dimension problem space
2. **Search with quality** — backend: source code, specs / creative: best examples, templates, style guides
3. **Extract complete patterns** — from ≥2 independent references
4. **Evaluate reuse** — REUSE / ADAPT / LEARN-FROM
5. **Verify readiness** — 11 checkboxes before producing output
6. **Report findings** — structured summary for user approval
7. **Self-audit** — catch problems before the user does

No more "I found a tutorial, here's my implementation."

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
├── SKILL.md                          # Core workflow (Tier 1+2, ~340 lines)
└── references/                       # Deep guides (Tier 3, on-demand)
    ├── search-quality.md             # Query construction, quality signals, anti-patterns
    ├── problem-expansion.md          # 10-dimension framework with concrete examples
    ├── adapting-depth.md             # Time pressure, risk levels, failure modes
    └── contradictions.md             # When references disagree — resolution framework
```

## Requirements

- Any AI agent supporting the Agent Skills standard (Claude Code, Codex, Cursor, etc.)
- No dependencies, no API keys, no configuration needed

## License

MIT — see [LICENSE](LICENSE)
