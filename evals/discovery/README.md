# Discovery value and host invocation

This evaluation asks whether an ordinary short request leads to useful research
and a better deliverable. It separates **host invocation** from **discovery value**.
A host reading a skill establishes loading, not compliance or product quality.

## Host invocation

Use the real supported host in a fresh session. Mix ordinary feature requests,
adjacent mechanical/read-only requests, and an explicitly invoked positive
control. Keep model, provider, tools and task fixture constant across conditions.
Record the CLI version, effective skill paths and file hashes before executing.

Do not assume a project copy hides an older user copy with the same name. Check
the host's actual skill listing and the path it reads; isolate versions with a
documented per-run setting where supported, without editing global installation
or account configuration. Selection descriptions may be shortened when many
skills are installed, so record the exposed metadata if available.

For Codex, preserve `codex exec --json` events. A successful tool read of the
intended `SKILL.md` is loading evidence. Mentioning the skill in a final answer,
listing its filename, checking its hash, or the skill appearing in `skills/list`
does not establish loading. Treat errors, incomplete traces and timeouts as
unknown when they do not establish the tested claim. A positive trial may stop
after confirmed loading if that rule was frozen beforehand; its task completion
must then be marked **not evaluated**. A negative control needs to finish to
support a no-load conclusion.

These mechanics follow the official [skill discovery documentation](https://learn.chatgpt.com/docs/build-skills)
and [structured non-interactive events](https://learn.chatgpt.com/docs/non-interactive-mode).
The [official skill evaluation guide](https://developers.openai.com/blog/eval-skills)
also separates explicit, implicit and negative-control prompts. Use the installed
CLI's help for supported flags; older examples may show deprecated flags.

For Claude Code, use `.claude/skills` and the native `Skill` tool or explicit
`/research-first` invocation. Record successful invocation separately from a body
visible in the trace: a launch acknowledgement alone establishes only the former.
A successful target file read can expose the body without a native Skill call.
Preserve paired tool results and the base directory when available; otherwise
record the attribution limit and isolated project inventory. Its same-name
precedence also differs: a personal skill overrides a project skill. Check the
installed version against the [Claude Code skill documentation](https://code.claude.com/docs/en/skills)
and [CLI reference](https://code.claude.com/docs/en/cli-reference). Keep host results
separate; a Codex pass does not establish Claude Code behavior. Do not change the
user's global installation or provider settings to make an evaluation pass.

## Discovery and delivery

[cases.json](cases.json) contains two synthetic local fixtures and private-to-the-
worker acceptance criteria. Copy only the selected fixture into a fresh working
directory. Explicitly load a frozen skill revision for this experiment; automatic
selection belongs to the separate host test. Do not expose the rubric or earlier
outputs to the worker. Freeze the prompt, fixture hashes, limits and environment
before each condition starts.

Preserve the generated artifact, inspected sources, tool events, final response
and executed checks. Independently exercise the result and verify its relevant
source claims. Evaluate these dimensions separately, with 0–2 evidence-supported
judgments; do not turn their sum into a general quality score:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Relevance and proportion | Repeats the request or expands unrelated scope | Plausible addition with unclear local benefit | Addresses the actual local friction at proportionate cost |
| Incremental usefulness | No useful addition established | Generic or uncertain benefit | A consequential improvement beyond the prompt or obvious source inventory |
| Research contribution | Unsupported claim or source list | Research confirms an already proposed approach | An inspected fact introduces or materially revises an applicable option/check |
| Choice calibration | Adds unnecessary requirements or hides costs | Reasonable choice with incomplete tradeoff | Evidence, local cost and uncertainty support adoption or rejection |

Keep core correctness separate: a novel but broken deliverable does not pass.
One worthwhile finding is enough; extra features, sources, options or pages do
not earn additional credit. For a tiny task, research that confirms a simple
approach may be the right result even when incremental usefulness is modest.

For important findings, distinguish:

- **Required:** already explicit in the prompt.
- **Local:** learned directly from the supplied source or fixture.
- **Confirmation:** a prior candidate supported by subsequently inspected evidence.
- **Discovery:** an inspected fact introduced or changed the candidate.
- **Unknown attribution:** the trace does not establish where the idea came from.

Use the event order and actual inspected content for this distinction. A source
cited at the end or an idea absent from another trial does not prove discovery.
A comparable product demonstrates an existing workflow, not that its full design
fits this project. Documented behavior and behavior exercised in a live interface
must remain distinguishable.

After an observed miss, revise only the relevant instruction or resource. Rerun
the motivating case as a regression check, then use a fresh case for forward
evaluation. Repeat matched trials before claiming reliable uplift. The fixtures
here establish potential usefulness under their assumptions, not real users'
preferences or general improvement across models.

## Fixtures

- [Contact import](fixtures/contacts/README.md): plain local HTML/JavaScript with
  synthetic contacts and a representative CSV; no external service.
- [Newcomer guide](fixtures/onboarding/README.md): standard-library Python CLI
  with synthetic receipts; judge instructions against actual behavior.

These are maintainer evaluation resources, not mandatory steps or examples to
inject into ordinary user tasks. Keep output directories outside the repository
or under the ignored `results/` directory.

## Executed Windows evaluation

- [2026-10-03 paired quality round](2026-10-03-quality-round.md): three fixed-task
  pairs and one supplementary pair after detecting MCP inventory drift, covering
  workflow discovery, rejection premises and failure acceptance. It retains
  timeouts, failed artifacts, environment differences and reviewer-blinding limits.
- [Host activation](2026-10-02-windows-host.md): two implicit requests, two negative
  controls and one explicit control, each in a fresh native Claude Code process.
- [Discovery and delivery results](2026-10-02-windows-outcomes.md): baseline
  fixtures, one targeted revision, a regression and a fresh forward case.
- [Forward case](forward-case.json): a local reading-list backup/restore task,
  frozen before execution; its acceptance criteria stay private from the worker.
- [Artifact manifest](artifact-manifest.json): hashes for the preserved generated
  patches and guides. These artifacts contain known failures and are evidence,
  not recommended implementations. Apply patches only to a fresh copy of their
  corresponding fixture. Keep the original failed output when repairing a case.
