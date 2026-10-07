# Handling Contradictory References

When two good references recommend different approaches, don't guess.
Use this framework.

## Resolution Priority

Resolve the exact claim using:

1. **Authority** — Which source defines the required contract or reports direct observations?
2. **Applicability** — Does it match the target version, environment, user, and requirement?
3. **Reproducibility** — Can source, tests, data, or an experiment demonstrate the claim?
4. **Independence and currency** — Is corroboration independent and still applicable?

Then compare fit, maintenance, integration effort, and performance when choosing
between valid options. Same-language code and newer publication dates alone do not
override an applicable specification or reproduced failure. If runtime behavior
violates its specification, record both the required contract and observed defect.

## Resolution Process

```
Reference A says X. Reference B says Y.

1. IDENTIFY the exact point of disagreement
   "A uses write-through cache, B uses cache-aside"

2. CHECK if they're solving different problems
   "A is optimizing for consistency, B for read performance"
   → If yes: choose based on YOUR requirements, not "which is better"

3. CHECK version applicability and whether one actually supersedes the other
   "B documents a changed contract in the target version"
   → Prefer the applicable contract, not simply the newer page

4. CHECK the tests for edge case behavior
   "A's tests show it handles cache failure gracefully, B's tests don't cover this"
   → Bias toward the reference with better edge case coverage

5. If still tied: run a spike implementation of both
   "Implement the simplest version of each, test with your data"
```

## Document the Conflict

In the decision update, note consequential disagreements:

```
### Conflicts Resolved
A uses [pattern X], B uses [pattern Y].
Chose A because: [applicable contract + reproduced behavior + local fit].
B's approach is better for: [scenario]. We may adopt it later if [condition].
```

## When Both Might Be Wrong

If two references agree on an approach that feels wrong for your project:

1. Recheck evidence for the project's constraints; do not elevate intuition above evidence
2. Search specifically for `"{approach} problems"` or `"{approach} limitations"`
3. Look for a third reference that takes a different approach entirely
4. If only two approaches exist and both feel wrong, the problem might need reframing

## When You Can't Decide

If a material user preference or constraint is missing, recommend an option and
ask about that tradeoff before dependent work. Continue independent investigation.
Do not ask the user to adjudicate a technical fact that a bounded experiment can
resolve. If the user already delegated selection and the choice is reversible,
explain the evidence and proceed.

Example of an unresolved user tradeoff:
```
Two strong references disagree on [specific point]:

A ([name]): [approach] — better for [reason]
B ([name]): [approach] — better for [reason]

Given our project's constraint of [key constraint], which direction?
```
