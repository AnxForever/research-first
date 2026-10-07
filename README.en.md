# research-first

[简体中文](README.md) · **English**

Help AI agents understand your purpose, investigate relevant products, open-source solutions, and technical guidance, then show you evidence-backed choices before implementing a feature.

**Reuse is optional. Investigation is required. Building from scratch should be an informed decision.**

A user often brings an idea without a list of useful component libraries, animation libraries, mature products, or implementation techniques. `research-first` makes discovering those options the agent's responsibility and requires the research to inform selection, implementation, and verification.

[Quick start](#quick-start) · [Behavior example](#behavior-example) · [What to expect](#what-to-expect) · [Boundaries](#boundaries) · [Optional Jev checks](#optional-jev-checks) · [File guide](#file-guide)

## Behavior example

You ask: **“Add a filterable, sortable table to the admin panel.”**

| Stage | Behavior to correct | Expected with research-first |
|---|---|---|
| Understand | Treat one sentence as a complete specification | Use project context to establish the workflow, data scale, important states, and constraints |
| Investigate | Hand-build the table and interactions from memory | Inspect installed components; investigate comparable products, reusable table solutions, and primary guidance |
| Choose | Explain the approach after writing the code | Show candidates, sources, tradeoffs, a recommendation, and remaining custom work before implementation |
| Verify | Call it done when the page renders | Turn findings into relevant acceptance conditions for filtering, sorting, empty states, keyboard use, and other material behavior |

Frontend research includes suitable component libraries, specialized components, and animation libraries when motion serves the requested experience. Evaluate the existing stack, styling control, interaction states, accessibility, maintenance, and integration cost. The outcome can be reuse, adaptation, composition, or a justified custom implementation.

The same principle applies to backend work, architecture, integrations, documents, and decisions: find products, implementations, and guidance that address the actual problem, uncover important missing questions, and preserve explicit technology and scope constraints.

## Quick start

Install with the Skills CLI:

As checked on 2026-10-02, [`skills@1.7.0`](https://registry.npmjs.org/skills/1.7.0)
requires **Node.js >=22.20.0**; discovery was verified on Node 22.21.1. The command
below does not pin the CLI. Use `npx skills@1.7.0 add AnxForever/research-first`
to reproduce the tested CLI version; later versions may change their requirements.
Manual cloning does not require Node.js.

```bash
npx skills add AnxForever/research-first
```

For manual installation, use the directory and invocation syntax of the actual host:

| Host | Personal installation | Project installation | Explicit invocation |
|---|---|---|---|
| Claude Code | `~/.claude/skills/research-first` | `.claude/skills/research-first` | `/research-first your request` |
| Codex | `~/.agents/skills/research-first` | `.agents/skills/research-first` | `$research-first your request` |

Claude Code example for WSL, Linux or macOS, with a destination that does not yet exist:

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/AnxForever/research-first.git "$HOME/.claude/skills/research-first"
```

Native Windows Claude Code (PowerShell, destination must not already exist):

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/skills" | Out-Null
git clone https://github.com/AnxForever/research-first.git "$HOME/.claude/skills/research-first"
```

In Claude Code, enter `/research-first add a filterable, sortable table to this project`.
Ordinary requests can also match the description automatically. A personal skill takes
precedence over a project skill with the same name, so check the actual loaded path
before testing a new copy. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

The following manual examples use **Codex**'s `~/.agents/skills/research-first`.
For native Windows Claude Code, replace `.agents/skills` with `.claude/skills`.
A CLI running inside WSL uses its WSL installation directories. `npx skills add`
works in common shells with Node.js/npm installed. Manual clone destinations must
not already exist:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/AnxForever/research-first.git "$HOME/.agents/skills/research-first"
```

Windows PowerShell:

```powershell
$skillRoot = Join-Path $HOME ".agents/skills"
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/AnxForever/research-first.git (Join-Path $skillRoot "research-first")
```

Windows Command Prompt (`cmd`):

```bat
if not exist "%USERPROFILE%\.agents\skills" mkdir "%USERPROFILE%\.agents\skills"
git clone https://github.com/AnxForever/research-first.git "%USERPROFILE%\.agents\skills\research-first"
```

For other environments, clone the repository into the directory where that agent discovers skills. Keep the entire folder so `SKILL.md` can resolve its references. If the destination already exists, update the existing clone there instead of cloning again to the same path.

The following examples use Codex syntax. In Claude Code, replace the initial
`Use $research-first` with `/research-first`:

```text
Use $research-first to add a filterable, sortable table to this project.
Understand the workflow, investigate comparable products, reusable components,
and official guidance. Before implementing, show me the options, your
recommendation, and what still needs custom code.
```

An implementation request already includes routine, reversible choices within the
existing stack and scope. To emphasize autonomous execution, you can say:

```text
Use $research-first to complete this feature. You can choose the implementation
within the existing stack. Briefly show the comparison and evidence,
then continue with implementation and verification.
```

You can also request research only:

```text
Use $research-first to investigate how products implement this feature,
reusable open-source solutions, and technical guidance.
Show candidates, tradeoffs, and a recommendation. Do not change code this time.
```

Environments with automatic skill matching may also select it from the request; explicit invocation makes your intent clear. The core skill consists of Markdown instructions and has no runtime dependencies. Browsing, reading code, and running verification depend on the tools available to the agent. The optional Jev adapter is installed separately and does not affect ordinary use.

## What to expect

```text
Understand → Inspect context → Investigate solutions and guidance → Show choices → Implement → Verify
```

Before substantial implementation, the agent should provide a concise update proportional to the task:

- **Purpose and constraints:** whose problem it addresses, what the project already has, and which assumptions remain open.
- **Evidence and findings:** products, source, documentation, or experiments examined; which findings changed or supported the approach.
- **Candidates and tradeoffs:** what can be reused, what adoption involves, and what remains custom.
- **Recommendation and verification:** why the approach fits this project and how important failure cases will be checked.

A table decision could use the following structure. This is an illustration of comparison questions; actual candidates need sources and verified findings:

| Approach | Investigate | Explain to the user |
|---|---|---|
| Extend the project's existing component | Whether it covers the required interactions and where it falls short | Which capabilities can be retained and which need work |
| Use a specialized table library with existing styles | APIs, version compatibility, interaction support, and license | What implementation work it saves and what dependencies and integration effort it adds |
| Build locally | The specific mismatch in investigated alternatives | Why custom work is justified, which evidence informs it, and who maintains it |

A reuse recommendation must explain the remaining business logic and integration work. A custom recommendation must explain why credible candidates do not fit. Table logic and animation are separate decisions; they should not be bundled into a choice between adopting an entire library stack and hand-building everything.

After implementation, report what was delivered, what verification showed, and what remains unverified. A concise evidence → decision → verification record is sufficient only when one reversible feature is completed in a single session without Deep research; the pre-implementation update can capture the evidence and decision, with verification added to the completion report. Use a [per-feature evidence ledger](references/feature-evidence-ledger.md) for multi-feature, cross-session, or high-risk work, so a project-wide research report cannot stand in for evidence about every feature.

## Boundaries

- **Research substantial work.** New features, pages, interactions, integrations, and important implementation choices qualify. Clear, low-risk changes that only alter copy and introduce no behavior can proceed directly; a small code change that introduces behavior is still a substantial feature.
- **Match evidence to the claim.** Support important claims with primary evidence. Add independent corroboration for high-risk claims or evidence disputes that could materially affect the outcome.
- **Implementation includes routine choices.** Explain and proceed with reversible choices within the existing stack and scope. Ask about an unauthorized change to the product outcome, explicit constraints, paid/external commitments, or substantial migration or maintenance obligations. Respect explicit requests to present options or wait first.
- **Respect constraints and match the task's scale.** Honor required technologies and restrictions such as no new dependencies. Small edits do not need an industry survey, and frontend work does not automatically need an animation library.
- **Reuse valid evidence and revisit affected conclusions.** Do not repeat current research. When the user questions the work, seek evidence that could overturn the approach instead of only defending it.
- **Disclose research gaps.** If browsing is unavailable, sources are insufficient, or a candidate remains unverified, distinguish facts, inferences, and assumptions. A failed search does not prove that no existing solution exists.

These are working instructions for an agent. Assess compliance through the sources it actually examines, the options it shows, and its delivery evidence. Repository examples do not replace validation in the current project.

## Optional Jev checks

Jev can provide a bounded second opinion at consequential checkpoints, without
adding a model call to every step:

| When | Question |
|---|---|
| After interpreting the request | Does the interpretation preserve the explicit requirement? |
| After inspecting a source | Does this actual excerpt support this one claim? |
| Before showing the comparison | Does the update disclose the supplied viable options and material costs? |
| After execution checks | Does the completion claim match the executed verification? |

On 2026-09-22, the documented stable version was `jev-1.13.0`; a live API probe
also resolved `jev-latest` to that version. The optional adapter uses the official
Python SDK and previews requests by default. Only `--live` sends the explicit short
evidence card; it does not collect project files or conversation history.

Its answers are advisory: they cannot establish source authenticity, replace
tests, determine user preferences, or authorize implementation. A real-project
trial produced a low-confidence disagreement with a pre-recorded evaluator label,
so there is no automatic approval threshold.

See [the Jev guide](references/jev-checkpoints.md) for setup and boundaries, and
[the evaluation record](evals/README.en.md) for the real-project experiment, pre-labeled
cases, and raw results. The core workflow remains usable without Jev.

## File guide

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Skill entry point: intent, research, selection, execution, and verification |
| [Reuse and alternatives](references/reuse-and-alternatives.md) | Existing solutions, frontend resources, and choices before implementation |
| [Search quality](references/search-quality.md) · [Research depth](references/adapting-depth.md) | Select evidence, scale investigation, and decide when to stop searching |
| [Problem expansion](references/problem-expansion.md) · [Contradictions](references/contradictions.md) | Uncover material questions and resolve conflicting evidence |
| [Feature evidence ledger](references/feature-evidence-ledger.md) | Track each feature's evidence, decisions, and historical gaps |
| [Research examples](references/research-examples.md) · [Case studies](references/case-studies.md) · [Evaluation scenarios](references/intent-interpretation-evaluation.md) | Understand the workflow and examine common reasoning failures |
| [Research report template](assets/research-report-template.md) · [Project identity card](assets/project-identity-card.md) | Capture findings and long-term project context when useful |
| [agents/openai.yaml](agents/openai.yaml) | Skill display metadata and default invocation prompt |
| [Jev guide](references/jev-checkpoints.md) · [Optional adapter](scripts/jev_check.py) | Bounded cards, official SDK calls, and interpreting results |
| [Evaluation record](evals/README.en.md) · [Boundary cases](evals/jev-cases.json) | Real-project experiment, reproducible material, and limitations |

Supporting material is read as needed. Short tasks do not require every template.

For outcome-based testing, use the [real-task evaluation procedure and fixed cases](evals/behavioral/README.md).
Judge delivered behavior, research contribution, scope, and effort separately;
package validation does not establish a quality improvement.

The [2026-10-02 outcome evaluation](evals/behavioral/2026-10-02.md) records navigation
trials against no skill and the published version, a saved-views task, browser
acceptance, replayable patches, and limitations (report in Chinese).

## License

[MIT](LICENSE)

## Maintainer validation

Repository maintainers can use Python 3.12 to install validation dependencies,
check the distributable package, and run the offline test suite:

```bash
python -m pip install -r scripts/requirements-dev.txt -r scripts/requirements-jev.txt
python scripts/validate_package.py
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

These dependencies and commands are for maintenance and validation; they are
not skill runtime dependencies. Everyday use only needs the Markdown
instructions. Jev SDK contract tests use a mock and do not send live API
requests.

The [Windows Claude Code evaluation](evals/discovery/README.md) separately checks
automatic invocation, negative controls, research contribution and delivered
behavior. It preserves failed cases and follow-up trials; successful invocation
does not establish that the deliverable passed acceptance.

The [2026-10-03 paired trials](evals/discovery/2026-10-03-quality-round.md) examine
stronger workflow discovery, option-rejection evidence and failure acceptance.
Invalid-input handling and source verification still have gaps; these results do
not establish reliable uplift. Inspect the actual artifact and evidence when
trying the skill.
