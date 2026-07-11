# research-first

> Understand what the user is really trying to achieve, then research before choosing how.

A universal intent-interpretation and research methodology for AI agents. It turns compressed ideas, symptoms, suggestions, and doubts into evidence-backed decisions without blindly copying the user or inventing unrelated scope.

## What It Does

The skill guides the agent to:

1. **Recover intent** — separate purpose, hard constraints, candidate means, assumptions, and missing dimensions.
2. **Expand proportionally** — add only considerations supported by relevance, evidence, and task stakes.
3. **Research with quality** — use local evidence, primary sources, prior art, user data, and safe experiments.
4. **Judge proposed means** — adopt, adapt, combine, or decline instead of treating suggestions as specifications.
5. **Reassess on doubt** — when the user questions the work, seek contrary evidence rather than defending or agreeing reflexively.
6. **Act and verify** — turn findings into decisions, implementation constraints, tests, and completion evidence.

It explicitly triggers when users ask for research, sources, examples, intent understanding, idea expansion, or reconsideration of work already in progress.

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
├── SKILL.md                          # Core workflow
├── agents/openai.yaml                # Skill UI metadata
├── assets/                           # Reusable research templates
└── references/                       # Deep guides and regression cases
    ├── search-quality.md             # Query construction, quality signals, anti-patterns
    ├── problem-expansion.md          # 10-dimension framework with concrete examples
    ├── adapting-depth.md             # Time pressure, risk levels, failure modes
    ├── contradictions.md             # When references disagree
    └── intent-interpretation-evaluation.md # Rubric and regression cases
```

## Requirements

- Any AI agent supporting the Agent Skills standard (Claude Code, Codex, Cursor, etc.)
- No dependencies, no API keys, no configuration needed

## License

MIT — see [LICENSE](LICENSE)
