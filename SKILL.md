---
name: research-first
description: >-
  Understand user intent and research existing products, open-source solutions,
  reusable libraries, and primary documentation before choosing how to implement
  a substantial feature, design, integration, or other deliverable. Use for
  research requests, compressed ideas, proposed technologies, frontend work that
  could reuse components or animation libraries, and doubts about ongoing work.
  Surface viable alternatives and tradeoffs before building from scratch. Skip
  routine lookups and fully specified, low-risk mechanical edits. Resume valid
  research rather than repeating it.
---

# Research First

Understand the outcome, find how others solve it, and give the user an informed
choice before implementing. Do not make the user's vocabulary or the agent's
memory the limit of the solution. Research must change or substantiate decisions,
not merely produce a source list.

## Operating Contract

1. Treat every user request, idea, and suggestion as compressed evidence of intent, not automatically as a complete specification.
2. Establish what is already known before searching.
3. Match research depth to risk, novelty, reversibility, ambiguity, and user urgency.
4. Use the evidence types that fit the task; do not force every task into GitHub research.
5. Prefer primary evidence and independently corroborate material claims.
6. Convert findings into an expanded problem definition, decisions, implementation constraints, and tests.
7. If the user already authorized execution and no material user choice remains unresolved, continue after a concise research update. Ask only about missing authority or a consequential choice, not permission already given.
8. Preserve an evidence trail sufficient to explain important decisions without flooding the user.
9. Treat every material feature and independently failing lifecycle as its own research unit. Project-level research does not automatically cover its subfeatures.
10. Maintain a complete feature inventory within the task's scope, including promised, implemented, hidden, disabled, inherited, and operational capabilities. An unlisted feature is an unassessed gap, not implicitly covered.
11. Mark inherited features with missing, stale, indirect, or generic evidence as historical research gaps; do not grandfather them as correct or erase the historical marker after later backfill.
12. Before implementing a substantial feature, investigate relevant products, reusable implementations or assets, and primary guidance. Local inspection establishes context; it does not replace investigating suitable existing solutions.
13. Show credible alternatives, a recommendation, and material tradeoffs before committing to implementation. Reuse is a choice, not an obligation; building from scratch also needs an evidence-backed reason.

## Step 0: Resume Before Restarting

First inspect the conversation, active plan/goal, existing research notes, recent commits, and current workspace state.

- Reuse research that is recent, source-grounded, and still relevant.
- Verify only assumptions affected by new code, changed requirements, version drift, or external state.
- Do not repeat completed searches merely to satisfy a checklist.
- When inheriting a task, record what is established, uncertain, and stale.

### Maintain a Per-Feature Evidence Ledger

For multi-feature products, refactors, and long-running goals, create or update a compact feature evidence ledger before substantial implementation. A feature is a user-visible outcome or independently failing lifecycle, not merely a file, component, endpoint, or sprint item. Inventory every such feature within the task's scope; whole-product work needs a whole-product inventory. Record discovered out-of-scope gaps without silently expanding into unrelated remediation.

For each feature record a stable feature ID, parent capability, lifecycle scope, user outcome, delivery state, local/runtime evidence, primary guidance, mature product or open-source evidence, reuse alternatives and the choice shown to the user, acceptance and failure evidence, current coverage, historical gap state, and priority.

Use **covered** only for current feature-specific evidence that supports material lifecycle, security, UX, and failure decisions. Use **partial** when a material dimension remains unverified, **gap** when the implementation rests on intuition, user wording, generic project research, code existence, or tests, and **stale** when versions, requirements, runtime state, or product direction changed.

When touching inherited behavior, inspect its ledger entry, treat missing feature-specific research as a live reasoning defect, seek evidence that could reverse the implementation, and backfill before preserving or extending it. Tests prove behavior under their coverage; they do not prove that behavior is the right decision.

Keep **delivery state**, **current evidence coverage**, and **research history** separate:

- Delivery state: `idea`, `planned`, `implemented`, `enabled`, `operational`, `deprecated`.
- Evidence coverage: `covered`, `partial`, `gap`, `stale`.
- Historical gap: `none`, `inherited-unassessed`, `previously-overclaimed`, `reopened-by-change`, `backfilled`.

Backfilling may improve current coverage, but it must retain the original gap type, reason, and supporting evidence alongside the `backfilled` event. Before planning broad work, reconcile the in-scope inventory against product copy, routes, controls, APIs, schemas, flags, tests, deployment configuration, operations docs, and prior completion claims. Add every missing item as `gap` before implementation.

Read [references/feature-evidence-ledger.md](references/feature-evidence-ledger.md) for the structure and backfill rules.

### Interpret Every User Input by Intent

Apply this to initial requests, short ideas, rough descriptions, follow-up messages, examples, corrections,
technology names, and proposed implementations. Users often contribute inspiration, symptoms, partial domain
knowledge, or a preferred direction with limited wording. Treat the message as evidence about the desired outcome,
not automatically as a complete or literal specification.

Before acting, separate the message into:

```text
Underlying purpose: what outcome, pain, risk, or quality bar the user is trying to change
Hard constraints: explicit boundaries that must be followed
Candidate means: examples, technologies, wording, or implementation ideas that may be adapted
Open assumptions: details the user may be implying but has not established
Missing dimensions: needs, users, lifecycle, failure modes, tradeoffs, and acceptance evidence not yet expressed
Impact on active goal: create, refine, extend, correct, or replace
```

Use the surrounding conversation, active goal, current artifacts, and evidence to infer purpose. Prefer the
interpretation that best advances the durable user outcome while preserving explicit constraints. Do not copy the
user's nouns, decomposition, or proposed mechanism into the plan merely because they were mentioned.

For each material request or suggestion:

1. Restate its intended effect internally in outcome language.
2. Expand the compressed idea into the relevant product, technical, operational, and human questions.
3. Research the local problem, user context, relevant prior art, and authoritative guidance before choosing a mechanism.
4. Look for needs, risks, opportunities, and established solutions the user did not have space or vocabulary to name.
5. Test whether the proposed means is sufficient, compatible, and the best fit.
6. Classify proposed means as **adopt**, **adapt**, **combine**, or **decline**, with evidence.
7. Update the objective, plan, and acceptance evidence around the expanded purpose, not the user's phrasing.

The agent is responsible for adding justified depth. Do not limit the solution to the concepts the user happened to
mention. Bring back relevant missing considerations and stronger options discovered through research, while avoiding
scope expansion that does not serve the inferred purpose.

Use an **interpretation confidence** before committing to the expanded frame:

- **High:** context and evidence strongly support the inferred purpose; proceed and briefly state the interpretation.
- **Medium:** several interpretations are plausible but a reversible path serves them all; proceed with labeled assumptions.
- **Low:** interpretations imply materially different, costly, destructive, or externally visible outcomes; research what
  can be discovered, then ask one focused question before crossing that decision boundary.

Expansion is justified only when it passes all three tests:

1. **Relevance:** it directly improves the inferred user outcome or prevents a material failure.
2. **Evidence:** local facts, authoritative guidance, user context, or a safe experiment supports it.
3. **Proportionality:** its cost and complexity match the task's stakes.

If an addition fails one of these tests, omit it or present it as an optional follow-up rather than silently enlarging scope.

An explicit hard constraint, exact artifact, or deliberately chosen method is binding immediately; the user
does not need to confirm it twice. Research how to implement it correctly within that boundary. If it conflicts
with the larger purpose, explain the conflict and ask before substituting a different method. Treat genuinely
ambiguous mechanisms as candidates, using context and evidence to interpret them.

Examples:

- "Add browser skills" may express a need for agents to complete web workflows reliably. Research browser
  automation, permission boundaries, session isolation, and observability before deciding whether that means a
  skill, MCP server, built-in tool, or combination.
- "Make it like Vercel" usually defines qualities such as restraint, hierarchy, density, and interaction behavior;
  it does not require copying every token or layout regardless of the product's workflows.
- "Use Redis" may signal a need for shared state, durability, coordination, or speed. Verify which problem exists
  before introducing Redis.

For an initial request, use the expanded intent to frame the goal before planning. For later input, if it changes only
the means, continue toward the existing goal with an evidence-based adaptation. If it changes the desired outcome or
scope materially, state that interpretation explicitly and revise the goal or plan rather than silently mixing
incompatible objectives.

### Treat User Doubt as a Reassessment Trigger

When the user questions the work—explicitly or indirectly—assume the current reasoning may have missed their purpose,
used weak evidence, made an unsupported assumption, or optimized the wrong outcome. Examples include "Are you sure?",
"This still feels wrong," "Why are you doing this?", "Is that enough?", corrections, repeated requests, and a change
in tone that indicates lost confidence.

Pause the affected course of action long enough to run a focused reassessment:

1. Identify exactly what claim, assumption, interpretation, or result the doubt concerns.
2. Reconstruct the user's intended outcome from the full conversation, not only the latest objection.
3. Inspect the current artifact and evidence; distinguish what is proven, inferred, stale, or absent.
4. Seek new evidence that could falsify the current approach, not only sources that support it.
5. Compare three possibilities: the work is sound but poorly explained; the direction is right but incomplete; the
   underlying framing or solution is wrong.
6. Continue, revise, or reverse based on evidence, and explain the correction concretely.

Do not treat doubt as an instruction to agree automatically. Reflexive deference is another form of shallow literalism.
Likewise, do not defend sunk work merely because it already exists. The purpose of reassessment is to recover alignment
and truth, not to preserve either party's first position.

For ambiguous intent, conflicting signals, or skill evaluation, read
[references/intent-interpretation-evaluation.md](references/intent-interpretation-evaluation.md).

## Step 1: Frame the Work Context

Create a short context brief. For a codebase, inspect README, architecture docs, configuration, tests, and recent history. For a document or decision, inspect the supplied artifact, audience, constraints, and desired outcome.

```text
Subject: project, artifact, system, or decision
Outcome: what success changes for the user
Users/audience: who consumes or is affected by it
Constraints: security, compatibility, policy, time, cost, tone, format
Current state: what exists and what is already proven
Unknowns: uncertainties that could change the approach
Failure cost: impact and reversibility if wrong
```

Do not invent missing identity details. Infer only from evidence and label assumptions.

## Step 2: Choose Research Depth

Use the smallest depth that responsibly reduces the important uncertainty.

| Mode | Use when | Minimum evidence |
|---|---|---|
| Direct | Mechanical or fully specified, low-risk change | Local/source evidence and targeted verification |
| Quick | Familiar, reversible task with one meaningful unknown | Resolve that unknown with a strong source or experiment |
| Standard | Substantial feature, design, plan, integration, or deliverable | Local/user context, relevant prior art and primary guidance, credible alternatives, material lifecycle and failure cases |
| Deep | High-impact or hard-to-reverse work, core architecture, conflicting evidence | Independently corroborate consequential claims; investigate adversarial cases and recovery/rollback |

A familiar library does not make a new feature mechanical. Substantial frontend work needs the existing-solution investigation in Step 4 even when the agent knows how to code it. Do not pad sources or edge cases to meet a quota, or use proportionality to skip a material uncertainty or reuse investigation.

Escalate depth when evidence conflicts, the domain is unfamiliar, the action is hard to reverse, or the user previously found the work shallow. Reduce breadth—not validation integrity—when time is constrained.

Read [references/adapting-depth.md](references/adapting-depth.md) for depth scoring, per-task adaptation, and what to do when evidence is unavailable.

## Step 3: Expand the Real Question

Select the dimensions that can materially affect the outcome. Investigate uncertain dimensions before dismissing them; cover all material ones at the chosen depth rather than meeting a numeric quota.

1. Outcome and acceptance criteria
2. Data, inputs, provenance, and validation
3. Lifecycle, state transitions, shutdown, and recovery
4. Integration boundaries and dependencies
5. Security, privacy, authorization, and abuse cases
6. Performance, scale, cost, and resource limits
7. Observability, auditability, and diagnosis
8. API, UX, accessibility, and human workflow
9. Configuration, environments, and deployment
10. Testing, compatibility, migration, and evolution

Omit irrelevant dimensions explicitly rather than filling them with generic prose. Use [references/problem-expansion.md](references/problem-expansion.md) for unfamiliar domains.

When the request contains a proposed solution, expand both questions separately:

- **Purpose question:** What result would make the user's underlying problem meaningfully better?
- **Means question:** Which mechanism best produces that result in this context?

Research must be allowed to change the means. Otherwise it is confirmation work, not research-first work.

## Step 4: Select Evidence Streams

Choose evidence by the question being answered. Two streams are independent when they arise from different failure modes or authorities—not merely two pages repeating the same claim.

| Evidence stream | Best for |
|---|---|
| Local source, tests, history, configuration | Existing behavior, conventions, constraints, regressions |
| Official docs, standards, specifications, policy | Supported contracts, lifecycle, security and compliance requirements |
| Maintainer source and tests | Real implementation details and edge behavior |
| User-provided files, examples, feedback, analytics | Actual requirements, audience, defects, and usage patterns |
| Production logs, metrics, traces, database inspection | Operational reality and scale |
| Competitors, reference products, design systems | Expected UX, positioning, interaction patterns |
| Papers, benchmarks, authoritative datasets | Algorithms, scientific or quantitative claims |
| Safe prototypes, spikes, dry runs, experiments | Feasibility and ambiguous runtime behavior |

### Investigate Existing Solutions Before Custom Work

For every substantial feature or deliverable, actively investigate:

- **Products and prior work:** how established products or practitioners solve this user problem, including workflows, states, and tradeoffs.
- **Reusable implementations and assets:** suitable open-source projects, SDKs, libraries, components, templates, or existing local modules; what can be reused, adapted, combined, or learned from.
- **Primary guidance and better techniques:** documentation, specifications, maintainer material, and domain references that could improve the approach.

For frontend work, explicitly look for relevant open-source component libraries, specialized components, and interaction or animation libraries where motion serves the requested experience. Compare them with the existing stack and design system. Check required states, accessibility, styling flexibility, integration cost, maintenance, and license as relevant. Do not invent an animation requirement just to add a library.

Start from local constraints, then investigate external candidates. Familiarity or a tight schedule is not a reason to silently default to hand-building. Reuse an earlier comparison when it covers this feature and remains current. If research access is unavailable, disclose the gap; do not claim no reusable solution exists.

For serious code reuse candidates, inspect relevant core source, tests, official APIs, or runnable examples rather than only a README. Compare credible alternatives using evidence relevant to the actual choice.

Read [references/reuse-and-alternatives.md](references/reuse-and-alternatives.md) for the investigation and user-facing choice.

Read [references/search-quality.md](references/search-quality.md) for source priority, quality signals, corroboration, stop conditions, and anti-patterns.

## Step 5: Gather Evidence Efficiently

- **Local-first tasks.** Start with the workspace. Search narrowly, follow data/control flow, inspect nearby tests, and check recent changes. For substantial features, continue with Step 4's investigation of prior art and reusable resources even if the local implementation seems straightforward. Mechanical edits and bounded diagnoses need external research only when it can resolve a relevant unknown.
- **External research.** Prefer official documentation and specifications, then primary source and maintainer artifacts, then independent analysis. Pin versions, dates, commits, or document revisions when behavior can drift. Check license before copying code or assets.
- **Creative and design work.** Study relevant exemplars, templates, style guides, and reusable assets; extract structure, interaction, visual language, states, accessibility, and the reason the example works. Do not add design research to a backend-only change unless it affects a user-facing contract.
- **Operational actions.** Research the exact target version and environment. Prefer read-only inspection and dry runs. Identify rollback, blast radius, credential scope, and success signals before mutating state.
- **Restricted or offline environments.** Use available local docs, vendored source, lockfiles, installed package metadata, tests, fixtures, and experiments. If primary evidence is unavailable: state the evidence gap; distinguish fact, inference, and assumption; proceed with a reversible best-effort path when the user has authorized it; ask only if the missing evidence creates a material, irreversible choice.

Read [references/search-quality.md](references/search-quality.md) for per-domain research rules and [references/adapting-depth.md](references/adapting-depth.md) for evidence-unavailable conditions.

## Step 6: Synthesize, Do Not Accumulate

For each important finding, capture:

```text
Question → Evidence → Confidence → Decision/constraint → Verification
```

Resolve conflicts by preferring evidence that is primary, version-matched, reproducible, maintained, and closest to the actual environment. Document consequential conflicts and why one source won.

Use [references/contradictions.md](references/contradictions.md) when sources disagree on a material claim or implementation choice.

Classify reuse decisions:

- REUSE: compatible, licensed, maintained, and fits directly.
- ADAPT: sound pattern but local constraints require changes.
- LEARN-FROM: useful principle, incompatible implementation or license.
- REJECT: evidence shows it does not fit.

The resulting implementation strategy may be **reuse**, **adapt**, **combine**, or **build**. Before committing to substantial implementation, show credible candidates and their sources, what each provides, material costs, your recommendation, and what remains custom. Include a viable alternative when one exists, especially when recommending custom work. Explain why promising candidates were declined; do not invent weak alternatives just to fill a table. Keep independent choices separate: reusing table state does not imply adopting row animations, and lightweight visuals do not imply hand-building the table logic.

Give the user an opportunity to choose when viable options entail a material product, dependency, cost, maintenance, or visual tradeoff they have not delegated. Recommend one and ask one focused question before dependent implementation; continue independent work while waiting. If the user already chose or authorized you to decide, disclose the comparison and proceed. Routine compatible details do not require a vote for every package. Do not hide reusable options until the final report.

## Step 7: Readiness Gate

Before creating or changing anything substantial, confirm:

- [ ] Context and desired outcome are understood.
- [ ] Research depth matches risk and novelty.
- [ ] Material unknowns were expanded across relevant dimensions.
- [ ] Primary evidence was used where available.
- [ ] Material claims have independent support or are labeled uncertain.
- [ ] Material lifecycle and failure cases are addressed with evidence appropriate to the stakes.
- [ ] Security and failure/rollback were considered when relevant.
- [ ] Reuse/license/version decisions are explicit when relevant.
- [ ] Findings map to implementation constraints and verification.
- [ ] The proposed action fits the user's authority and scope.
- [ ] User input was separated into purpose, constraints, candidate means, assumptions, and missing dimensions.
- [ ] The plan optimizes for the inferred outcome rather than mirroring the latest wording.
- [ ] Every material feature being changed has a ledger entry or is explicitly one low-risk mechanical unit.
- [ ] Existing features with weak historical evidence are marked partial/gap/stale rather than presumed correct.
- [ ] Relevant reusable options were investigated and shown to the user, or the research gap is disclosed.
- [ ] Any material choice requiring the user's answer has actually been resolved.

If a box is inapplicable, mark it inapplicable rather than manufacturing research.

## Step 8: Report and Act

Give a concise research update before substantial implementation:

```markdown
Research summary: [topic]

- Context: [what matters locally]
- Evidence: [primary streams and pinned versions]
- Corrections: [assumptions changed by evidence, if any]
- Edge cases: [important cases and mechanisms]
- Decision: [reuse/adapt/learn-from/reject]
- Options: [credible candidates and sources, benefits, costs, recommendation, and remaining custom work]
- Execution plan: [ordered slices and verification]
```

Then:

- If execution is already authorized and no material user choice remains unresolved, continue immediately.
- If the user asked only for analysis/review, stop at findings.
- If a missing choice materially changes scope, cost, risk, or external state, ask that question.
- If research disproves the requested approach, explain the evidence and propose the closest viable alternative.

Use [assets/research-report-template.md](assets/research-report-template.md) for a written decision report and [assets/project-identity-card.md](assets/project-identity-card.md) for reusable context when useful. Keep the update proportional; it need not repeat a comparison already shown in Step 6.

## Step 9: Verify and Self-Audit

After execution, test in proportion to risk and revisit the evidence-to-decision chain.

- Confirm the implementation addresses the researched edge cases.
- Run relevant tests, builds, lint/type checks, dry runs, or artifact inspection.
- Check for new TODOs, stubs, unsupported claims, or stale docs.
- Report known residual risks and unverified external assumptions.
- Do not claim completion because research or coding is extensive; claim it only when the requested outcome is achieved.
- Compare the result against both failure directions: literal under-interpretation and speculative over-interpretation.
- Confirm every added requirement traces to user purpose plus evidence, and every explicit constraint remains intact.
- Update the feature ledger with implementation evidence, remaining gaps, source versions/dates, and any design reversal caused by research.

## Optional Jev Checkpoints

When the user enables Jev, use [references/jev-checkpoints.md](references/jev-checkpoints.md)
for bounded second opinions after intent interpretation, source inspection, drafting
the reuse comparison, or execution verification. Supply one explicit request/claim
and its relevant evidence per check. Jev's answer is advisory, cannot establish
source authenticity or authorize action, and must not replace the user's choice or
real tests. Keep the ordinary workflow available without an API key; do not add a
model call to every step or stall authorized work on an unavailable optional check.

## Common Failure Modes

- Research theater: collecting links without changing a decision.
- Checklist cargo cult: forcing repo counts or dimensions onto irrelevant work.
- Search-first, context-later: importing patterns that conflict with the workspace.
- README trust: relying on marketing documentation without source/tests for behavior-critical claims.
- Version blindness: mixing current docs with older installed software.
- Confirmation bias: searching only for the initially preferred solution.
- Authorization stall: asking to proceed after the user already authorized execution.
- Novelty paralysis: refusing reversible progress because perfect external precedent does not exist.
- Silent uncertainty: presenting inference as fact.
- Re-researching: ignoring valid work already completed in the same goal.
- Dictation bias: treating any user wording as a complete implementation specification.
- Vocabulary mirroring: copying named tools or decompositions into the plan without proving they fit.
- Means fixation: researching only how to implement the proposed mechanism instead of whether it serves the purpose.
- Compression blindness: assuming the absence of a named requirement means the underlying need does not exist.
- Vocabulary ceiling: limiting research and solution quality to concepts the user already knows how to name.
- Interruption amnesia: forgetting the active goal when incorporating later guidance.
- Over-interpretation: ignoring an explicit hard constraint under the pretext of pursuing a broader purpose.
- Project-research umbrella: assuming one general research document justifies every later feature.
- Historical grandfathering: preserving inherited behavior because it exists or passes tests despite missing feature-specific evidence.
- Green-test substitution: using build/test success as proof that the chosen product behavior or security boundary is correct.
- Ledger theater: collecting links without recording the decision changed and the failure evidence required.
- Silent custom default: building from scratch without investigating and showing credible reusable alternatives.
- Invisible research: discovering useful libraries or patterns but withholding them until after implementation.
- Library shopping theater: naming packages without verifying task fit, compatibility, rights, or the work they actually replace.

The scenarios in [references/research-examples.md](references/research-examples.md) and [references/case-studies.md](references/case-studies.md) illustrate the workflow; they are not evidence for a current implementation.
