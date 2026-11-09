# Research Tools

Use this guide when the evidence needed depends on a documentation, package or
repository lookup tool the host may or may not expose. The goal is a grounded
answer, not tool installation for its own sake.

## Decide Whether a Tool Would Change the Answer

Check before suggesting anything:

1. **What is already callable.** Do not propose installing what the host already
   provides. A tool listed as unavailable, unauthenticated or failing to connect
   is not a working route — try it once with a harmless call before relying on it.
2. **What local evidence settles first.** A manifest, lockfile, installed package
   under `node_modules/` or `site-packages/`, vendored source, tests or a small
   probe may answer the question without any external service. Local evidence
   describes this project; a documentation service describes a library.
3. **Whether the question is version-sensitive.** An API shape, option name,
   deprecation or migration question usually is. A conceptual question often is
   not, and may not justify a new dependency in the user's environment.

Suggest a tool only when its absence would leave a decision-changing claim
unverified. Do not turn a small edit into an installation project, and do not
suggest a tool during research-only work unless it is the only remaining route to
the evidence the user asked for.

## Ask Before Changing the Environment

Installing an MCP server edits the user's global configuration, starts a local
process, or sends queries to a third party. Treat it as an external commitment:

- State which tool, which host configuration it modifies, whether it needs an API
  key, and what leaves the machine.
- Offer the local-evidence alternative if one exists.
- Do not install, edit configuration files, or run a third-party setup command
  unless the user agrees. A research or review request does not authorize it.
- Prefer the narrower scope when the user does agree: a project-scoped
  configuration over a user-wide one, and a read-only documentation lookup over a
  server that can act on repositories or accounts.
- Send only public identifiers, package names, API names, file paths within the
  library, and error text. Keep private source, customer data and messages local.

## Tool Roles

| Tool | Answers | Cannot establish |
|---|---|---|
| Library documentation server (Context7) | Current documented API, options, examples for a named package | Whether this app is wired correctly; unversioned results may describe another major version |
| Repository wiki (DeepWiki) | Architecture, data flow and design rationale of a public GitHub repository | A pinned release's exact behavior; it indexes a repository, not a version |
| Web/neural search (Exa and similar) | Which projects, discussions or pages address a problem | That a page was read or that its claim is current |
| Package registry (npm, PyPI, NuGet, Maven) | Versions, publish dates, license, dependencies, repository URL | Runtime behavior or integration fit |
| Vendor SDK documentation server | Supported contract for that vendor's platform | The local project's state or configuration |
| Local installed source, tests, probes | What this project actually runs | Whether a different version behaves the same |

A documentation server and a repository wiki both describe intent; neither runs
your code. Keep the acceptance check from [execution evidence](execution-evidence.md).

## Installation Commands

Verify each command against the vendor's current page before using it; these were
checked on 2026-11-09 and may drift. Run them yourself only with the user's
agreement.

### Context7 — version-addressable library documentation

Two routes: a remote HTTP endpoint, or a local `npx` process. The API key is
optional per the vendor and raises rate limits; the vendor does not publish
numeric limits, and none were measured here.

Claude Code, remote:

```bash
claude mcp add --scope user --transport http context7 https://mcp.context7.com/mcp
```

Claude Code, remote with an API key (`https://context7.com/dashboard?tab=settings`):

```bash
claude mcp add --scope user --transport http context7 https://mcp.context7.com/mcp \
  --header "Authorization: YOUR_API_KEY"
```

Claude Code, local process:

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

Codex, remote:

```bash
codex mcp add context7 --url https://mcp.context7.com/mcp
```

Codex, equivalent configuration:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
```

On the version checked here, that Codex command triggers an OAuth browser flow
and stores OAuth credentials under `CODEX_HOME`; it is not a silent config edit.
Say so before suggesting it.

The vendor also ships `npx ctx7 setup --claude`, a third-party installer that
edits client configuration for you. Inspect what it writes before running it, or
use the explicit commands above.

Query pattern: resolve the library id first, then query it. Prefer the
version-qualified id the catalog exposes (for example `/tanstack/table/v8.20.5`)
over the default entry, which may serve the main branch or a different major
version. A resolve that returns a similarly named or umbrella project is a miss,
not documentation.

### DeepWiki — public repository wiki

```bash
claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp
```

Endpoint: `https://mcp.deepwiki.com/mcp` (streamable HTTP; the `/sse` endpoint is
legacy). Useful for architecture and rationale questions about a public
repository. It indexes a repository rather than a release, so use a pinned tag or
the installed source for behavior that depends on an exact version. Private
repositories and the `devin_*` tools require an account; do not assume they work
anonymously.

The community `mcp-deepwiki` npm package is a separate, self-hosted server. Its
own README calls the current version broken and points to the hosted service.

### Exa — web and neural search

```bash
claude plugin install exa@claude-plugins-official
```

Or connect the MCP endpoint directly at `https://mcp.exa.ai/mcp`, which needs an
`x-api-key` header for direct access; the plugin path signs in instead. Results
are discovery leads until the underlying page is read.

### Package registries

Often enough on their own, and they need no installation. `npm view <pkg>
versions`, `npm view <pkg> dist.tarball`, `pip index versions <pkg>`, the PyPI
JSON API and the NuGet registration API return versions, dates, license and
repository URL. Use them to establish what exists and which version is current;
read the source or documentation for behavior.

## Confirm a Tool Actually Works

A configuration entry proves nothing. After adding a server, start a new session
and make one representative call whose answer you can check — for a documentation
server, resolve a package the project actually uses and confirm the version
segment exists. Record the tool, the identifier, and whether the response matched
the installed version.

If the call fails, is unauthenticated, times out, or serves another version, treat
the route as unavailable for this claim, say so, and fall back to versioned
official documentation, a pinned source, or a local probe. An installation
suggestion is not a substitute for evidence, and a failed tool does not prove that
no documentation exists.
