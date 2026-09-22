# Adapting Research Depth

Use this guide when task risk, novelty, time, or evidence access makes the default depth unclear.

## Depth Score

Score each factor from 0 to 2:

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Reversibility | trivial rollback | moderate cleanup | destructive/hard to undo |
| Impact | personal/local | team/customer-facing | money, privacy, security, regulated, core platform |
| Novelty | known pattern | some unknowns | unfamiliar or no precedent |
| Coupling | isolated | several dependencies | cross-system/data migration |
| Evidence conflict | aligned | incomplete | contradictory |

- 0-2: Direct or Quick
- 3-5: Standard
- 6-10: Deep

User urgency can narrow scope, but it does not justify skipping safeguards for destructive or high-impact work.

## Evidence Needed

The score is a starting point, not a quota or permission to ignore a material risk.
A substantial new feature needs Standard research even if coding it feels familiar.

| Mode | Evidence | Failure coverage | Verification |
|---|---|---|---|
| Direct | Local source of truth | Behavior affected by the exact edit | Exact check |
| Quick | Strong source or experiment resolving the bounded unknown | Relevant boundary cases | Focused test or inspection |
| Standard | Local/user context, relevant existing solutions and primary guidance, credible alternatives | Material states, lifecycle, and failures | Checks tied to acceptance criteria |
| Deep | Independently corroborated consequential claims | Adversarial cases and recovery | Staged/dry-run/rollback checks as applicable |

An evidence stream is a distinct authority or failure lens: local tests, official spec, production telemetry, user research, independent implementation, or experiment. Two articles quoting the same source are one stream.

## Task-Specific Adaptation

### Existing codebase

Inspect local source and tests first. For substantial new or redesigned features,
investigate existing products, reusable implementations, and primary guidance before
custom work. Do not assume that knowing how to implement it makes reuse irrelevant.
Mechanical edits and bounded diagnoses may stay local when local evidence resolves
the question. Resume valid, feature-specific comparisons instead of repeating them.

### Writing or document work

Treat supplied facts and source material as primary evidence. For substantial new
deliverables, investigate relevant exemplars, templates, standards, or methods that
could improve the result. Supplied/local materials may provide that comparison;
do not force software-library research onto writing work.

### Product/design work

Combine actual user evidence with established product behavior and design systems.
For substantial frontend work, investigate relevant component libraries, specialized
components, and interaction or animation resources where appropriate. Show credible
options and tradeoffs before implementing. A screenshot is not proof of usability,
and motion is not a requirement simply because an animation library exists.

### Diagnosis

Prefer reproduction, logs, traces, recent diffs, and source flow. External search supports hypotheses but does not replace local evidence.

### Operations and migrations

Escalate for destructive actions. Pin target versions, inspect live state read-only, define rollback, and use dry runs or staged rollout where supported.

### Continuing prior work

Audit freshness instead of restarting. Recheck only evidence invalidated by new requirements, changed dependencies, code changes, or elapsed time.

## When Evidence Is Unavailable

After reasonable attempts:

1. State what could not be verified and why.
2. Separate facts, inferences, and assumptions.
3. Choose the most reversible path.
4. Add instrumentation or tests that expose wrong assumptions early.
5. Ask the user only when the gap creates a material irreversible choice or requires new authority.

Research unavailability is not evidence that no existing solution exists. Clearly
label a provisional custom implementation and avoid locking in a choice that still
requires the user's answer. No answer is not approval. If the user delegated the
selection and the path is reversible, disclose limitations and continue.

## Failure Modes

| Failure | Correction |
|---|---|
| Research consumes more effort than the reversible change | Downgrade to Quick and validate directly |
| High-risk task uses only one source | Add independent primary evidence and rollback analysis |
| No network causes a total stop | Use local package/source/tests and a reversible experiment |
| Existing research is repeated | Create a freshness audit and resume |
| User already authorized execution but agent asks again | Report concise findings and continue |
| Checklist items are irrelevant | Mark inapplicable and focus on material uncertainty |
