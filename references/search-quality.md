# Evidence and Search Quality

## Start With the Question

Write the uncertainty in a testable form before choosing a source:

```text
What must be true for this approach to work in this environment?
What evidence would disprove it?
Which version, audience, scale, or policy applies?
```

Search by problem, competing solution, failure mode, and authoritative owner. Avoid queries that assume the preferred answer.

## Source Priority

| Priority | Source | Use for |
|---|---|---|
| 1 | Local system/source of truth | Current behavior, constraints, data, conventions |
| 2 | Official docs/specs/policies | Supported contract, security, compliance, lifecycle |
| 3 | Primary implementation/tests/data | Edge behavior, integration details, reproducibility |
| 4 | Maintainer issues/releases/advisories | Known defects, drift, migration notes |
| 5 | Independent expert analysis | Alternative interpretation and operational experience |
| 6 | Blogs/forums/search summaries | Leads only; verify material claims |

The order changes by task. Production telemetry may outrank official performance claims; a legal policy may outrank an implementation example.

## Quality Signals

Evaluate evidence on:

- Authority: is the source responsible for the contract or result?
- Proximity: does it observe the actual system or audience?
- Version match: does it apply to the installed/target version and date?
- Reproducibility: can the behavior or claim be checked?
- Independence: is it genuinely separate from other evidence?
- Completeness: does it include failure cases, not only the happy path?
- Maintenance: is it current and acknowledged by maintainers?
- Incentives: is it documentation, marketing, advocacy, or neutral measurement?
- License/rights: may code, data, media, or templates be reused?

## Repository Research

When code reuse or implementation patterns are material:

1. Pin a release, tag, or commit.
2. Check license, recent activity, releases, and CI.
3. Read at least two core source files relevant to the question.
4. Read tests that demonstrate lifecycle and failure behavior.
5. Inspect relevant issues or advisories for hidden constraints.
6. Compare with an independent implementation or official specification.

Popularity is a weak signal. Prefer version fit, tests, maintainership, and architectural similarity over stars.

Useful query dimensions include problem wording, protocol/API name, failure message, security boundary, migration path, language/framework, organization, file path, and target version. Use current dates rather than hard-coded year filters.

## Product and Design Research

Use live products, official design systems, accessibility guidance, user studies, analytics, and support feedback. Record:

- target user and job-to-be-done;
- hierarchy and interaction flow;
- empty/loading/error/success states;
- accessibility and responsive behavior;
- what is convention versus brand-specific styling;
- evidence that the pattern works for the intended audience.

Do not infer business success from visual polish alone.

## Quantitative and Scientific Research

Prefer original datasets, methods, standards, peer-reviewed work, and reproducible benchmarks. Check sample definition, denominators, uncertainty, confounders, leakage, and whether the metric matches the user's decision.

Never merge numbers from incompatible populations or time periods without explicit normalization.

## Operational Research

Pin the target environment and exact version. Verify prerequisites, permissions, credential scope, rate limits, backups, rollback, blast radius, and observable success criteria. Use read-only checks and dry runs before writes when supported.

## Corroboration Rules

- Material claim: support with primary evidence or label as inference.
- High-risk claim: require primary evidence plus an independent stream.
- Conflicting sources: prefer version-matched, reproducible, proximate evidence and document the conflict.
- No source: state the gap and use a reversible experiment rather than presenting a guess as fact.

## Search Stop Conditions

Stop researching when:

- the important uncertainty is resolved enough to choose safely;
- additional sources repeat known information;
- a prototype/test can answer faster and more directly;
- remaining uncertainty is explicitly accepted and contained by rollback or validation.

Continue when:

- evidence changes the architecture or safety boundary;
- sources disagree on material behavior;
- version applicability is unclear;
- edge cases or failure recovery remain unknown.

## Anti-Patterns

- First-result bias
- GitHub-only or web-only evidence
- Reading README without tests for behavior-critical claims
- Hard-coded recency filters that age poorly
- Treating popularity as correctness
- Copying without license review
- Collecting sources without recording decisions
- Repeating prior research instead of auditing freshness
