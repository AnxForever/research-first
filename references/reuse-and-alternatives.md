# Reuse and Alternatives

Use this guide when selecting an implementation, adding a material feature, or shaping a new interface or artifact. The outcome is an informed choice the user can see: reuse, adapt, combine, or build. Research should uncover useful options the user did not know to ask about.

## Research the Feature in Its Local Context

Start with the existing stack, dependency versions, design system, conventions, and explicit constraints. Define the user outcome and the behavior that needs evidence. Search by that behavior and by relevant technical terms; do not restrict discovery to the user's vocabulary or the first proposed library.

For each material feature, investigate the applicable sources:

| Source | What to learn |
|---|---|
| Comparable products and workflows | Expected behavior, interaction states, limitations, and unmet needs |
| Open-source projects, libraries, components, and examples | Reusable implementation, integration patterns, and failure handling |
| Official documentation, standards, papers, and technical explanations | Supported contracts, alternative techniques, and reasons behind design choices |

These sources answer different questions. A product demo does not establish implementation quality; an official API page does not show whether the workflow serves users. A whole-project comparison does not cover every material feature. Reuse valid prior research when it matches the feature and current versions, and research only changed or missing decisions. Mechanical edits do not require another survey.

When an underspecified request leaves a material user-flow choice open, inspect a
comparable product's relevant flow or an established artifact serving the same
purpose. Follow the actual user step, feedback, and recovery behavior in official
help, a demo, or an accessible interface. Keep documented behavior distinct from
behavior you personally exercised. Connect the useful finding to this project's
friction and cost before adopting, adapting, or rejecting it; similarity alone
does not prove local demand. If no suitable flow is accessible, label that gap
rather than substituting a package feature list or inventing an improvement.

Search for both direct reuse and better approaches: a smaller dependency, a platform capability, an established composition, or a documented technique may fit better than adopting a whole project. For documents and other non-code work, look for authoritative materials, reusable structures, and relevant exemplars instead of forcing a package search.

## Frontend Discovery

For material frontend behavior, actively look for resources that implement the relevant interaction. Depending on the feature, this may mean a component library, headless primitive, animation library, visualization package, editor, or design-system example. Check what the project already uses before adding another system.

Compare more than appearance. Inspect the applicable behavior: focus and keyboard support, semantic structure, loading/empty/error states, responsive behavior, reduced motion, cleanup, and performance. Verify that styling and composition can support the intended visual direction without fighting the library. A polished screenshot alone is insufficient evidence for selecting an interactive component.

Do not install a general component or animation library merely because the task involves frontend work. Find resources for the actual feature, and explain whether using them improves the result.

## Verify Serious Candidates

Inspect enough primary material to support the claims that would drive adoption. Apply these checks where relevant; do not turn them into a fixed quota:

- **Behavior:** read the relevant API documentation, examples, core source, and tests for behavior-critical claims. Distinguish observed behavior from documented promises and untested inference.
- **Compatibility:** check the target framework/runtime versions, rendering model, dependency and peer-dependency requirements, and integration with the existing stack.
- **Reuse rights:** inspect the license for the exact code, asset, or material being reused, including attribution or redistribution conditions. Public availability does not establish permission to copy.
- **Maintenance:** check relevant releases, issue handling, and support for the needed API. Age, stars, or a recent commit alone do not establish suitability.
- **Cost of adoption:** identify meaningful dependency weight, migration work, service costs, coupling, upgrade burden, or loss of control.
- **Frontend fit:** verify styling control, composability, accessibility claims, animation behavior, and relevant performance constraints against primary evidence or a focused experiment.

Record source links and the relevant version, revision, or date when behavior can drift. If a needed check is unavailable, mark it unverified and explain its effect on the recommendation. Never present a search result or remembered capability as a verified candidate.

Apply the same standard to rejection. First identify the premise that excludes a
credible option, then try to disprove that premise with primary documentation,
relevant source, or a small probe. An absent mention, search snippet, or assumed
maintenance cost cannot establish that a capability is unavailable. If unknown,
state the uncertainty and compare verified tradeoffs; a local preference does not
need an invented technical limitation. Keep this check on decision-changing claims,
not every incidental sentence or every result in a search.

## Prove Fit at the Integration Boundary

Follow the actual local entry point through wrappers to the candidate API and back
to application state or output. Identify which guarantees depend on local wiring:
for example, a dialog primitive may manage focus only when its trigger or callbacks
are connected; a table state API does not decide what survives a reload. Verify
the relevant connection in source and, when uncertain, a small isolated experiment.
Do not replace this check with the library's feature list or a screenshot.

Turn the important finding into a concrete acceptance check on the assembled
feature. Keep a short link: inspected fact -> local consequence -> executed check.
Research may confirm the original approach; do not manufacture a design change
to look productive. Review-only tasks may use permitted isolated probes but must
leave the reviewed artifact unchanged.

## Make the Choice Visible Before Implementation

Before substantial implementation, give a concise comparison of the recommendation and credible alternatives, including a custom implementation when it is a meaningful option. For each serious option, state what it provides, what must change locally, the important tradeoff, and the evidence behind those claims. Exclude weak candidates with a short reason when their rejection affects the decision; do not fill a table with unrelated names.

Keep independent choices separate. A table-state library can be combined with
lightweight CSS; a motion library is a separate decision. Do not offer a false
choice between "custom and simple" and "reuse with elaborate animation" when a
reusable, simple combination is viable. Compare the work actually saved and the
remaining local responsibilities, rather than assuming custom logic is cheap
because the dataset is small.

Use these decisions:

| Decision | Meaning |
|---|---|
| Reuse | Adopt an existing implementation or material with a suitable contract and acceptable integration cost |
| Adapt | Change a reusable implementation or apply an evidenced pattern to fit local constraints; check reuse rights when copying |
| Combine | Compose compatible resources and explain the responsibilities and integration boundary |
| Build | Implement locally because the verified alternatives do not fit, or because the user knowingly prefers the tradeoff |

Building is a valid result of research. Explain the specific mismatch or benefit that justifies it, what established patterns still inform the work, and what maintenance responsibility it creates. A limited or failed search supports "no suitable candidate verified in this search," not "no solution exists." Disclose the gap and use a reversible, authorized path when appropriate.

Give the user a real choice without inventing an approval gate:

- A feature implementation request normally authorizes routine, reversible choices within the existing stack and scope. Show the recommendation and evidence, then proceed without requiring a separate delegation phrase. Respect a request to present options or wait first; research-only work does not authorize implementation.
- If a choice changes the intended product, conflicts with an explicit constraint, adds a paid/external commitment, or creates a substantial migration or maintenance obligation outside the request, ask one concrete question with the recommendation and consequence. Continue independent work while awaiting the answer; defer only dependent action.
- If the user already selected an approach or delegated that material choice, proceed within that authority. Do not ask again for each package or implementation step.
- If the user prohibits new dependencies, respect that constraint. Still explain relevant reusable patterns and resources, and how they inform a compliant implementation; do not install a dependency or ask to override the constraint as a routine step.

An update such as "I found libraries and will use one" does not expose a meaningful choice. An update should let the user understand what they gain, what they take on, and why the recommendation fits their feature.

## Carry the Decision Into Delivery

For each material feature, preserve the evidence-to-decision link in the research notes or feature ledger. Record the selected reuse/adapt/combine/build approach, rejected alternatives that mattered, remaining unknowns, and verification needed for the local adaptation. Research is useful when it changes a choice, confirms a consequential constraint, or prevents an unsupported assumption.

Use [the research report template](../assets/research-report-template.md) when a written handoff is useful. Keep short work concise; omit inapplicable sections rather than manufacturing candidates, edge cases, or discoveries.
