# Research-First Examples

## Example 1: Building an MCP Client

**Task**: "Add MCP client to AgentOS"

**Wrong approach**: Write JSON-RPC from scratch based on blog post.

**Correct approach**:
1. Read OpenCode source: `reference/opencode/packages/opencode/src/mcp/index.ts` (1013 lines)
2. Read OpenCode catalog: `reference/opencode/packages/opencode/src/mcp/catalog.ts`
3. Read OpenCode auth: `reference/opencode/packages/opencode/src/mcp/auth.ts`
4. Read OpenCode lifecycle tests: `reference/opencode/packages/opencode/test/mcp/lifecycle.test.ts`
5. Extract COMPLETE pattern: 3 transports (stdio/StreamableHTTP/SSE), 5 connection states, OAuth PKCE flow, process tree cleanup, tool cache invalidation

**Result**: Found 30+ gaps between naive implementation and production reference.

## Example 2: Building a Skill System

**Task**: "Add skill auto-loading to AgentOS"

**Wrong approach**: Hardcode a skill-to-task mapping table in system prompt.

**Correct approach**:
1. Read OpenCode skill discovery: `reference/opencode/packages/opencode/src/skill/index.ts`
2. Read OpenCode skill tool: `reference/opencode/packages/opencode/src/tool/skill.ts`
3. Read OpenCode system prompt: `reference/opencode/packages/opencode/src/session/system.ts`
4. Read OpenCode skill schema: `reference/opencode/packages/schema/src/skill.ts`
5. Extract COMPLETE pattern: metadata-only in system prompt, XML registry format, on-demand loading via skill tool, file listing in tool output, multi-source discovery

**Result**: Found that injecting full skill content into system prompt wastes context; metadata + tool call is the correct pattern.

## Example 3: Building a Scheduler

**Task**: "Add scheduled tasks to AgentOS"

**Wrong approach**: Write a while-loop with asyncio.sleep().

**Correct approach**:
1. Search "FastAPI APScheduler 2025 best practices" → found 6 articles
2. Search "github FastAPI boilerplate scheduler 2025" → found sodipto/fastapi-starter-boilerplate
3. Read APScheduler 4.x official docs → lifespan pattern, AsyncIOScheduler
4. Extract COMPLETE pattern: lifespan management, SQLite jobstore, explicit timezone, misfire_grace_time, multi-worker dedup

**Result**: Avoided the deprecated `on_event` pattern and the pickle issue with SQLAlchemyJobStore.
