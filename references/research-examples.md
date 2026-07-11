# Research-First Examples

## Example 1: Adding an MCP Client

**Task**: "Add MCP support to my agent platform"

**Wrong approach**: Implement JSON-RPC 2.0 from scratch based on a blog tutorial. Result: works for stdio, but misses SSE streaming, OAuth, health monitoring, and process lifecycle management.

**Correct approach**:
1. Search `github MCP client production implementation` → find OpenCode
2. Read core files: `mcp/index.ts` (connection lifecycle), `mcp/catalog.ts` (tool bridging), `mcp/auth.ts` (OAuth)
3. Read lifecycle tests: `test/mcp/lifecycle.test.ts`
4. Extract COMPLETE pattern: 3 transports (stdio/StreamableHTTP/SSE), 5 connection states, OAuth PKCE flow, process tree cleanup, tool cache invalidation
5. Output findings: "Found 25+ gaps between naive implementation and reference. Key: use official SDK, not manual JSON-RPC."

**Result**: The implementation handles connection failures, orphaned processes, tool collisions, and OAuth — all things the blog tutorial never mentioned.

## Example 2: Adding a Skill System

**Task**: "Add skill auto-loading to my agent"

**Wrong approach**: Dump all skill content into the system prompt. Result: wastes context window on unused skills, skills compete for attention.

**Correct approach**:
1. Search `github agent skill system implementation` → find OpenCode skill module
2. Read: `skill/index.ts` (discovery), `tool/skill.ts` (loading), `session/system.ts` (prompt integration)
3. Extract pattern: metadata-only in prompt (name+description), XML format for structured parsing, on-demand loading via tool call, file listing in tool output
4. Output findings: "Key insight — skills are discovered at startup but CONTENT is only loaded when LLM calls the skill tool."

**Result**: The skill system saves 80%+ of context vs dumping everything, and LLM gets richer tool output with file listings.

## Example 3: Adding a Scheduler

**Task**: "Add scheduled/cron tasks to my FastAPI app"

**Wrong approach**: Write a while-loop with `asyncio.sleep()`. Result: no persistence, no cron syntax, breaks with multiple workers.

**Correct approach**:
1. Search `FastAPI APScheduler 2025 best practices` → 6 articles + GitHub repos
2. Find reference: production FastAPI boilerplate with scheduler module
3. Read APScheduler 4.x official docs: lifespan pattern, AsyncIOScheduler, job stores
4. Extract pattern: FastAPI lifespan management, SQLite jobstore for persistence, explicit timezone, misfire_grace_time, multi-worker deduplication
5. Output findings: "Avoid deprecated on_event. MemoryJobStore avoids pickle issues with closures. Must handle multi-worker duplicate execution."

**Result**: The scheduler handles restarts (persisted jobs), cron expressions, and won't silently skip missed runs.

## Key Lesson

Every example follows the same pattern:
1. **Search broadly** (docs + repos + issues) BEFORE writing code
2. **Read source code** of the reference, not just README
3. **Extract the COMPLETE pattern** — lifecycle + errors + edge cases
4. **Compare against initial assumptions** — find what you would have missed
5. **Output findings** before implementing
