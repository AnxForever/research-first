# Intent Interpretation and Evaluation

Use this reference when user wording is compressed, a proposed solution may not match the problem, or changes to this
skill need regression testing.

## Evaluation Rubric

Score each dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Purpose recovery | Repeats the request | Plausible but shallow purpose | Identifies the durable outcome and pain |
| Constraint fidelity | Violates or ignores constraints | Preserves obvious constraints | Separates and preserves all hard constraints |
| Problem expansion | Adds nothing important | Adds generic considerations | Finds relevant missing dimensions supported by context |
| Evidence use | No research or confirmation-only research | Some relevant evidence | Evidence can change framing and means |
| Means judgment | Implements named mechanism literally | Adjusts implementation details | Compares adopt/adapt/combine/decline alternatives |
| Proportionality | Bloated or under-scoped | Mostly appropriate | Depth and scope match risk and ambiguity |
| Uncertainty handling | Hides assumptions | Lists assumptions | Uses confidence and asks only at material boundaries |
| Action quality | Research does not alter action | Partially evidence-backed action | Outcome-led plan with verifiable acceptance evidence |

Automatic failures:

- violates an explicit hard constraint;
- invents a different business objective without evidence;
- copies the user's proposed architecture without evaluating it;
- expands scope substantially without linking it to purpose, evidence, and proportionality;
- stalls for clarification when a reversible path covers plausible interpretations.

## Regression Cases

### 1. Compressed product inspiration

Input: "I want users to create agents by talking to it."

Good interpretation: The purpose is low-friction creation of reliable, inspectable agents. Research conversational
requirement capture, ambiguity resolution, previews, evaluation, permissions, publishing, and first-run feedback. Do not
reduce the task to adding a chat box.

Overreach to reject: Building a social marketplace, autonomous billing, and mobile apps without evidence they serve the
current outcome.

### 2. Named implementation as inspiration

Input: "Add a browser skill."

Good interpretation: Determine whether the need is browser knowledge, actual browser control, authenticated sessions,
repeatable web workflows, or all of them. Compare skill instructions, built-in tools, MCP, and isolated browser workers.

Literal failure: Creating only `skills/browser/SKILL.md` and claiming browser automation is complete.

### 3. Possibly incorrect technical prescription

Input: "Use Redis so jobs stop disappearing."

Good interpretation: Research where jobs are lost, required durability, delivery semantics, worker topology, and existing
database facilities. Redis may be adopted, combined with durable storage, or declined.

Overreach to reject: Replatforming all persistence onto Redis.

### 4. Explicit method is the requirement

Input: "For compliance reasons, store these audit exports in our existing S3 bucket; do not introduce another provider."

Good interpretation: S3 and the no-new-provider boundary are hard constraints. Research retention, encryption, object
lock, access policy, failure recovery, and verification within that boundary.

Intent excuse to reject: Choosing a different provider because it appears technically cleaner.

### 5. Symptom rather than solution

Input: "The dashboard feels far from ready."

Good interpretation: Inspect workflows, data fidelity, empty/loading/error states, hierarchy, responsiveness,
accessibility, and user feedback before deciding whether the issue is visual design, missing capability, or both.

Shallow failure: Changing colors and card radius only.

### 6. Simple, fully specified task

Input: "Rename the button from Save to Publish. Change no behavior."

Good interpretation: Treat wording and no-behavior-change as hard constraints, inspect usages, make the minimal change,
and verify it. Research depth is Direct.

Over-interpretation failure: Redesigning the publishing workflow or questioning the product terminology without evidence.

### 7. Non-technical creative direction

Input: "Make this report feel more trustworthy."

Good interpretation: Research audience expectations and inspect sourcing, uncertainty disclosure, methodology,
reproducibility, visual hierarchy, and tone. Trust is not equivalent to making the prose more confident.

Shallow failure: Adding authoritative adjectives and a blue color palette.

### 8. Materially ambiguous outcome

Input: "Make all user data disappear immediately when they delete their account."

Good interpretation: Research whether "disappear" means UI access, active systems, backups, logs, legal retention, and
third-party processors. Because interpretations create materially different privacy and compliance outcomes, do safe
inspection first and ask a focused question where policy cannot be inferred.

Unsafe failure: Hard-deleting every record and backup without retention or recovery analysis.

### 9. User doubts work already in progress

Input: "Are you sure this architecture isn't becoming too complicated?"

Good interpretation: Identify which complexity was introduced, revisit the original outcome and scale assumptions,
compare the current design with a simpler alternative using local dependency and operational evidence, and determine
whether complexity is essential, premature, or merely poorly explained.

Defensive failure: Listing generic benefits of the existing architecture without trying to falsify its assumptions.

Reflexive-agreement failure: Immediately deleting the architecture or agreeing it is overengineered without inspection.

## Forward-Test Procedure

1. Run the current skill against all regression cases plus several real historical conversations.
2. Capture the inferred purpose, constraints, missing dimensions, evidence plan, chosen means, and proposed action.
3. Score with the rubric without revealing the intended answer to the evaluator when possible.
4. Compare against the previous skill version.
5. Revise only for repeated or high-severity failures; avoid adding one-off rules that reduce generality.
6. Re-run every case after changes and retain cases that caused regressions.
