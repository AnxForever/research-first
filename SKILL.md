---
name: research-first
description: Interpret the user's underlying purpose, expand compressed or incomplete requests, and research evidence before choosing a solution. Always use, in any language, when the user asks to research, investigate, gather sources or examples, inspect evidence, understand their intent, avoid literal copying, or expand an idea. Also always use when the user questions, doubts, challenges, corrects, is dissatisfied with, or asks to reconsider the agent's understanding, plan, decision, or work; reassess intent, assumptions, and contrary evidence instead of merely defending or agreeing. Use for ideas, symptoms, named technologies, proposed implementations, product directions, architecture, integrations, migrations, security, privacy, payments, and other consequential work where evidence could change the framing or solution. Skip only fully specified, low-risk mechanical actions where research cannot materially change the result. Resume valid research instead of restarting it.
---

# Research First

Build from evidence, not habit. Research is any disciplined reduction of uncertainty: inspecting the workspace, reading official docs and source, analyzing user-provided material or telemetry, comparing established examples, or running a safe experiment.

## Operating Contract

1. Treat every user request, idea, and suggestion as compressed evidence of intent, not automatically as a complete specification.
2. Establish what is already known before searching.
3. Match research depth to risk, novelty, reversibility, ambiguity, and user urgency.
4. Use the evidence types that fit the task; do not force every task into GitHub research.
5. Prefer primary evidence and independently corroborate material claims.
6. Convert findings into an expanded problem definition, decisions, implementation constraints, and tests.
7. If the user already authorized execution, continue after a concise research update. Ask before implementation only when authority or a material product choice is missing.
8. Preserve an evidence trail sufficient to explain important decisions without flooding the user.

## Step 0: Resume Before Restarting

First inspect the conversation, active plan/goal, existing research notes, recent commits, and current workspace state.

- Reuse research that is recent, source-grounded, and still relevant.
- Verify only assumptions affected by new code, changed requirements, version drift, or external state.
- Do not repeat completed searches merely to satisfy a checklist.
- When inheriting a task, record what is established, uncertain, and stale.

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

Literal execution is appropriate only when the user clearly specifies a hard constraint, exact artifact, or
deliberately chosen method. Even then, research how to implement it correctly in context. If literal wording
conflicts with the larger purpose, surface the conflict and pursue the purpose unless the user explicitly confirms
that the method itself is the requirement.

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
| Quick | Familiar, reversible task with one meaningful unknown | 1 strong evidence stream; 2-3 relevant dimensions |
| Standard | New feature, design, plan, integration, or customer-facing change | 2 independent evidence streams; at least 6 relevant dimensions; 5 edge cases |
| Deep | Security, auth, money, privacy, destructive operations, core architecture, migration, regulated work | 3+ evidence streams; 8-10 dimensions; adversarial and rollback analysis |

Escalate depth when evidence conflicts, the domain is unfamiliar, the action is hard to reverse, or the user previously found the work shallow. Reduce breadth—not validation integrity—when time is constrained.

Read [references/adapting-depth.md](references/adapting-depth.md) when depth is ambiguous or constraints are severe.

## Step 3: Expand the Real Question

Select the dimensions that can materially affect the outcome. Standard work should cover at least six; Deep work should normally cover all applicable dimensions.

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

Examples of valid Standard combinations:

- Existing feature: local implementation/tests + official API docs.
- Product workflow: user feedback/analytics + two strong product examples.
- Migration: current schema/data sample + vendor migration guide + dry run.
- Document revision: supplied draft/source material + applicable style guide or exemplar.
- Incident diagnosis: logs/traces + source/history + reproduction experiment.

Repository quotas are not universal. When external code reuse or architecture is central, inspect at least two independent implementations; for each serious reuse candidate, read core source and tests rather than only its README.

Read [references/search-quality.md](references/search-quality.md) before broad external research.

## Step 5: Gather Evidence Efficiently

### Local-first tasks

Start with the workspace. Search narrowly, follow data/control flow, inspect nearby tests, and check recent changes. Search externally only for unresolved behavior, unfamiliar APIs, security guidance, standards, or prior art that can change the design.

### External research

Prioritize:

1. Official documentation and specifications
2. Primary source code, tests, datasets, or product behavior
3. Maintainer issues, release notes, and security advisories
4. High-quality independent analysis
5. Blogs and forum answers only as leads to verify

Pin versions, dates, commits, or document revisions when behavior can drift. Check license before copying code or assets.

### Creative and design work

Study relevant exemplars, templates, style guides, and reusable assets. Extract structure, interaction, visual language, states, accessibility, and the reason the example works. Do not add design research to a backend-only change unless it affects a user-facing contract.

### Operational actions

For deployments, migrations, account changes, or external writes, research the exact target version and environment. Prefer read-only inspection and dry runs. Identify rollback, blast radius, credential scope, and success signals before mutating state.

### Restricted or offline environments

Use available local docs, vendored source, lockfiles, installed package metadata, tests, fixtures, and experiments. If primary evidence is unavailable:

- state the evidence gap;
- distinguish fact, inference, and assumption;
- proceed with a reversible best-effort path when the user has authorized it;
- ask only if the missing evidence creates a material, irreversible choice.

## Step 6: Synthesize, Do Not Accumulate

For each important finding, capture:

```text
Question → Evidence → Confidence → Decision/constraint → Verification
```

Compare evidence across these concerns when applicable:

- contract/data model
- lifecycle and failure handling
- security boundary
- configuration and deployment
- performance/cost
- API/UX
- test strategy
- compatibility/evolution

Resolve conflicts by preferring evidence that is primary, version-matched, reproducible, maintained, and closest to the actual environment. Document consequential conflicts and why one source won.

Classify reuse decisions:

- REUSE: compatible, licensed, maintained, and fits directly.
- ADAPT: sound pattern but local constraints require changes.
- LEARN-FROM: useful principle, incompatible implementation or license.
- REJECT: evidence shows it does not fit.

## Step 7: Readiness Gate

Before creating or changing anything substantial, confirm:

- [ ] Context and desired outcome are understood.
- [ ] Research depth matches risk and novelty.
- [ ] Material unknowns were expanded across relevant dimensions.
- [ ] Primary evidence was used where available.
- [ ] Material claims have independent support or are labeled uncertain.
- [ ] At least five edge cases exist for Standard/Deep work.
- [ ] Security and failure/rollback were considered when relevant.
- [ ] Reuse/license/version decisions are explicit when relevant.
- [ ] Findings map to implementation constraints and verification.
- [ ] The proposed action fits the user's authority and scope.
- [ ] User input was separated into purpose, constraints, candidate means, assumptions, and missing dimensions.
- [ ] The plan optimizes for the inferred outcome rather than mirroring the latest wording.

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
- Execution plan: [ordered slices and verification]
```

Then:

- If execution is already authorized, continue immediately.
- If the user asked only for analysis/review, stop at findings.
- If a missing choice materially changes scope, cost, risk, or external state, ask that question.
- If research disproves the requested approach, explain the evidence and propose the closest viable alternative.

## Step 9: Verify and Self-Audit

After execution, test in proportion to risk and revisit the evidence-to-decision chain.

- Confirm the implementation addresses the researched edge cases.
- Run relevant tests, builds, lint/type checks, dry runs, or artifact inspection.
- Check for new TODOs, stubs, unsupported claims, or stale docs.
- Report known residual risks and unverified external assumptions.
- Do not claim completion because research or coding is extensive; claim it only when the requested outcome is achieved.
- Compare the result against both failure directions: literal under-interpretation and speculative over-interpretation.
- Confirm every added requirement traces to user purpose plus evidence, and every explicit constraint remains intact.

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
