# Research-First Examples

These are illustrative scenarios, not verified project histories or measured outcomes. Named products and libraries are discovery candidates, not endorsements or evidence of compatibility. The checks below must be performed against the actual project and current, version-matched sources before their results can be reported as facts.

## A Filterable, Sortable Table with Light Animation

**Request:** "Make this data page easier to explore, with filtering, sorting, and a little animation."

**Purpose:** Help people find and compare records while keeping interactions clear. Animation should explain changes without delaying work. The request names outcomes but leaves accessibility, data volume, query ownership, and loading states open.

**Start locally:** Inspect the framework, installed UI components, table utilities, styling conventions, existing motion dependency, data endpoint, and comparable pages. Determine whether filtering and sorting operate on all records or only a loaded page. Existing components may solve much of the work, but their presence alone does not establish adequate keyboard or screen-reader behavior.

**Actively discover candidates:** Search relevant product examples, maintained component demos, official documentation, and open-source implementations. Search separately for the table interaction and the animation: choosing a table library does not settle motion behavior.

| Candidate route | Evidence to inspect before choosing |
|---|---|
| Extend the project's existing table and controls | Actual filtering/sorting support, consistent state handling, accessible markup, and the cost of missing behavior |
| Combine existing visual components with a headless table candidate such as TanStack Table | Framework/version fit, relevant examples and source/tests, controlled state, server-side data behavior, and integration work |
| Adapt an integrated grid candidate such as AG Grid | Required features in the applicable edition, licensing, accessibility behavior, styling fit, bundle impact, and whether its complexity serves this page |
| Reuse the existing motion system, or evaluate Motion or GSAP | Framework support, licensing, cleanup, reduced-motion behavior, and whether the required transitions need another dependency |
| Use CSS transitions or the platform's Web Animations API | Whether simple effects suffice, interruption behavior, reduced-motion handling, and the project's browser requirements |

Do not add every candidate to the project. Narrow the shortlist using local constraints, inspect the promising options, and try a small reversible interaction when documentation cannot settle behavior. Record source versions and distinguish a working demo from proof that the integration fits this app.

**Show the choice before substantial implementation.** After checking the evidence, a concise update could follow this pattern:

> The goal is to make records easier to find and compare. I checked the existing components, a headless table option, an integrated grid, and lightweight motion options. [Evidence] supports [recommended combination]. [Alternative] would help if [relevant additional need], but adds [verified cost or constraint]. I will use [choice], keep [important local convention], and verify filtering, sorting, keyboard use, and reduced motion.

Replace brackets with actual findings. If the user has authorized implementation,
the recommendation fits that scope, and no material undelegated choice remains,
continue; the update does not require repeated approval. If a material visual or
dependency tradeoff still needs the user's choice, ask about it before dependent
work. It is valid to reject all new dependencies, but tell the user which useful
options were considered and why the chosen route fits.

**Deliver and verify:** Exercise filter/sort combinations, empty and loading states, data errors, and query persistence if the workflow requires it. Verify that server-side operations do not misleadingly affect only the visible page. Check focus, keyboard interaction, reduced motion, and interrupted transitions. Completion requires usable record exploration and appropriate motion; a screenshot or dependency installation alone is insufficient.

## Background Scheduling: Reuse Without Importing an Architecture Blindly

**Request:** "Add recurring background jobs to this service."

**Purpose:** Run work at the intended times, preserve the promised behavior across restarts, and make failures understandable. First establish the deployment model, timing requirements, persistence owner, and whether execution may overlap. Do not assume that scheduling automatically requires a distributed queue.

**Discover alternatives:** Inspect any existing scheduler or queue integration, then research a maintained scheduler library, the scheduling facilities of a queue already used by the project, and a platform scheduling service if the deployment makes it relevant. For a Python service, APScheduler can be a search candidate; its name does not settle the version, API, persistence model, or worker coordination contract.

**Validate the shortlist:** Use the exact installed or proposed version's official documentation, relevant source/tests, and independent integration examples. Check startup/shutdown, persistence, missed runs, timezone rules, cancellation, retries, and execution ownership. For a serious architecture or code-reuse choice, compare independent implementations rather than copying a tutorial. Check licenses before copying code. Never combine examples from different major versions or infer durable storage from a library's presence.

**Present the options:** Explain which route fits the current deployment, what it reuses, and what it leaves to the application. A brief comparison might distinguish an in-process scheduler, an existing queue's scheduling path, and an external scheduling service by their verified recovery behavior, operational requirements, and integration cost. Recommend one and proceed within existing authorization. Ask only if a remaining choice changes a material requirement, cost, or authority boundary.

**Deliver and verify:** Trace the chosen mechanism from persisted schedule through dispatch and execution to completion or failure. Exercise restart, overdue work, repeated dispatch, execution failure, cancellation, and shutdown where relevant. Use failure evidence to determine whether the promised delivery semantics hold; do not claim "exactly once" or durable recovery without support.

## A Small Edit Does Not Need a Selection Exercise

**Request:** "Change this button label from Save to Publish; keep its behavior."

**Purpose and constraint:** Change the specified copy while preserving the action.

**Evidence and action:** Locate the label and its context, check whether localization affects the change, edit the applicable text, and inspect the diff and rendered label as appropriate. There is no material unresolved component or architecture choice, so no external search, candidate matrix, feature ledger, or implementation approval is needed.

Research-first means resolving the uncertainty that matters. It does not turn every small edit into procurement or redesign.
