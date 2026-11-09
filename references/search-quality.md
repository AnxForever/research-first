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
| 2 | Official docs/specs/policies, including version-matched documentation tools | Supported contract, security, compliance, lifecycle |
| 3 | Primary implementation/tests/data | Edge behavior, integration details, reproducibility |
| 4 | Maintainer issues/releases/advisories | Known defects, drift, migration notes |
| 5 | Independent expert analysis | Alternative interpretation and operational experience |
| 6 | Blogs/forums/search summaries | Leads only; verify material claims |

The order changes by task. Production telemetry may outrank official performance claims; a legal policy may outrank an implementation example.

## Retrieval Tools and Version Scope

Check the host's callable tools before falling back on memory or a generic web
search. Documentation servers and MCP tools (for example Context7, DeepWiki, or a
vendor SDK's documentation server), package registries, and installed package
sources answer different questions. Prefer the route that observes the intended
contract; a tool appearing in a listing is availability, not a successful lookup.
With a library-documentation server such as Context7, resolve the library first,
then query it; request the version segment when the catalog exposes one.

1. Resolve the exact package. A lookup may return a similarly named project or an
   umbrella website. Confirm that the identifier belongs to the library the
   project actually imports.
2. Request the installed or target version when the tool supports it: a
   version-qualified library identifier, a tagged revision, or a version selector.
   A default or main-branch result may document a different major version than
   the project runs.
3. Check what came back: source URL, tag or branch, date, and API shape against
   the local manifest, lockfile or installed package. Treat unversioned results
   as leads rather than version-matched evidence.
4. Record the tool, query, identifier and version scope in the evidence note, so
   a later reader can tell what was actually inspected.

Send only the public identifier, API name or error text to an external
documentation service; keep private source, data and messages local.

A documentation tool states an intended contract. It does not show how this
application is wired or whether the assembled feature works; keep the local
integration check from [execution evidence](execution-evidence.md). When the
needed tool is missing or broken, see [research tools](research-tools.md) for
what to check first and how to propose an installation without changing the
user's environment unasked.

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
3. Follow the relevant implementation far enough to verify the claimed behavior; file count is not the goal.
4. Read tests that demonstrate lifecycle and failure behavior.
5. Inspect relevant issues or advisories for hidden constraints.
6. Compare with an independent implementation or official specification.

Popularity is a weak signal. Prefer version fit, tests, maintainership, and architectural similarity over stars.

Useful query dimensions include problem wording, protocol/API name, failure message, security boundary, migration path, language/framework, organization, file path, and target version. Use current dates rather than hard-coded year filters.

For a substantial feature, search for existing solutions even when a custom
implementation seems straightforward. Search by the user's workflow as well as
technical names so the agent's familiar libraries do not become the whole shortlist.
Use [reuse-and-alternatives.md](reuse-and-alternatives.md) to turn findings into
visible options; a search that never informs the user or the decision is incomplete.

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
- High-risk claim or consequential disagreement: require primary evidence plus an independent stream.
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
- Answering a library or API question from memory when a documentation tool was available
- Treating a default-branch or unversioned documentation result as the installed version
- Reading README without tests for behavior-critical claims
- Hard-coded recency filters that age poorly
- Treating popularity as correctness
- Copying without license review
- Collecting sources without recording decisions
- Repeating prior research instead of auditing freshness
