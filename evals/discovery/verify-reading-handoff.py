#!/usr/bin/env python3
"""Independent offline CLI acceptance for this reading-shelf handoff task.

Example (choose a new output directory):
  python evals/discovery/verify-reading-handoff.py --app-dir ../handoff-app \
      --baseline evals/discovery/fixtures/reading-handoff/reading_shelf.py \
      --output-dir ../handoff-check

The option and Markdown parsing here is adapted to the two artifacts in this
round; this is not a generic judge for every implementation of the prompt.
The harness reads the app's --help before choosing commands, reads the fixed
app-dir/shelf.json fixture, and requires a new --output-dir outside --app-dir.
Harness-created files and app output arguments point into --output-dir. The
subprocess itself is not OS-sandboxed; use this only with the archived fixtures.
Replay JSON and console output include local paths and execution diagnostics.
Keep these raw results local; review and replace private paths before sharing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import unquote

RUN_ERRORS: list[dict[str, str]] = []
TIMEOUT_SECONDS = 15


def safe_run(command: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            check=False,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        if isinstance(stdout, str):
            stdout = stdout.encode("utf-8", "replace")
        if isinstance(stderr, str):
            stderr = stderr.encode("utf-8", "replace")
        detail = f"timeout after {TIMEOUT_SECONDS}s: {command!r}"
        RUN_ERRORS.append({"kind": "timeout", "command": repr(command), "detail": detail})
        return subprocess.CompletedProcess(command, 124, stdout, stderr + (detail + "\n").encode())
    except (OSError, ValueError) as error:
        detail = f"{type(error).__name__}: {error}"
        RUN_ERRORS.append({"kind": "execution_error", "command": repr(command), "detail": detail})
        return subprocess.CompletedProcess(command, 127, b"", (detail + "\n").encode())
    except Exception as error:
        detail = f"{type(error).__name__}: {error}"
        RUN_ERRORS.append({"kind": "execution_error", "command": repr(command), "detail": detail})
        return subprocess.CompletedProcess(command, 127, b"", (detail + "\n").encode())


def run(script: pathlib.Path, cwd: pathlib.Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return safe_run([sys.executable, "-S", str(script), *args], cwd)


def save_bytes(path: pathlib.Path, data: bytes) -> None:
    path.write_bytes(data)


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_items(document: str) -> list[tuple[str, str, str | None]]:
    found: list[tuple[str, str, str | None]] = []
    for line in document.splitlines():
        if not line.startswith("- "):
            continue
        match = re.fullmatch(r"- \[(.*)\]\(([^)]*)\)(?: — (.*))?", line)
        if not match:
            raise ValueError(f"malformed Markdown item: {line!r}")
        label, url, note = match.groups()
        title = re.sub(r"\\(.)", r"\1", label)
        found.append((title, unquote(url), note))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-dir", type=pathlib.Path, required=True)
    parser.add_argument("--baseline", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--timeout", type=int, default=15, help="seconds allowed per app invocation (default: 15)")
    args = parser.parse_args()

    global TIMEOUT_SECONDS
    if args.timeout < 1:
        parser.error("--timeout must be at least 1 second")
    TIMEOUT_SECONDS = args.timeout

    app_dir = args.app_dir.resolve()
    app = app_dir / "reading_shelf.py"
    baseline = args.baseline.resolve()
    out = args.output_dir.resolve()
    source_data = (app_dir / "shelf.json").resolve()
    if out == app_dir or app_dir in out.parents:
        parser.error("--output-dir must be outside --app-dir")
    if out.exists():
        parser.error("--output-dir must be new; choose a path that does not already exist")
    out.mkdir(parents=True, exist_ok=False)
    if not app.is_file() or not baseline.is_file() or not source_data.is_file():
        parser.error("--app-dir must contain reading_shelf.py and shelf.json; --baseline must exist")

    report: dict[str, object] = {
        "app_dir": str(app_dir),
        "output_dir": str(out),
        "runtime": "",
        "interpreter": sys.executable,
        "launcher_mode": "python -S (site initialization disabled; no third-party modules loaded)",
        "per_invocation_timeout_seconds": TIMEOUT_SECONDS,
        "scope_note": "CLI flag and Markdown parsing adaptation covers the two handoff artifacts in this round; not a generic judge. Harness outputs are directed outside the app directory, but subprocesses are not OS-sandboxed.",
    }
    checks: dict[str, bool | int | str] = {}
    diagnostics: dict[str, bool] = {}
    source_hash_before = sha256(source_data)

    version_result = safe_run([sys.executable, "--version"], app_dir)
    report["runtime"] = (version_result.stdout or version_result.stderr).decode("utf-8", "replace").strip()
    checks["runtime_probe_exit_0"] = version_result.returncode == 0

    root_help = run(app, app_dir, ["--help"])
    export_help = run(app, app_dir, ["export", "--help"])
    list_help = run(app, app_dir, ["list", "--help"])
    for name, result in (("help-root.txt", root_help), ("help-export.txt", export_help), ("help-list.txt", list_help)):
        save_bytes(out / name, result.stdout + result.stderr)
    root_text = (root_help.stdout + root_help.stderr).decode("utf-8", "replace")
    export_text = (export_help.stdout + export_help.stderr).decode("utf-8", "replace")
    list_text = (list_help.stdout + list_help.stderr).decode("utf-8", "replace")
    checks["help_exit_codes"] = root_help.returncode == 0 and export_help.returncode == 0 and list_help.returncode == 0
    checks["export_discovered_from_help"] = "export" in root_text and export_help.returncode == 0

    output_flag = "--output" if "--output" in export_text else ("-o" if re.search(r"(?:^|[ ,])(?:-o)(?:[ ,=]|$)", export_text) else "")
    data_flag = "--data" if "--data" in root_text else ""
    format_flag = "--format" if "--format" in list_text and "markdown" in list_text else ""
    usage = root_text.splitlines()[0] if root_text.splitlines() else ""
    data_before_subcommand = bool(data_flag and usage.find("--data") >= 0 and usage.find("--data") < usage.find("{"))
    report["discovered_options"] = {
        "export_command": "export" if "export" in root_text else None,
        "output_flag": output_flag or None,
        "data_flag": data_flag or None,
        "data_position": "before subcommand" if data_before_subcommand else "after subcommand",
        "list_format_flag": format_flag or None,
        "stdout_export_advertised": "stdout" in export_text.lower(),
    }
    checks["output_option_discovered_from_help"] = bool(output_flag)
    checks["data_option_discovered_from_help"] = bool(data_flag)
    checks["markdown_list_option_discovered_from_help"] = bool(format_flag)

    def app_args(command: list[str], data: pathlib.Path | None = None) -> list[str]:
        if data is None:
            return command
        if data_before_subcommand:
            return [data_flag, str(data), *command]
        if command:
            return [command[0], data_flag, str(data), *command[1:]]
        return [data_flag, str(data)]

    baseline_default = run(baseline, baseline.parent, ["list"])
    app_default = run(app, app_dir, ["list"])
    save_bytes(out / "baseline-list-default.txt", baseline_default.stdout)
    save_bytes(out / "trial-list-default.txt", app_default.stdout)
    checks["list_default_matches_baseline"] = (
        baseline_default.returncode == app_default.returncode == 0
        and baseline_default.stdout == app_default.stdout
        and baseline_default.stderr == app_default.stderr
    )
    checks["list_default_exit"] = app_default.returncode

    if format_flag:
        baseline_markdown = run(baseline, baseline.parent, ["list", format_flag, "markdown"])
        app_markdown = run(app, app_dir, ["list", format_flag, "markdown"])
        save_bytes(out / "baseline-list-markdown.txt", baseline_markdown.stdout)
        save_bytes(out / "trial-list-markdown.txt", app_markdown.stdout)
        checks["list_markdown_matches_baseline"] = (
            baseline_markdown.returncode == app_markdown.returncode == 0
            and baseline_markdown.stdout == app_markdown.stdout
            and baseline_markdown.stderr == app_markdown.stderr
        )
        checks["list_markdown_exit"] = app_markdown.returncode
    else:
        checks["list_markdown_matches_baseline"] = False
        checks["list_markdown_exit"] = -1

    selected_path = out / "selected.md"
    file_result = run(app, app_dir, app_args(["export", output_flag, str(selected_path)])) if output_flag else subprocess.CompletedProcess([], 2, b"", b"no output option discovered")
    save_bytes(out / "export-file.stdout.txt", file_result.stdout)
    save_bytes(out / "export-file.stderr.txt", file_result.stderr)
    checks["export_file_exit_0"] = file_result.returncode == 0 and selected_path.is_file()
    selected_bytes = selected_path.read_bytes() if selected_path.is_file() else b""
    try:
        selected_text = selected_bytes.decode("utf-8")
        checks["file_is_utf8"] = True
    except UnicodeDecodeError:
        selected_text = ""
        checks["file_is_utf8"] = False
    diagnostics["file_has_no_bom"] = not selected_bytes.startswith(b"\xef\xbb\xbf")
    diagnostics["file_uses_lf"] = b"\r" not in selected_bytes

    items = json.loads(source_data.read_text(encoding="utf-8-sig"))
    chosen = [item for item in items if item.get("selected")]
    parsed_items: list[tuple[str, str, str | None]] = []
    parse_ok = True
    try:
        parsed_items = markdown_items(selected_text)
    except ValueError:
        parse_ok = False
    expected_items = []
    for item in chosen:
        note_value = item.get("note", "")
        note = " ".join(str(note_value).splitlines()) if note_value else None
        expected_items.append((str(item.get("title", "")), unquote(str(item.get("url", ""))), note))
    checks["selection_order_and_filter"] = parse_ok and parsed_items == expected_items and len(parsed_items) == len(chosen)
    checks["markdown_title_url_and_note_integrity"] = checks["selection_order_and_filter"] and "\\[brackets\\]" in selected_text and "%28v2%29" in selected_text and "下次讨论时检查。 重点看第三节。" in selected_text
    checks["empty_note_has_no_dangling_suffix"] = "A short follow-up checklist](https://example.org/follow-up)\n" in selected_text

    stdout_supported = "stdout" in export_text.lower()
    stdout_equivalent = True
    if stdout_supported and output_flag:
        stdout_result = run(app, app_dir, app_args(["export", output_flag, "-"]))
        save_bytes(out / "stdout-export.md", stdout_result.stdout)
        save_bytes(out / "stdout-export.stderr.txt", stdout_result.stderr)
        try:
            stdout_equivalent = stdout_result.returncode == 0 and markdown_items(stdout_result.stdout.decode("utf-8")) == expected_items
        except (UnicodeDecodeError, ValueError):
            stdout_equivalent = False
        checks["stdout_export_exit_0"] = stdout_result.returncode == 0
        checks["stdout_semantically_equal_to_file"] = stdout_equivalent
    else:
        checks["stdout_semantically_equal_to_file"] = True
        report["stdout_export"] = "not advertised by export --help; optional criterion skipped"

    empty_data = out / "empty-selection.json"
    empty_data.write_text("[]\n", encoding="utf-8")
    empty_path = out / "empty-handoff.md"
    empty_path.write_text("STALE CONTENT\n", encoding="utf-8")
    empty_result = run(app, app_dir, app_args(["export", output_flag, str(empty_path)], empty_data)) if output_flag and data_flag else subprocess.CompletedProcess([], 2, b"", b"required options unavailable")
    save_bytes(out / "empty-export.stdout.txt", empty_result.stdout)
    save_bytes(out / "empty-export.stderr.txt", empty_result.stderr)
    empty_bytes = empty_path.read_bytes() if empty_path.is_file() else b""
    try:
        empty_text = empty_bytes.decode("utf-8")
        valid_empty_text = empty_text.startswith("# ") and not any(line.startswith("- ") for line in empty_text.splitlines())
    except UnicodeDecodeError:
        empty_text = ""
        valid_empty_text = False
    checks["empty_selection_exit_0_no_traceback"] = empty_result.returncode == 0 and b"Traceback" not in empty_result.stderr
    checks["empty_selection_replaces_stale_with_valid_document"] = valid_empty_text and "STALE CONTENT" not in empty_text
    checks["empty_selection_has_clear_diagnostic"] = any(token in empty_result.stderr.lower() for token in (b"empty", b"no item", b"no selected"))

    source_hash_after = sha256(source_data)
    checks["source_shelf_hash_unchanged"] = source_hash_before.casefold() == source_hash_after.casefold()
    checks["stdlib_only_app_runs_under_no_site"] = file_result.returncode == 0
    report["source_hash_before"] = source_hash_before
    report["source_hash_after"] = source_hash_after
    report["checks"] = checks
    report["criterion_results"] = {
        "preserve-list-contract": bool(checks["list_default_matches_baseline"] and checks["list_markdown_matches_baseline"]),
        "selection-and-order": bool(checks["selection_order_and_filter"]),
        "useful-markdown": bool(checks["markdown_title_url_and_note_integrity"] and checks["empty_note_has_no_dangling_suffix"]),
        "file-and-stdout": bool(checks["export_file_exit_0"] and checks["file_is_utf8"] and checks["stdout_semantically_equal_to_file"]),
        "empty-selection": bool(checks["empty_selection_exit_0_no_traceback"] and checks["empty_selection_replaces_stale_with_valid_document"] and checks["empty_selection_has_clear_diagnostic"]),
        "local-inheritance": bool(checks["source_shelf_hash_unchanged"] and checks["stdlib_only_app_runs_under_no_site"] and checks["runtime_probe_exit_0"]),
    }
    report["diagnostics_not_part_of_frozen_criteria"] = diagnostics
    report["execution_errors"] = RUN_ERRORS
    report["all_criteria_pass"] = all(report["criterion_results"].values()) and not RUN_ERRORS
    report["selected_file_sha256"] = sha256(selected_path) if selected_path.is_file() else None
    report["empty_file_sha256"] = sha256(empty_path) if empty_path.is_file() else None
    (out / "cli-acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["all_criteria_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
