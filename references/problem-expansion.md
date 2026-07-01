# Problem Space Expansion — Complete Guide

## Why Expand?

Users ask "add X feature." They mean "add X, correctly, securely, efficiently,
maintainably, in a way that fits the project, handles edge cases, and won't
need rewriting next month."

The surface question finds "how to load a file." The expanded question finds
the complete architecture that production systems converged on.

## 10 Dimensions — Detail

For any feature X, ask ALL of these:

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

## Minimum Bar

Expand at least 6/10 dimensions. If you can't think of what to ask for a dimension,
that dimension is probably an unknown risk — search it anyway.
