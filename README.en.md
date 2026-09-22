# research-first

[简体中文](README.md) · **English**

> Understand the outcome, investigate existing solutions, show the choices, then implement.

A universal intent-interpretation and research methodology for AI agents. It turns compressed ideas, symptoms, suggestions, and doubts into evidence-backed decisions, actively investigating relevant products, open-source implementations, reusable resources, and primary documentation before showing the user options and tradeoffs.

**Reuse is optional. Skipping the investigation and silently defaulting to building from scratch is not.**

## What it does

The skill guides the agent to:

1. **Recover intent** — separate purpose, hard constraints, candidate means, assumptions, and missing dimensions.
2. **Expand proportionally** — add only considerations supported by relevance, evidence, and task stakes.
3. **Find existing solutions** — investigate comparable products, open-source projects, libraries, better techniques, and primary guidance; for frontend work, include relevant component libraries, specialized components, and animation libraries when motion serves the experience.
4. **Make choices visible** — show credible candidates, reusable parts, limitations, costs, and a recommendation before implementation. Reuse, adapt, combine, or build with evidence while preserving explicitly required methods.
5. **Reassess on doubt** — when the user questions the work, seek contrary evidence rather than defending or agreeing reflexively.
6. **Act and verify** — turn findings into decisions, implementation constraints, tests, and completion evidence.

It explicitly triggers when users ask for research, sources, examples, intent understanding, idea expansion, or reconsideration of work already in progress.

## Why it exists

What a user says is usually not a specification. **"Add browser skills"** may mean agents must complete web workflows reliably. **"Make it like Vercel"** names qualities — restraint, hierarchy, density — not a layout to copy. **"Use Redis"** may signal a need for shared state, durability or coordination; find out which problem exists before introducing Redis.

The skill keeps the agent at *research first, decide second* on inputs like these, instead of carrying the user's nouns straight into the plan. It carries a symmetric constraint: the pretext of "understanding intent" does not license scope expansion. Every addition has to pass three tests — relevance, evidence, and proportionality.

For example, "add a filterable, sortable admin table" should lead the agent to understand the workflow, inspect installed components, investigate suitable table resources and documentation, and explain what can be reused, what remains custom, and the maintenance and styling tradeoffs. A request that does not mention libraries is not an instruction to hand-build the interaction.

When a material product, dependency, cost, or visual tradeoff has not been delegated, the agent recommends an option and lets the user choose. If the user already selected or delegated the choice, it explains the evidence and continues. An exact mechanical edit, such as renaming a button, does not need another survey.

For multi-feature or long-running work, it preserves feature-specific evidence and historical gaps. Existing code, passing tests, or a project bibliography cannot establish every child feature's design quality.

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
├── SKILL.md                              # Core workflow
├── agents/openai.yaml                    # Skill UI metadata
├── assets/                               # Reusable research templates
└── references/                           # Deep guides and regression cases
    ├── search-quality.md                 # Query construction, quality signals, anti-patterns
    ├── reuse-and-alternatives.md         # Existing solutions, frontend resources, and user choices
    ├── problem-expansion.md              # 10-dimension framework with concrete examples
    ├── feature-evidence-ledger.md        # Ledger structure and backfill rules
    ├── adapting-depth.md                 # Time pressure, risk levels, failure modes
    ├── contradictions.md                 # When references disagree
    ├── research-examples.md              # Research and selection examples
    ├── case-studies.md                   # Hypothetical scenarios and evidence mistakes
    └── intent-interpretation-evaluation.md # Rubric and regression cases
```

The core file stays lean; depth lives in `references/`, read on demand rather than loaded on every trigger.

## Requirements

- Any AI agent supporting the Agent Skills standard (Claude Code, Codex, Cursor, etc.)
- No dependencies, no API keys, no configuration needed

## License

MIT — see [LICENSE](LICENSE)
