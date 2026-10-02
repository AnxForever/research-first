# Evaluation Record

On 2026-09-22, one research-and-implementation experiment was completed in a
real open-source project, with Jev checks on several short evidence cards. This
record preserves the observed results, reproducible materials, and limitations;
the small sample is not a general performance guarantee.

## Real-project experiment

Project: [satnaing/shadcn-admin](https://github.com/satnaing/shadcn-admin), MIT,
at fixed baseline
[`e16c87f`](https://github.com/satnaing/shadcn-admin/tree/e16c87f213a5ba5e45964e9b67c792105ec74d26).
The experiment used an isolated clone and did not submit changes upstream. The
environment was Windows, Node 24.14.0, pnpm 10.28.0, React 19, and TanStack
Table 8.21.3.

The evaluation request was written for this experiment; it was not an issue
submitted by an upstream user:

> Make the bulk CSV export on the Tasks page actually work, and make the exported file useful for organizing tasks afterward.

The original handler only called `sleep(2000)`, showed a toast, and cleared the
selection; it did not encode CSV or initiate a download. This finding came from
reviewing the complete source. An earlier browser-tool timeout was not treated
as valid evidence that no download occurred.

An independent agent followed the skill to investigate before implementation
and showed the options first. It examined Linear's export workflow, MUI/MRT
table export, TanStack v8 row models, CSV/BOM/download documentation, and the
fixed-version source of two candidate libraries. See the [research record](shadcn-admin-research.md)
for the full evidence and the per-feature ledger prepared before implementation.

| Approach | Fit found | Cost | Decision |
|---|---|---|---|
| Papa Parse 5.7.0 | Explicit fields, quoting/newlines, configurable formula escaping | Adds a runtime dependency and type declarations; the project still owns scope selection and download | Adopted at a pinned version |
| export-to-csv 1.5.0 | Typed ESM, CSV/BOM, and a download helper | Still needs resource cleanup and text protection for these inputs | Shown to the user; not adopted |
| Hand-written encoding | Five string fields could be encoded locally | Saves a dependency but requires maintaining CSV and formula edge cases | Shown to the user; not adopted |
| Replace the table/UI stack | Could provide other export capabilities | Existing TanStack/shadcn interactions already fit; migration had no matching benefit | Kept the existing components |

The findings informed the implementation:

- Selected rows from the filtered and sorted full row model, including selected
  rows across pages; did not copy a third-party row-selection example directly.
- Fixed the columns to `id,title,status,label,priority`, preserved full values,
  and excluded mock metadata outside the Task contract.
- Reused Papa Parse for encoding and emitted UTF-8 BOM and CRLF. After inspecting
  the pinned implementation, extended formula-prefix rules for tested leading
  newlines, whitespace, and full-width symbols. The added apostrophe changes
  cell data, and the project documentation says so.
- Kept the selection after both success and failure so failures can be retried;
  the UI says a download was initiated and does not claim to know whether the
  user saved it.

### Checks performed

| Check | Result and scope |
|---|---|
| Original project build | `pnpm build` passed before implementation |
| Modified Tasks tests | 5 files / 39 tests passed: 19 encoding and download-lifecycle tests, 4 real TanStack integration tests, and 16 existing form tests |
| Build and lint after changes | `pnpm build` and `pnpm lint` passed |
| Changed-file format and patch | Prettier and `git diff --check` passed; `git apply --check` passed on a clean baseline worktree |
| Independent real downloads | Edge 153.0.4234.48 saved 3 files; Python's standard library parsed and compared all five fields, row order, CRLF, and BOM; empty-selection and selection-retention checks passed |

The download clicks in the 39 automated tests used spies; those tests alone do
not prove that a file reached disk. The independent browser check used real
Playwright `download` events and `saveAs`, without Blob/anchor mocks. Its records
and artifacts are:

| File | Parsed result | Size |
|---|---|---|
| [cross-page.csv](shadcn-admin-browser/cross-page.csv) | TASK-9366 on page 1 and TASK-9874 on page 2; 2 rows | 228 bytes |
| [filtered.csv](shadcn-admin-browser/filtered.csv) | Only TASK-9366 after filtering | 153 bytes |
| [sorted-descending.csv](shadcn-admin-browser/sorted-descending.csv) | Descending title order, TASK-9874 before TASK-9366 | 228 bytes |

All three `download.failure()` values were `null`; the BOM was `efbbbf`. Clearing
the filter restored the original selections on both pages. Clearing selection
removed the export control and caused no additional download. See the
[raw browser result](shadcn-admin-browser/result.json) and the
[rerunnable script](verify-shadcn-export.mjs).

For distribution, only the three machine-specific absolute download paths in
the raw JSON were shortened to relative artifact filenames in the same
directory. Byte counts, BOM, download status, actual row values, and all other
observed fields remain unchanged. The result file contains no SHA field.

The earlier agent-browser 0.37.1 / Chrome 153.0.8010.47 download path repeatedly
returned `Download was canceled`; explicitly setting a download directory did
not resolve it. The cause is unknown. The existing project Playwright setup and
local Edge subsequently saved the files, with no application-code change. The
evidence therefore supports the Edge path only; it does not show that the CLI
issue was fixed or establish cross-browser coverage.

### Reproduce the implementation

The [implementation patch](shadcn-admin-export.patch) contains source changes,
dependency lockfile updates, project documentation, and new tests. The
upstream project's copyright notice is included in
[LICENSE.shadcn-admin](LICENSE.shadcn-admin). The commands below assume both
repositories are siblings:

```bash
git clone https://github.com/satnaing/shadcn-admin.git
cd shadcn-admin
git checkout e16c87f213a5ba5e45964e9b67c792105ec74d26
git apply --check ../research-first/evals/shadcn-admin-export.patch
git apply ../research-first/evals/shadcn-admin-export.patch
pnpm install --frozen-lockfile
pnpm exec playwright install chromium
pnpm test src/features/tasks
pnpm build
pnpm lint
```

The first local test attempt could not start because the default `::1:63315`
port was unavailable and Playwright Chromium had not been installed; it was not
counted as a pass. The final run used a temporary `.mts` configuration outside
the repository, extending the project's `vite.config` and changing only the
browser API to `127.0.0.1:4184` and the Playwright channel to the installed
`msedge`. The upstream test configuration was not changed. In other
environments, the Chromium command above should usually work as written.

The real-download script needs Node, Python, the target project's installed
Playwright, and a running app. Start `pnpm dev --host 127.0.0.1 --port 4173` in
the target project, then run this from the research-first root in another
terminal:

```bash
node evals/verify-shadcn-export.mjs ../shadcn-admin ../new-export-artifacts
```

The script uses an installed Playwright Chromium by default. To reproduce the
Edge environment, set `CSV_BROWSER_CHANNEL` to `msedge`. The output directory
must be new; an optional third argument specifies another Tasks page URL.

## Jev checkpoints and observations

TypeSafe's official [model list](https://docs.typesafe.ai/models),
[API](https://docs.typesafe.ai/api), and
[limitations for 1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
were checked on 2026-09-22. The adapter used `typesafe-sdk==0.7.1`; the
evaluation pinned `jev-1.13.0`, and a separate live `jev-latest` probe returned
that version.

Each card asked one bounded question. Labels and explanations were not sent to
the model. The expected labels were recorded by the task agent before seeing
the corresponding responses; **there was no independent human annotation**.
Raw probabilities, model versions, errors, and disagreements were retained.
Local rules did not override the model answers, and the evaluation was not
rerun with tuned settings to improve the results.

| Data group | Type | Successful calls | Match with pre-label | Mean client latency |
|---|---|---:|---:|---:|
| [12 boundary cards](jev-cases.json) · [raw responses](jev-boundary-results.json) | Agent-authored synthetic cases with Chinese constraints, instructions inside quotes, hidden alternatives, and unrun tests | 12/12 | 12/12 | 1037.2 ms |
| [4 project cards](shadcn-admin-before.json) · [raw responses](shadcn-admin-before-results.json) | Derived from real pre-implementation research, including deliberately incorrect diagnostic claims | 4/4 | 3/4 | 1246.8 ms |
| [2 completion cards](shadcn-admin-after.json) · [raw responses](shadcn-admin-after-results.json) | Follow-up diagnosis after real-file acceptance; not an independent held-out set | 2/2 | 2/2 | 1166.8 ms |

Read the groups separately; do not combine them into an “overall accuracy.” The
four project cards are neither four actual defects nor four independent
projects.

One clear disagreement concerned the choice summary: it mentioned a hand-written
approach but omitted its maintenance cost. The pre-label was `contradicted`,
while Jev returned `supported`; raw confidence was `0.47`, with probabilities
of supported `0.64` / contradicted `0.35` / insufficient `0.01`. The agent still
added the dependency benefit and maintenance cost of the hand-written option.
This does not show that Jev found or fixed the omission, and this sample cannot
set an automatic release threshold.

The other project cards compared the request interpretation, a claim about the
old handler, and a claim that planned tests had already verified behavior. Jev
received only short evidence; it did not read source, look up citations, or run
tests. The CSV edge cases came from the actual research.

The last two cards used executed browser results. Jev supported the bounded
claim that Edge saved the two cross-page selected tasks and labeled the
deliberately overstated claim “verified in Excel and LibreOffice” as
`insufficient`. The latter was never a delivery claim. This demonstrates the
completion checkpoint; it caused no new implementation change.

The boundary cards used 6072 input tokens, the pre-implementation project cards
2393, and the completion cards 1373. At the documented rate on that date of
$0.042 per million input tokens, the estimated costs were $0.000255024,
$0.000100506, and $0.000057666, respectively, excluding the alias probe. These
are calculations, not a vendor invoice. Latency includes client overhead and is
not server-side model inference time.

### Reproduce Jev checks

Run this command from the research-first root. The default preview is offline
and needs no SDK, extra dependencies, or API key:

```bash
python evals/run_jev_cases.py evals/jev-cases.json preview-results.json
```

To run the current full maintainer test suite, first install the validation and
optional SDK dependencies. Installation needs network access; the tests use
local data and mocks and do not send live API requests:

```bash
python -m pip install -r scripts/requirements-dev.txt -r scripts/requirements-jev.txt
python -m unittest discover -s tests -v
```

In the 2026-09-22 evaluation, the adapter and runner had **19 offline tests
pass** in a virtual environment with the pinned SDK installed. They covered
explicit live calls, output validation, errors/timeouts, model versions,
report reservation, and probe-failure statistics. Without the optional SDK,
2 SDK contract tests are skipped. This is a historical result for the code at
that time, not the current test count for later versions; these local tests do
not measure model capability.

When TypeSafe calls are enabled and `TYPESAFE_API_KEY` is supplied securely by
the runtime:

```bash
python -m pip install -r scripts/requirements-jev.txt
python evals/run_jev_cases.py evals/jev-cases.json new-boundary-results.json --live --probe-latest
python evals/run_jev_cases.py evals/shadcn-admin-before.json new-project-results.json --live
python evals/run_jev_cases.py evals/shadcn-admin-after.json new-completion-results.json --live
```

Only explicit `--live` calls contact TypeSafe. When used without `--live`,
`--probe-latest` creates a preview payload but does not resolve `jev-latest`; the
report records `probe_status: not_run`, `request_attempted: false`, and an empty
`resolved_model`. Only `--live --probe-latest` sends the alias probe and records
the actual returned model. If a live probe fails, the runner preserves the
failure report and exits nonzero even when all card calls succeed.

Each card is sent once, with no automatic retry. The output path must be a new
file, and existing reports are not overwritten. The first boundary report was
produced by an equivalent one-off runner before the repository runner existed,
so it lacks later report fields such as `mode`; `source: jev`, the actual model,
and usage came from the real response. Reruns may differ; do not replace the
historical reports.

## Limits of the conclusion

This run shows that the skill guided an agent to investigate products, source,
and technical material, show reusable options, and apply findings to a feature
and its acceptance checks. It covers one selected project and one implementation
process, with no “without the skill” control group. It therefore does not prove
an overall success-rate improvement or that Jev improved the final
implementation.

The current recommendation is to use Jev as needed at the intent, evidence,
choice, and completion checkpoints. Model output is advisory; it does not replace
user choices, evidence verification, or execution results. The ordinary skill
workflow needs no Jev, SDK, or API key.

The project still uses demo data. Import, CRUD, and backend persistence were
outside this task. Real Excel/LibreOffice behavior, non-Chromium browsers, all
regional separators, very large datasets, and full accessibility use were not
verified. Formula-prefix protection covers the tested inputs; it does not
guarantee that protection survives repeated saves in arbitrary spreadsheet
software.
