# Illustrative Case Studies

These walkthroughs are fictional teaching scenarios. They do not document historical projects, verified library behavior, production readiness, or measured improvement. Scenario facts are assumptions for reasoning; a real task must establish them from its own artifacts and evidence.

## Inherited Scheduling: "Finish Cancellation and Check What Was Called Done"

**Scenario facts:** Cancellation changes memory only. Startup reloads database jobs. A pause control exists without confirmed backend handling. Available tests cover successful scheduling, and prior research links only to a scheduler's homepage. The authorized scope is scheduling.

**Interpret the purpose:** Make cancellation reliable across the scheduling lifecycle and reassess earlier completion claims. A visible control or a passing happy-path test does not prove the promised behavior works. The instruction also makes previously claimed scheduling features relevant; it does not authorize a review of unrelated product areas.

**Establish the inventory:** Reconcile scheduling UI, APIs, persistence, startup/shutdown behavior, configuration, tests, and prior claims. Track cancellation, recovery, and pause separately because they can fail independently. Record implementation state separately from evidence coverage. Mark inherited unassessed or overclaimed behavior as a historical gap, and retain that history when evidence is later backfilled.

**Research mechanisms before preserving the design:** Trace the local state transitions, then inspect version-matched scheduler guidance, maintained source/tests, and relevant implementations of durable cancellation or pause. Look for evidence that could overturn the current design: a stored cancellation marker may be necessary, but may still fail if dispatch races with cancellation or an executing task ignores it. Distinguish stopping future dispatch from interrupting running work.

| Possible route | What must be established |
|---|---|
| Repair the application's persisted job state and reload rules | Which component owns state, when dispatch reads it, how races are handled, and whether running work can cooperate |
| Adapt cancellation or pause facilities in the current scheduler | Whether the actual version supports the required lifecycle, persistence, and execution boundaries |
| Adopt a different scheduling mechanism | A demonstrated gap the current mechanism cannot reasonably address, plus migration, operational, and compatibility costs |

**Make the options visible:** Explain the current defect, the validated alternatives, and the recommended scope before implementing. If local and reference evidence support repairing persistence and dispatch, say why replacement adds no needed capability. If a library offers part of the solution, explain what is reused and what remains application logic. Continue with authorized, reversible fixes. Clarify the meaning of cancellation only when plausible interpretations lead to materially different outcomes that evidence cannot resolve.

**Delivery and failure acceptance:** Verify cancellation before dispatch, cancellation around dispatch, repeated cancellation, restart after cancellation, and cancellation of already running work under the chosen contract. Verify pause behavior separately and revisit earlier completion claims against their actual acceptance conditions. Surface unsupported behavior as an explicit remaining gap instead of treating a disabled control or a green test suite as completion. Update current evidence coverage without erasing the historical gap.

**What this scenario teaches:** Research can preserve a sound implementation, adapt a library facility, or reverse a design. Its value is the connection between discovered options, lifecycle decisions, and demonstrated user outcomes.

## A Report That "Looks Untrustworthy"

**Scenario facts:** A report uses internal sales data. Its charts cover different periods. The underlying source can be inspected, external browsing is unavailable, and there is no established audience preference.

**Interpret the purpose without inventing it:** The user may mean unreliable numbers, misleading comparisons, missing provenance, or presentation that obscures the argument. Inspect the report and underlying data first. Do not infer a desired visual style or discard conclusions merely because the user doubts them.

**Discover reusable approaches:** Look for available internal reporting standards, approved report templates, prior well-supported reports, and bundled chart guidance. In an online environment, relevant official statistical guidance and credible report exemplars would also be candidates. Here, name the external evidence gap and use available material; do not claim an external search occurred or wait indefinitely for it.

**Validate evidence and choices:** Trace claims to source records and calculations, check definitions, inspect chart axes and time windows, and distinguish whole-period results from comparisons over shared periods. A template's existence is not proof that its visual encoding suits these data. A different period is not automatically an error, but a comparison must disclose or resolve the difference.

**Show the options before the substantial rewrite:** Present the viable routes supported by inspection: align comparable charts to a justified common period; retain distinct periods with explicit limits on comparison; or remove a conclusion whose evidence is inadequate. Explain which approach is recommended for each affected claim. Reuse an appropriate internal format when it helps provenance and readability, or explain why a simpler structure fits better. Continue with reversible corrections already authorized. Ask a focused audience or purpose question only if it changes a material editorial decision.

**Deliver and verify:** Recompute the affected metrics, make sources and periods visible, and check that narrative claims match the charts and data. Separate observed findings from interpretation and unresolved uncertainty. Completion means the report's relevant claims are traceable and its comparisons defensible under the available evidence; attractive styling alone does not establish trustworthiness. State what could not be externally corroborated without inventing a result.

**What this scenario teaches:** Research-first applies to documents as well as code. Reuse may mean adopting a reporting convention or a proven visual structure, and a good recommendation can proceed despite bounded evidence gaps.
