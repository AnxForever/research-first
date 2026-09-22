# Per-Feature Evidence Ledger

Use this ledger for multi-feature work, inherited behavior, or work that spans sessions. Its purpose is to connect each material outcome to its design evidence, reuse choices, and verification. A project bibliography cannot establish coverage for every feature.

## Inventory and Scope

State the active outcome and scope before building the inventory. Include every material capability within that scope: promised, planned, implemented, hidden, disabled, inherited, and operational. Reconcile the inventory against relevant user promises, artifacts, routes, controls, APIs, schemas, flags, tests, configuration, and operating instructions.

A feature is a user or audience outcome, or a lifecycle that can fail independently. Split authentication from session renewal and revocation when their decisions and failure modes differ. Do not create a row for every file or component. For non-code work, units may be a report's evidence claims, an audience workflow, or a decision with separate acceptance conditions.

Whole-project construction or assessment requires a whole-project inventory. A scoped change requires a complete inventory of the affected capabilities and dependencies. Record discovered out-of-scope gaps separately; finding them does not authorize fixing them. A low-risk mechanical change can remain one unit without creating a project ledger.

## Compact Record

Use a table with linked detail, short cards, or an existing research document. Keep stable IDs when names or implementation choices change. Child records identify their parent; shared evidence may be linked, but each child explains which of its decisions that evidence supports.

```text
Feature ID / parent: stable ID / parent ID or none
User outcome: what success changes, with hard constraints
Scope / lifecycle: included states and boundaries; exclusions
Priority / task scope: risk or dependency priority; in scope or observation only
Delivery: idea | planned | implemented | enabled | operational | deprecated
Evidence coverage: covered | partial | gap | stale
Historical gap: none | inherited-unassessed | previously-overclaimed |
                reopened-by-change | backfilled

Decision questions: material uncertainties and evidence that could disprove the approach
Local evidence: source, artifact, runtime observation, user evidence; what it establishes
Primary guidance: relevant specification, documentation, policy, or original source
Prior art / candidates: relevant products, open-source implementations, tools,
                       libraries, technical resources, or reusable artifacts
Candidate comparison: fit, lifecycle/failures, compatibility, maintenance,
                      license/rights and cost where relevant; inspected sources
Implementation strategy: reuse | adapt | combine | build; rationale and alternatives
Candidate judgments: what was adopted, adapted, combined, learned from, or declined
User-facing options: where/when candidates, tradeoffs, and recommendation were shown;
                     selected option, existing delegation, or material choice still open
Acceptance / failure evidence: required checks, observed results, and unverified cases
Freshness: source versions/dates/commits and conditions that invalidate the decision
Gap history: dated events retaining original reasons, evidence, actions, and outcome
Next action: unresolved question or verification, owner if useful
```

Use actual source locators and name the claim each supports. Mark inapplicable fields with a short reason. Do not fill missing evidence with invented citations, assumed user decisions, or generic links.

## Research and Reuse for Every Material Feature

Before substantial implementation of each feature, actively investigate relevant products, open-source implementations, technical resources, and primary documentation. Identify existing solutions before choosing a custom implementation. Reuse current prior research when its applicability to this feature is explicit.

For frontend work, include relevant component libraries and animation libraries or existing motion facilities. Assess interaction states, accessibility, reduced motion, compatibility, and integration cost where applicable. For documents and other non-code work, investigate relevant established outputs, templates, methods, source material, and reusable tools.

Inspect enough of serious candidates to establish fit: documentation plus relevant source, tests, live behavior, or examples as available. A list of package names is discovery, not a comparison. Record what can be adopted directly, adapted, combined, or declined. Custom work is a valid decision when the comparison supports it.

Show the user a concise shortlist with useful links, tradeoffs, and a recommendation before committing to the implementation choice. Include viable alternatives even when recommending custom work. Record that update in the ledger; a private shortlist does not satisfy disclosure. If execution and routine choices are delegated, present the options and continue with the recommendation. Wait only for a material choice that existing instructions do not resolve.

When relevant evidence or candidates cannot be found, record what was checked and the limitation. Do not imply that no solution exists merely because a search failed. Keep the gap visible and use a reversible, verified path when authorized.

## Coverage Means Design Support

| Coverage | Meaning |
|---|---|
| `covered` | Current, feature-specific evidence supports the material design and lifecycle decisions; relevant reuse candidates were assessed and disclosed; remaining uncertainty is explicitly bounded. |
| `partial` | Relevant support exists, but a material decision, lifecycle, candidate comparison, or user-facing disclosure is still incomplete. |
| `gap` | No adequate feature-specific design basis is recorded. Intuition, generic project research, code existence, or passing tests alone cannot establish it. |
| `stale` | Previously relevant evidence no longer establishes fit because requirements, versions, context, or runtime behavior changed. |

Official specifications establish intended contracts; implementation source, tests, and observations establish behavior under their conditions. They can support a decision together when matched to the target version and environment. Investigate material disagreements instead of treating either as automatically conclusive.

Tests can verify a researched acceptance condition or expose a wrong assumption. They do not independently show that the chosen outcome, security boundary, or reuse decision serves the user's purpose. Keep design support and verification results separate. A well-supported design can be unimplemented or fail verification; an operational implementation can still have a research gap. Completion claims require the relevant delivery and verification evidence as well as honest coverage.

## Backfill Without Erasing History

1. Record the original gap and its cause before backfilling. Use `inherited-unassessed` for missing inherited rationale, `previously-overclaimed` for an unsupported coverage claim, and `reopened-by-change` when a change invalidated prior support.
2. Research the affected outcome and lifecycle, including alternatives that could overturn the existing design. Backfill before preserving or extending material inherited behavior; record any unavoidable evidence limitation rather than grandfathering it.
3. Update the decision, user-facing options, constraints, and acceptance evidence. Record whether the design was confirmed, changed, or rejected; research need not force a change to be useful.
4. Update current coverage independently. Set the historical marker to `backfilled` only when the recorded research gap has been addressed; leave unresolved dimensions `partial`, `gap`, or `stale` as appropriate.
5. Append a dated history event with the prior cause and state, new evidence, outcome, and residual gaps. Never replace the original cause with the single word `backfilled` or reset history to `none`. Later regressions append new events.

For example, an event sequence may retain `inherited-unassessed: no revocation research` followed by `backfilled: revocation evidence added; design revised`. The current record can be `covered` while that history remains intact. If only renewal was researched, the revocation gap remains open.

On resume, inspect freshness and unresolved decisions. Recheck evidence affected by change; reuse valid work instead of repeating the entire survey.

## Hypothetical False Positives

These examples illustrate judgments, not measured project outcomes or real source citations.

| Apparent coverage | Correct judgment and action |
|---|---|
| An authentication research document exists, so a newly added logout and token-revocation flow is marked covered. | The parent bibliography does not establish revocation behavior. Create or assess the child lifecycle, map applicable evidence, and research its missing decisions. |
| An inherited job scheduler passes restart tests, so its persistence and worker-coordination design is marked covered. | Record what the tests actually demonstrate. Missing design and candidate evidence remains a gap; inspect documented contracts and relevant implementations before extending it. |
| A custom modal works in a screenshot, and a private note names two libraries. | Visual output and package names do not establish interaction, accessibility, or reuse fit. Compare applicable components and motion facilities, then show the user the viable choices and recommendation. |
| A report's outdated methodology was researched and corrected, so its prior unsupported claims are removed from the history. | Current coverage may improve; retain the stale or overclaimed reason and append the correction with its evidence. Successful backfill does not erase the earlier gap. |
