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

## Evidence Minimums

| Mode | Questions | Evidence | Edge cases | Verification |
|---|---:|---|---:|---|
| Direct | 1 | local/source-of-truth | targeted | exact check |
| Quick | 2-3 | 1 strong stream | 2-3 | focused test or inspection |
| Standard | 6 dimensions | 2 independent streams | 5+ | tests/build/artifact validation |
| Deep | 8-10 dimensions | 3+ streams, including primary | adversarial set | staged/dry-run/rollback plus full checks |

An evidence stream is a distinct authority or failure lens: local tests, official spec, production telemetry, user research, independent implementation, or experiment. Two articles quoting the same source are one stream.

## Task-Specific Adaptation

### Existing codebase

Inspect local source and tests first. External implementations are required only when reuse, unfamiliar technology, standards, or architecture choices are material.

### Writing or document work

Treat supplied facts and source material as primary evidence. Add style guides, audience examples, or templates only when they can affect structure, tone, compliance, or format.

### Product/design work

Combine actual user evidence when available with established product behavior or design systems. Do not substitute competitor screenshots for user needs.

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

## Failure Modes

| Failure | Correction |
|---|---|
| Research consumes more effort than the reversible change | Downgrade to Quick and validate directly |
| High-risk task uses only one source | Add independent primary evidence and rollback analysis |
| No network causes a total stop | Use local package/source/tests and a reversible experiment |
| Existing research is repeated | Create a freshness audit and resume |
| User already authorized execution but agent asks again | Report concise findings and continue |
| Checklist items are irrelevant | Mark inapplicable and focus on material uncertainty |
