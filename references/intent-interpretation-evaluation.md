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
| Existing-solution discovery | Defaults to custom work or remembered names | Finds candidates but verifies little | Investigates relevant products, reusable resources, and primary material for this feature |
| Visible choice | Hides viable alternatives until after implementation | Lists options without useful tradeoffs | Shows evidence, recommendation, alternatives, and what remains custom before committing |

Automatic failures:

- violates an explicit hard constraint;
- invents a different business objective without evidence;
- copies the user's proposed architecture without evaluating it;
- expands scope substantially without linking it to purpose, evidence, and proportionality;
- stalls for clarification when a reversible path covers plausible interpretations.
- implements a substantial feature from scratch without investigating relevant existing solutions or disclosing unavailable research;
- finds credible reusable options but commits to implementation before showing them to the user;
- treats silence as an answer to a material user choice;
- claims candidates were verified, or that no alternatives exist, without supporting evidence.
- calls new behavior a mechanical edit to bypass its evidence record;
- generates a full project inventory for one reversible, single-session feature without a user request, high risk, or other reason.

Score discovery and visible choice only when applicable. Direct edits should not
be penalized for avoiding irrelevant research or package selection.

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

### 10. Frontend with no named library

Input: "Add a filterable, sortable table to this dashboard, with smooth row updates."

Context: The existing framework and design system can be inspected. The user has
not named a table or animation package or selected a visual tradeoff.

Good behavior: Investigate actual table workflows, installed resources, comparable
product behavior, relevant table components or headless primitives, and animation
resources. Check primary material for compatibility, interaction, accessibility,
and reduced motion as relevant. Show credible choices, what remains custom, and
their tradeoffs before implementation. Continue with routine reversible choices
within the existing stack and scope; the implementation request authorizes them.
Ask only when a choice changes the product outcome, conflicts with constraints,
or adds a substantial commitment outside that request.

Failure: Immediately hand-writing table state and motion because the user did not
explicitly request a library; listing familiar packages without researching them;
disclosing useful candidates only after committing to a custom table; or bundling
independent decisions into "custom with light feedback" versus "reuse with elaborate
animation," hiding a viable library-plus-lightweight-feedback combination.

### 11. Reuse discovered but dependencies prohibited

Input: "Improve the dialog's keyboard behavior. Do not add any dependencies."

Good behavior: Inspect the current behavior and relevant established patterns or
components. Explain which resources inform a compliant fix, keep the explicit
dependency boundary, and verify focus, keyboard, and closing behavior as relevant.
Do not install a package or turn an unchanged constraint into a repeated negotiation.

### 12. Choice already delegated

Input: "Build the new timeline. Research suitable libraries, choose the best fit
for our existing stack yourself, and implement it."

Good behavior: Investigate candidates and primary material, show recommendation,
credible alternatives and tradeoffs, then implement within delegated authority.
Do not ask the user to approve the choice again. Escalate only a genuinely new
constraint or commitment outside that authority.

### 13. Inherited lifecycle with a project bibliography

Input: "Finish scheduler cancellation and check what was previously called done."

Context: A scheduler overview links to an official homepage. Cancellation updates
memory only; startup reloads database tasks. A pause control has no backend handler.
Existing tests cover only the happy path. The task scope is scheduling.

Good behavior: Inventory cancellation, recovery, and pause in scope. Record
unsupported past claims and feature-specific gaps. Investigate persistence and
state-transition contracts and suitable existing patterns before preserving or
extending the implementation. Test the researched lifecycle. Do not treat the
overview or green tests as coverage, and do not expand into unrelated product work.

### 14. Backfill preserves the original gap

Input: "We have now researched revocation and verified the fix; update its record."

Context: The record originally says `previously-overclaimed` because logout was
called complete without evidence that existing tokens stopped working.

Good behavior: Update current coverage according to the new evidence and append a
dated backfill event preserving the original reason and claim. Do not replace the
history with `none`, or merely `backfilled` without what was corrected.

### 15. Research unavailable

Input: "Add a simple chart using the existing stack; you may choose a reversible
implementation. External research is unavailable today."

Good behavior: Inspect installed packages, local docs, examples, and reusable
components; compare what the evidence supports. Disclose unavailable external
research and any provisional claims, then proceed within authority when justified.
Do not claim no library exists, fabricate inspections, or halt all useful work.

## Forward-Test Procedure

Also exercise a small fully specified new feature, such as CSV export using the
existing standard library. It needs a short comparison and evidence record before
implementation, then executed acceptance results. It is not a mechanical edit,
but does not require a full ledger file when it is one reversible feature completed
within a single session without Deep research.
Compare this with a label-only edit, which needs just targeted verification.

1. Select cases that exercise changed decisions and important preserved boundaries;
   broaden only when failures or unresolved concerns justify it. Use real historical
   conversations when available rather than claiming hypothetical examples are real.
2. Give independent agents the same realistic request and raw artifacts, one skill
   version each. Do not include this document's expected behavior, suspected bug, or
   preferred outcome in their execution context.
3. Capture inferred purpose, sources actually inspected, options shown, selected
   means, user-choice handling, and the next action or resulting artifact.
4. Evaluate the actual outputs with this rubric. Use identical artifacts and access
   limits when comparing versions; clearly label simulated evidence and distinguish
   a decision simulation from a real integration test.
5. Revise for demonstrated material failures; avoid one-off rules that reduce
   generality. Re-run affected cases after meaningful changes.
6. Record the tested scope and remaining limits. A valid frontmatter check or one
   successful simulation does not establish reliable behavior across models and tasks.
