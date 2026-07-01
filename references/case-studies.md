# Case Studies — Research-First in Action

## Case 1: Adding MCP Client to Axiom

**Task**: "Add MCP support to the agent platform"

**Without skill (what would have happened)**:
- Search "how to implement JSON-RPC Python"
- Build from scratch based on blog tutorial
- Miss: SSE transport, OAuth, process lifecycle, tool caching

**With skill (what actually happened)**:
- Phase 0: Axiom is an AI agent platform. MCP is how agents connect to external tools.
- Phase 1: Expanded "add MCP" to 10 dimensions → found tool naming, caching, security, lifecycle
- Phase 2: Found OpenCode's 1013-line `mcp/index.ts`, read source code + tests
- Phase 3: Extracted: 3 transports, 5 connection states, OAuth PKCE, process tree cleanup
- Phase 4: LEARN-FROM — different language (TypeScript→Python) but same patterns
- Phase 5: All 11 boxes checked
- Phase 6: Output structured findings, identified 25+ gaps vs naive implementation

**Result**: Production-grade MCP client with StreamableHTTP, tool caching, connection robustness.
30+ gaps found that a blog tutorial would never have mentioned.

## Case 2: Adding Skill System to Axiom

**Task**: "Add skill auto-loading to agents"

**Without skill**:
- Dump all skill content into system prompt
- No dedup, no budget control, no progressive disclosure

**With skill**:
- Phase 0: Agent platform → skills = reusable agent knowledge
- Phase 1: Expanded to data (schema), lifecycle (discovery→load→unload), security (injection)
- Phase 2: Found agentskills.io spec, Claude Code skill architecture, OpenCode skill system
- Phase 3: Extracted 3-tier progressive disclosure, XML metadata format, user-message injection
- Phase 4: ADAPT — same concept, different implementation
- Phase 6: Output showed metadata-only registry saves 80%+ context vs dumping content

**Result**: Claude Code-compatible skill system with on-demand loading, session dedup, budget cap.

## Case 3: Adding Scheduler to Axiom

**Task**: "Add scheduled/cron tasks to FastAPI"

**Without skill**:
- Write `while True: await asyncio.sleep(60)`
- No persistence, no cron syntax, breaks with multiple workers

**With skill**:
- Phase 1: Expanded to lifecycle (startup→shutdown), performance (multi-worker dedup)
- Phase 2: Found APScheduler 4.x best practices (2025), sodipto/fastapi-starter-boilerplate
- Phase 3: Extracted: lifespan management (not deprecated on_event), AsyncIOScheduler, timezone
- Phase 5: Found pickle issue with SQLAlchemyJobStore → switched to MemoryJobStore

**Result**: APScheduler 4.x with FastAPI lifespan, SQLite-persisted jobs, proper cleanup.

## Pattern: What All Three Cases Share

1. Started with project identity, not just the task
2. Expanded from surface question to 10+ dimensions before searching
3. Found at least 2 independent production references
4. Read source code and tests, not just README
5. Made explicit reuse/adapt/learn-from decisions
6. Found at least one "I would have missed this" insight per case
7. Output structured findings before writing code
