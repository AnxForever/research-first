# Outcome evaluations

These cases test the purpose of research-first: useful discovery that reaches a
working artifact. Package validation and the Jev unit tests serve different goals.
The cases use a public project and synthetic demo data; they need no paid service.

## Run a fair comparison

1. Freeze the skill revision, [case](cases.json), upstream commit, environment,
   and acceptance criteria before executing. Keep the rubric out of worker input.
2. Prepare independent checkouts of the pinned upstream commit. Preserve its
   license and install the frozen lockfile. Never use a person's active worktree
   or reuse another trial's generated code.
3. Give fresh workers the same task and tools, with either no skill, the previous
   skill, or the candidate skill. Load only that condition's skill and references.
   Do not provide suspected defects, solutions, earlier outputs, or grading notes.
4. Preserve the artifact, patch, source locators, commands, and actual results.
   Save raw tool transcripts and actual model/usage metadata when the host exposes
   them. Otherwise mark them unavailable; worker-authored notes are not raw traces.
5. Independently run builds and browser workflows. Evaluate the visible outcome,
   not one prescribed DOM structure, package, or implementation. Distinguish a
   broken test selector/environment from an application failure before grading.
6. Review whether findings affected choices or validation. A passing implementation
   can have poor research; a careful report can accompany a broken implementation.
7. Repair only a demonstrated instruction gap, then forward-test in a clean context.
   Include a different task that did not inform the repair. Keep earlier failures.

Use a normal implementation request without explicit delegation in some trials:
routine choices should not require a special authorization phrase. Also check the
preserved boundaries in the cases file when changing scope or permission wording.

Use the same requested model configuration across conditions and record any host
differences. Repeat matched trials before claiming reliable superiority. A single
case can find a defect, but cannot establish a general success-rate improvement.
These principles follow outcome/trace separation and repeated-trial guidance in
[Anthropic's agent evaluation guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

## What to judge

| Dimension | Evidence | What does not establish it |
|---|---|---|
| User outcome | Independent interaction or artifact checks | Agent says it works |
| Useful discovery | A relevant omission or candidate, supported and carried into a decision/check | Number of searches or library names |
| Reuse fit | Inspected contract, local integration and remaining responsibilities | Popularity or adopting a dependency |
| Scope and autonomy | Work completed within constraints, necessary questions only | Following every template heading |
| Verification honesty | Actual results and explicit gaps agree with the artifact | A build labeled as full UX verification |
| Effort | Measured elapsed time, calls and tokens where available | Markdown length treated as token cost |

Keep each dimension separate. Do not hide a failed core workflow in an average
score, award points for a particular phrase, or treat unknown as pass. Independent
graders should receive anonymized artifacts when practical; disclose residual
clues instead of calling a review perfectly blind.

## Reproduce the recorded UI acceptance

See the [2026-10-02 evaluation report](2026-10-02.md) and the preserved
[structured browser observations](observations-2026-10-02.json). The two patches
target separate fresh checkouts of
[`satnaing/shadcn-admin` at `e16c87f213a5ba5e45964e9b67c792105ec74d26`](https://github.com/satnaing/shadcn-admin/tree/e16c87f213a5ba5e45964e9b67c792105ec74d26).
The pinned [upstream package scripts](https://github.com/satnaing/shadcn-admin/blob/e16c87f213a5ba5e45964e9b67c792105ec74d26/package.json#L5-L10)
provide the `build` and `preview` commands used below.
Each checkout retains the upstream MIT license. Start from this repository's
root; the commands below assume it is named `research-first` and create both
fixtures beside it. Do not apply both feature patches to one checkout or add the
older CSV-export patch.

```powershell
git clone https://github.com/satnaing/shadcn-admin.git ..\shadcn-admin-navigation
git clone https://github.com/satnaing/shadcn-admin.git ..\shadcn-admin-saved-views

git -C ..\shadcn-admin-navigation checkout e16c87f213a5ba5e45964e9b67c792105ec74d26
git -C ..\shadcn-admin-saved-views checkout e16c87f213a5ba5e45964e9b67c792105ec74d26

git -C ..\shadcn-admin-navigation apply --check ..\research-first\evals\behavioral\navigation.patch
git -C ..\shadcn-admin-navigation apply ..\research-first\evals\behavioral\navigation.patch
git -C ..\shadcn-admin-saved-views apply --check ..\research-first\evals\behavioral\saved-views.patch
git -C ..\shadcn-admin-saved-views apply ..\research-first\evals\behavioral\saved-views.patch
```

For each checkout, begin without `node_modules` or `dist`, then install the
frozen dependencies and build. The recorded Windows run used Node 24.14.0, pnpm
12.4.2, Python 3.12.10, Playwright 1.57.0, and locally installed Microsoft
Edge:

```powershell
Set-Location ..\shadcn-admin-navigation
pnpm install --frozen-lockfile --ignore-scripts
pnpm build
pnpm preview --host 127.0.0.1 --port 4313
```

Leave that preview server running. Open a second terminal at the `research-first`
root and prepare a dedicated Python 3.12 virtual environment outside the
checkouts. The browser scripts use
the installed Microsoft Edge through Playwright's `msedge` channel, so do not
run `playwright install`:

```powershell
py -3.12 -m venv ..\research-first-browser-venv
..\research-first-browser-venv\Scripts\python.exe -m pip install playwright==1.57.0
& ..\research-first-browser-venv\Scripts\python.exe evals\behavioral\verify-navigation.py --sample candidate --url http://127.0.0.1:4313 --output ..\research-first-navigation-results
```

The navigation runner creates a timestamped result directory beneath the
`--output` root, including `report.json` and screenshots. For saved views, stop
the first preview server, start the separate patched checkout, and use a new
output directory:

```powershell
Set-Location ..\shadcn-admin-saved-views
pnpm install --frozen-lockfile --ignore-scripts
pnpm build
pnpm preview --host 127.0.0.1 --port 4314
```

In another terminal at the `research-first` root:

```powershell
& ..\research-first-browser-venv\Scripts\python.exe evals\behavioral\verify-saved-views.py --url http://127.0.0.1:4314 --output ..\research-first-saved-views-results
```

The saved-views runner requires that its `--output` directory not already exist;
it writes `browser-results.json` and screenshots there. Both runners accept only
loopback URLs without credentials, restrict page requests to that local origin,
and launch the installed Edge channel. The navigation report records intentionally
blocked external assets separately from local application errors. Choose unused loopback ports
and fresh output paths if those shown above are occupied. Reapplying these
patches and running the browser checks verifies the application artifacts; it
does not rerun a model trial or establish general research-first skill quality.

## Local checks versus host behavior

An explicitly loaded trial establishes behavior under those instructions. Test
automatic selection separately in the actual supported host, using normal prompts
and positive/negative controls. Listing an installed skill only verifies discovery;
it does not establish activation or task quality. Do not simulate selection by
asking a model whether it thinks the skill should apply.

The stored cases and rubrics are maintainer material. Do not load this directory
into ordinary user tasks or count the repository's fictional examples as evidence
about the current project.
