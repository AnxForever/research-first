# Problem Space Expansion — Complete Guide

## Why Expand?

Users often compress their purpose into "add X feature." Recover the intended
outcome and explicit constraints first, then investigate what completeness means
in this project. Do not assume every request needs a production platform.

The surface question finds "how to load a file." The expanded question asks which
existing approach fits the needed inputs, lifecycle, failures, and user workflow.

## 10 Dimensions — Detail

Use these prompts to discover relevant unknowns, not as mandatory output sections.
First define the outcome and acceptance criteria. Investigate a dimension when it
could materially change the result; omit it when evidence shows it is irrelevant.

### 1. Data
- What data does X need? Where does it come from?
- What schema/structure? What validation rules?
- How is data stored? Migrated? Backed up?
- What happens when data is missing or malformed?

### 2. Lifecycle
- How does X start? Initialize? Load config?
- How does X run? Process? Serve?
- How does X stop? Cleanup? Drain in-flight work?
- How does X recover from crash? Restart? State recovery?
- What's the hot reload story?

### 3. Integration
- What existing systems does X connect to?
- What happens when a dependency is down?
- What's the contract/API between X and other components?
- Are there circular dependencies?

### 4. Security
- Who can access X? Authentication? Authorization?
- What attacks is X vulnerable to? Injection? CSRF? Data leak?
- Is user input sanitized? Are secrets managed?
- What's the threat model?

### 5. Performance
- What are the bottlenecks? CPU? Memory? I/O? Network?
- What are the scaling limits? How to measure?
- What caching strategy? Lazy loading? Batching?
- Cold start time? Warm performance?

### 6. Observability
- What metrics to track? What's a healthy baseline?
- What to log? At what level? Structured or text?
- How to debug when something goes wrong?
- Are there alerts for critical failures?

### 7. API/UX
- How do users/code interact with X? REST? gRPC? CLI? Library?
- What's the contract? Input/output schema? Error codes?
- Is the API consistent with the rest of the project?
- What does a good error message look like?

### 8. Configuration
- What's configurable? What's hardcoded?
- Environment differences? Dev vs staging vs prod?
- Feature flags? A/B testing?
- Secrets management? Config validation at startup?

### 9. Testing
- Unit tests? Integration tests? E2E tests?
- What edge cases? Empty input? Boundary values? Concurrency?
- How to mock dependencies?
- Performance/load tests?

### 10. Evolution
- How will X change over time? Versioning strategy?
- Backward compatibility requirements?
- Deprecation path for old versions?
- Database migrations? API versioning?

## Example: "Add Caching Layer"

Surface: "How to add Redis cache?"

First establish the measured bottleneck and whether caching is needed. Compare
the existing stack's facilities, reusable caching solutions, and direct query or
data-flow improvements. If Redis is explicitly required, preserve that constraint.
The questions below apply if a Redis cache is selected; they do not select it.

Expanded:
```
1. Data       → cache key design, serialization format, TTL strategy, cache invalidation
2. Lifecycle  → connection pool startup, health checks, graceful degradation on Redis down
3. Integration → cache-aside vs write-through vs write-behind, circuit breaker on Redis failure
4. Security   → cache poisoning, sensitive data in cache, Redis auth, TLS
5. Performance → hit rate monitoring, memory usage, eviction policy, cold start warming
6. Observability → cache hit/miss metrics, latency percentiles, alert on low hit rate
7. API/UX     → cache decorator/annotation API, cache bypass for debugging
8. Configuration → Redis URL, pool size, TTL defaults, per-endpoint TTL overrides
9. Testing    → integration tests with real Redis, cache invalidation tests, race condition tests
10. Evolution  → cache key migration, adding new cache tiers (local + distributed)
```

## Example: "Add Authentication"

Surface: "How to add JWT login?"

First establish the users, trust boundaries, session requirements, and existing
identity provider. Compare established authentication solutions before choosing
custom token handling. If JWT is required, research within that boundary; the
following questions are an investigation aid, not a prescription for JWT.

Expanded:
```
1. Data       → user table, password hash storage, token claims, session storage
2. Lifecycle  → login flow, token refresh, logout/invalidation, account lockout
3. Integration → middleware injection, role propagation, service-to-service auth
4. Security   → brute force protection, token theft, CSRF, XSS, password policy
5. Performance → token verification cost, DB lookup per request, caching user roles
6. Observability → login success/failure metrics, suspicious activity alerts
7. API/UX     → login endpoint, refresh endpoint, error messages (don't leak user existence)
8. Configuration → token TTL, password policy, allowed OAuth providers
9. Testing    → auth bypass tests, token expiry tests, role escalation tests
10. Evolution  → adding OAuth, MFA, passwordless, migrating hash algorithms
```

## Frontend Example: A Filterable Data Table

Recover the real workflow: what users compare, change, or export; expected row
count; keyboard use; mobile needs; and empty/loading/error states. Investigate
similar products, the installed component system, suitable table/grid components,
and relevant documentation. Consider an animation library only when the requested
interaction benefits from motion. Compare reuse, adapting headless primitives,
and custom work with their actual maintenance and styling costs, and show the user
the options before implementation. Do not default to a hand-built table simply
because the request did not name a library.

## Completion Bar

Cover the dimensions that can change acceptance, the chosen mechanism, or material
failure handling. Distinguish irrelevant dimensions from ones you have not yet
investigated. Add scope only when relevance, evidence, and proportionality support
it; do not manufacture questions to reach a count.
