# Handling Contradictory References

When two good references recommend different approaches, don't guess.
Use this framework.

## Resolution Priority

Rank references by these criteria (in order):

1. **Stack match** — Same language/framework as your project? (most important)
2. **Maintenance** — More recently updated? Active community?
3. **Test coverage** — Better test suite? Tests cover edge cases?
4. **Production evidence** — Known production users? Case studies?
5. **Conceptual clarity** — Code easier to understand and adapt?
6. **Performance characteristics** — Better fit for your use case's scale?

## Resolution Process

```
Reference A says X. Reference B says Y.

1. IDENTIFY the exact point of disagreement
   "A uses write-through cache, B uses cache-aside"

2. CHECK if they're solving different problems
   "A is optimizing for consistency, B for read performance"
   → If yes: choose based on YOUR requirements, not "which is better"

3. CHECK if one is older (superseded by the other)
   "A is from 2022, B is from 2025 and references A's limitations"
   → If yes: prefer the newer one, but verify it actually improves things

4. CHECK the tests for edge case behavior
   "A's tests show it handles cache failure gracefully, B's tests don't cover this"
   → Bias toward the reference with better edge case coverage

5. If still tied: run a spike implementation of both
   "Implement the simplest version of each, test with your data"
```

## Document the Conflict

In Phase 6 report, always note the disagreement:

```
### Conflicts Resolved
A uses [pattern X], B uses [pattern Y].
Chose A because: [stack match + better test coverage].
B's approach is better for: [scenario]. We may adopt it later if [condition].
```

## When Both Might Be Wrong

If two references agree on an approach that feels wrong for your project:

1. Trust your Phase 0 knowledge — you understand the project's constraints
2. Search specifically for `"{approach} problems"` or `"{approach} limitations"`
3. Look for a third reference that takes a different approach entirely
4. If only two approaches exist and both feel wrong, the problem might need reframing

## When You Can't Decide

Ask the user:
```
Two strong references disagree on [specific point]:

A ([name]): [approach] — better for [reason]
B ([name]): [approach] — better for [reason]

Given our project's constraint of [key constraint], which direction?
```
