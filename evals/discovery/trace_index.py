#!/usr/bin/env python3
"""Create a privacy-preserving index of observed Claude Code stream-json events.

This is a maintainer audit aid, not a source-truth or skill-quality checker. It
does not execute commands, make network requests, or copy tool parameters and
results into the index. The schema support is limited to the Claude Code event
envelopes observed by this repository's evaluation; it is not a promise about
all Claude Code versions or other hosts.

Example:
    python evals/discovery/trace_index.py --input events.jsonl --output index.json

The output must be a new file in an existing directory. It contains raw trace
hashes, event line numbers, tool-use IDs, hashes and lengths of normalized JSON
values, and structural anomaly flags. Lengths count Python Unicode code points.
It intentionally contains no overall pass/fail or evidence-quality judgment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


SCHEMA = "claude-code-stream-json-index"
SCHEMA_VERSION = 1

# Only common, non-MCP Claude Code tool labels are shown. Unknown and custom
# tool names are represented by a hash so the index cannot disclose a private
# tool inventory by default.
PUBLIC_TOOL_LABELS = frozenset({
    "Bash", "Edit", "Glob", "Grep", "PowerShell", "Read", "Skill", "WebFetch", "WebSearch", "Write",
})


class DuplicateJSONKey(ValueError):
    """Raised when a JSON object repeats a property name."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    # Python's decoder accepts NaN and Infinity by default although JSON does not.
    raise ValueError("non-standard JSON constant")


def canonical_json(value: Any) -> str:
    """Return the exact serialization used for input/result fingerprints."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def fingerprint(value: Any) -> dict[str, Any]:
    serialized = canonical_json(value)
    return {
        "sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "normalized_json_chars": len(serialized),
    }


def _raw_line_fingerprint(line: bytes) -> dict[str, Any]:
    return {
        "sha256": hashlib.sha256(line).hexdigest(),
        "line_content_bytes": len(line),
    }


def _split_lines(raw: bytes) -> list[bytes]:
    if not raw:
        return []
    lines = raw.split(b"\n")
    if lines[-1] == b"":  # The final newline terminates the last record.
        lines.pop()
    return [line[:-1] if line.endswith(b"\r") else line for line in lines]


def _parse_line(line: bytes) -> Any:
    text = line.decode("utf-8")
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
    )


def _ensure_utf8_json(value: Any) -> None:
    """Reject JSON strings that cannot be represented in the index's UTF-8 hashes."""
    if isinstance(value, str):
        value.encode("utf-8")
    elif isinstance(value, list):
        for item in value:
            _ensure_utf8_json(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            key.encode("utf-8")
            _ensure_utf8_json(item)


def _indexed_values(event: dict[str, Any]):
    """Yield only values that can be copied or fingerprinted into the index."""
    if event.get("type") == "system" and event.get("subtype") == "init":
        if "model" in event:
            yield event["model"]
        if "tools" in event:
            yield event["tools"]
        return
    if event.get("type") == "system" and event.get("subtype") == "permission_denied":
        if "tool_use_id" in event:
            yield event["tool_use_id"]
        return
    if event.get("type") not in {"assistant", "user"}:
        return
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return
    expected = "tool_use" if event["type"] == "assistant" else "tool_result"
    for block in content:
        if isinstance(block, dict) and block.get("type") == expected:
            yield block


def _tool_label(name: Any) -> tuple[str | None, str | None]:
    if not isinstance(name, str) or not name:
        return None, None
    name_hash = fingerprint(name)["sha256"]
    if name in PUBLIC_TOOL_LABELS:
        return name, name_hash
    return "other", name_hash


def index_bytes(raw: bytes) -> dict[str, Any]:
    """Index tool calls/results without retaining their raw values."""
    lines = _split_lines(raw)
    malformed_lines: list[dict[str, Any]] = []
    malformed_events: list[dict[str, Any]] = []
    init_events: list[dict[str, Any]] = []
    uses: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    denials: list[dict[str, Any]] = []

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            malformed_lines.append({
                "line_number": line_number,
                "kind": "blank_line",
                **_raw_line_fingerprint(raw_line),
            })
            continue
        try:
            event = _parse_line(raw_line)
        except UnicodeDecodeError:
            malformed_lines.append({
                "line_number": line_number,
                "kind": "invalid_utf8",
                **_raw_line_fingerprint(raw_line),
            })
            continue
        except DuplicateJSONKey:
            malformed_lines.append({
                "line_number": line_number,
                "kind": "duplicate_json_key",
                **_raw_line_fingerprint(raw_line),
            })
            continue
        except (json.JSONDecodeError, ValueError):
            malformed_lines.append({
                "line_number": line_number,
                "kind": "malformed_json",
                **_raw_line_fingerprint(raw_line),
            })
            continue

        if not isinstance(event, dict):
            malformed_events.append({"line_number": line_number, "kind": "top_level_not_object"})
            continue

        try:
            for value in _indexed_values(event):
                _ensure_utf8_json(value)
        except UnicodeEncodeError:
            malformed_lines.append({
                "line_number": line_number,
                "kind": "non_utf8_json_value",
                **_raw_line_fingerprint(raw_line),
            })
            continue

        event_type = event.get("type")
        subtype = event.get("subtype")
        if event_type == "system" and subtype == "init":
            model_present = "model" in event
            tools_present = "tools" in event
            model = fingerprint(event["model"]) if model_present else None
            inventory = fingerprint(event["tools"]) if tools_present else None
            statuses = []
            if not model_present:
                statuses.append("missing_model")
            if not tools_present:
                statuses.append("missing_tool_inventory")
            init_events.append({
                "line_number": line_number,
                "model": model,
                "tool_inventory": {
                    **inventory,
                    "item_count": len(event["tools"]) if isinstance(event.get("tools"), list) else None,
                } if inventory else None,
                "statuses": statuses,
            })
            continue

        if event_type == "system" and subtype == "permission_denied":
            tool_use_id = event.get("tool_use_id")
            denials.append({
                "line_number": line_number,
                "tool_use_id": tool_use_id if isinstance(tool_use_id, str) and tool_use_id else None,
            })
            if not isinstance(tool_use_id, str) or not tool_use_id:
                malformed_events.append({"line_number": line_number, "kind": "permission_denial_missing_tool_use_id"})
            continue

        if event_type == "assistant":
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if not isinstance(content, list):
                continue
            for block_index, block in enumerate(content):
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                tool_use_id = block.get("id")
                name = block.get("name")
                has_input = "input" in block
                statuses = []
                if not isinstance(tool_use_id, str) or not tool_use_id:
                    statuses.append("malformed_tool_use_id")
                    tool_use_id = None
                if not isinstance(name, str) or not name:
                    statuses.append("malformed_tool_name")
                if not has_input:
                    statuses.append("missing_tool_input")
                label, name_hash = _tool_label(name)
                uses.append({
                    "line_number": line_number,
                    "block_index": block_index,
                    "tool_use_id": tool_use_id,
                    "tool_label": label,
                    "tool_name_sha256": name_hash,
                    "input": fingerprint(block["input"]) if has_input else None,
                    "statuses": statuses,
                    "result_events": [],
                    "permission_denial_lines": [],
                })
            continue

        if event_type == "user":
            message = event.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if not isinstance(content, list):
                continue
            for block_index, block in enumerate(content):
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                tool_use_id = block.get("tool_use_id")
                statuses = []
                if not isinstance(tool_use_id, str) or not tool_use_id:
                    statuses.append("malformed_tool_result_id")
                    tool_use_id = None
                has_content = "content" in block
                if not has_content:
                    statuses.append("missing_tool_result_content")
                has_is_error = "is_error" in block
                is_error = block.get("is_error") if has_is_error else None
                if has_is_error and not isinstance(is_error, bool):
                    statuses.append("malformed_is_error_flag")
                    is_error = None
                elif is_error is True:
                    statuses.append("tool_error")
                results.append({
                    "line_number": line_number,
                    "block_index": block_index,
                    "tool_use_id": tool_use_id,
                    "result": fingerprint(block["content"]) if has_content else None,
                    "is_error": is_error,
                    "statuses": statuses,
                })

    uses_by_id: dict[str, list[dict[str, Any]]] = {}
    results_by_id: dict[str, list[dict[str, Any]]] = {}
    denials_by_id: dict[str, list[int]] = {}
    for use in uses:
        if use["tool_use_id"] is not None:
            uses_by_id.setdefault(use["tool_use_id"], []).append(use)
    for result in results:
        if result["tool_use_id"] is not None:
            results_by_id.setdefault(result["tool_use_id"], []).append(result)
    for denial in denials:
        if denial["tool_use_id"] is not None:
            denials_by_id.setdefault(denial["tool_use_id"], []).append(denial["line_number"])

    for tool_use_id, matching_uses in uses_by_id.items():
        matching_results = results_by_id.get(tool_use_id, [])
        denial_lines = denials_by_id.get(tool_use_id, [])
        duplicate_uses = len(matching_uses) > 1
        duplicate_results = len(matching_results) > 1
        for use in matching_uses:
            if duplicate_uses:
                use["statuses"].append("duplicate_tool_use_id")
            if not matching_results:
                use["statuses"].append("missing_result")
            elif duplicate_uses or duplicate_results:
                use["statuses"].append("ambiguous_pairing")
            else:
                use["statuses"].append("paired")
            if duplicate_results:
                use["statuses"].append("duplicate_tool_result_id")
            if denial_lines:
                use["statuses"].append("permission_denied")
                use["permission_denial_lines"] = denial_lines
            for result in matching_results:
                for result_status in result["statuses"]:
                    if result_status not in use["statuses"]:
                        use["statuses"].append(result_status)
            use["result_events"] = [
                {
                    "line_number": result["line_number"],
                    "block_index": result["block_index"],
                    "result": result["result"],
                    "is_error": result["is_error"],
                    "statuses": result["statuses"],
                }
                for result in matching_results
            ]

    unmatched_results = [
        {
            "line_number": result["line_number"],
            "block_index": result["block_index"],
            "tool_use_id": None,
            "result": result["result"],
            "is_error": result["is_error"],
            "statuses": [*result["statuses"], "unmatched_tool_result"],
        }
        for result in results if result["tool_use_id"] is None
    ]
    for tool_use_id, matching_results in results_by_id.items():
        if tool_use_id not in uses_by_id:
            unmatched_results.extend({
                "line_number": result["line_number"],
                "block_index": result["block_index"],
                "tool_use_id": tool_use_id,
                "result": result["result"],
                "is_error": result["is_error"],
                "statuses": [*result["statuses"], "orphan_tool_result"]
                    + (["duplicate_tool_result_id"] if len(matching_results) > 1 else []),
            } for result in matching_results)
    unmatched_denials = [
        {"line_number": denial["line_number"], "tool_use_id": denial["tool_use_id"]}
        for denial in denials
        if denial["tool_use_id"] is not None and denial["tool_use_id"] not in uses_by_id
    ]

    pairing_counts = {
        "paired": sum("paired" in use["statuses"] for use in uses),
        "missing_result": sum("missing_result" in use["statuses"] for use in uses),
        "ambiguous_pairing": sum("ambiguous_pairing" in use["statuses"] for use in uses),
    }
    flag_counts = {
        "permission_denied_tool_uses": sum("permission_denied" in use["statuses"] for use in uses),
        "tool_error_results": sum("tool_error" in result["statuses"] for result in results),
        "duplicate_tool_use_ids": sum(len(group) > 1 for group in uses_by_id.values()),
        "duplicate_tool_result_ids": sum(len(group) > 1 for group in results_by_id.values()),
    }

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "fingerprint_format": "UTF-8 of Python json.dumps(sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False); normalized_json_chars counts Unicode code points.",
        "scope": "Observed Claude Code stream-json event envelopes only; this index does not establish command truth, source support, authorization, or skill quality.",
        "trace": {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "line_count": len(lines),
        },
        "init_events": init_events,
        "tool_uses": uses,
        "unmatched_tool_results": unmatched_results,
        "unmatched_permission_denials": unmatched_denials,
        "malformed_lines": malformed_lines,
        "malformed_events": malformed_events,
        "counts": {
            "init_events": len(init_events),
            "tool_use_events": len(uses),
            "tool_result_events": len(results),
            "unique_pairs": pairing_counts["paired"],
            "missing_results": pairing_counts["missing_result"],
            "ambiguous_pairings": pairing_counts["ambiguous_pairing"],
            "orphan_tool_results": sum(
                "orphan_tool_result" in result["statuses"] for result in unmatched_results
            ),
            "unmatched_tool_results": len(unmatched_results),
            "permission_denial_events": len(denials),
            "permission_denied_tool_uses": flag_counts["permission_denied_tool_uses"],
            "tool_error_results": flag_counts["tool_error_results"],
            "duplicate_tool_use_ids": flag_counts["duplicate_tool_use_ids"],
            "duplicate_tool_result_ids": flag_counts["duplicate_tool_result_ids"],
            "malformed_lines": len(malformed_lines),
            "malformed_events": len(malformed_events),
            "unmatched_permission_denials": len(unmatched_denials),
        },
    }


def write_new_json(output: Path, report: dict[str, Any]) -> None:
    serialized = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(serialized)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Index Claude Code stream-json tool-use/result events without copying private payloads.")
    parser.add_argument("--input", required=True, type=Path, help="Existing Claude Code stream-json JSONL trace")
    parser.add_argument("--output", required=True, type=Path, help="New JSON index file in an existing directory")
    args = parser.parse_args(argv)

    try:
        source = args.input.resolve(strict=True)
        output = args.output.resolve(strict=False)
        if args.output.is_symlink():
            raise ValueError("output must not be a symlink")
        if not source.is_file():
            raise ValueError("input must be a regular file")
        if source == output:
            raise ValueError("input and output must be different files")
        if not output.parent.is_dir():
            raise ValueError("output parent directory must already exist")
        if output.exists():
            raise FileExistsError

        report = index_bytes(source.read_bytes())
        write_new_json(output, report)
    except FileExistsError:
        print("Output already exists; it was not overwritten.", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        # Do not echo paths or exception details that may include private data.
        print(f"trace_index failed: {type(error).__name__}", file=sys.stderr)
        return 2

    print(json.dumps(report["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
