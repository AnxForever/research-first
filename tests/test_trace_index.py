"""Contract tests for the maintainer-only Claude trace index."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "evals" / "discovery" / "trace_index.py"
SPEC = importlib.util.spec_from_file_location("trace_index", SCRIPT)
trace_index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace_index)


def json_line(event: object, ending: bytes = b"\n") -> bytes:
    return json.dumps(event, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + ending


def use_event(tool_use_id: str, name: str, tool_input: object) -> dict:
    return {
        "type": "assistant",
        "message": {"content": [{"type": "tool_use", "id": tool_use_id,
                                   "name": name, "input": tool_input}]},
    }


def result_event(tool_use_id: str, content: object, *, is_error: object = None) -> dict:
    block = {"type": "tool_result", "tool_use_id": tool_use_id, "content": content}
    if is_error is not None:
        block["is_error"] = is_error
    return {"type": "user", "message": {"content": [block]}}


def fixture_bytes() -> bytes:
    events = [
        {"type": "system", "subtype": "init", "model": "private-model-name",
         "tools": ["Bash", "mcp__private.server__secret"], "cwd": "C:\\private\\project",
         "skills": [{"name": "research-first", "body": "private skill body"}]},
        use_event("call-a", "Bash", {"command": "inspect C:\\private\\project\\data.csv",
                                       "description": "private prompt phrase"}),
        use_event("call-b", "mcp__private.server__secret", {"payload": "private input"}),
        {"type": "system", "subtype": "permission_denied", "tool_use_id": "call-b",
         "message": "private denial detail"},
        result_event("call-b", [{"type": "text", "text": "private list result"}], is_error=True),
        result_event("call-a", "private string result"),
        use_event("call-missing", "Read", {"file_path": "C:\\private\\missing.txt"}),
        use_event("call-duplicate", "Grep", {"pattern": "first"}),
        use_event("call-duplicate", "Grep", {"pattern": "second"}),
        result_event("call-duplicate", "first duplicate result"),
        result_event("call-duplicate", "second duplicate result"),
        b'{"type":"assistant", broken json}\n',
        b'{"type":"result","type":"user"}\n',
        result_event("orphan-call", "orphan result"),
    ]
    return b"".join(event if isinstance(event, bytes) else json_line(event) for event in events)


class TraceIndexTests(unittest.TestCase):
    def test_pairs_by_id_across_event_order_and_keeps_result_kinds_and_flags(self):
        report = trace_index.index_bytes(fixture_bytes())
        calls = {call["tool_use_id"]: call for call in report["tool_uses"]}

        self.assertEqual(calls["call-a"]["line_number"], 2)
        self.assertEqual(calls["call-a"]["result_events"][0]["line_number"], 6)
        self.assertEqual(calls["call-a"]["statuses"], ["paired"])
        self.assertEqual(calls["call-b"]["line_number"], 3)
        self.assertEqual(calls["call-b"]["result_events"][0]["line_number"], 5)
        self.assertEqual(calls["call-b"]["result_events"][0]["result"]["normalized_json_chars"],
                         len(json.dumps([{"type": "text", "text": "private list result"}],
                                         sort_keys=True, separators=(",", ":"), ensure_ascii=False)))
        self.assertTrue(calls["call-b"]["result_events"][0]["is_error"])
        self.assertIn("permission_denied", calls["call-b"]["statuses"])
        self.assertIn("tool_error", calls["call-b"]["statuses"])
        self.assertIn("tool_error", calls["call-b"]["result_events"][0]["statuses"])

    def test_missing_duplicate_orphan_and_malformed_records_remain_visible(self):
        report = trace_index.index_bytes(fixture_bytes())
        calls = {call["tool_use_id"]: call for call in report["tool_uses"]}

        self.assertIn("missing_result", calls["call-missing"]["statuses"])
        self.assertIn("duplicate_tool_use_id", calls["call-duplicate"]["statuses"])
        self.assertIn("duplicate_tool_result_id", calls["call-duplicate"]["statuses"])
        self.assertIn("ambiguous_pairing", calls["call-duplicate"]["statuses"])
        self.assertEqual(len(calls["call-duplicate"]["result_events"]), 2)
        self.assertEqual(report["unmatched_tool_results"][0]["tool_use_id"], "orphan-call")
        self.assertEqual(report["malformed_lines"][0]["line_number"], 12)
        self.assertEqual(report["malformed_lines"][0]["kind"], "malformed_json")
        self.assertEqual(report["malformed_lines"][1]["line_number"], 13)
        self.assertEqual(report["malformed_lines"][1]["kind"], "duplicate_json_key")
        self.assertEqual(report["counts"]["ambiguous_pairings"], 2)
        self.assertNotIn("overall_pass", report)

    def test_canonical_hashes_and_default_output_do_not_disclose_payloads(self):
        raw = fixture_bytes()
        report = trace_index.index_bytes(raw)
        call_a = next(call for call in report["tool_uses"] if call["tool_use_id"] == "call-a")
        normalized_input = '{"command":"inspect C:\\\\private\\\\project\\\\data.csv","description":"private prompt phrase"}'
        expected_hash = hashlib.sha256(normalized_input.encode("utf-8")).hexdigest()
        self.assertEqual(call_a["input"]["sha256"], expected_hash)
        string_result = call_a["result_events"][0]["result"]
        expected_result = hashlib.sha256(b'"private string result"').hexdigest()
        self.assertEqual(string_result["sha256"], expected_result)
        self.assertEqual(string_result["normalized_json_chars"], len('"private string result"'))
        self.assertEqual(report["trace"]["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(report["init_events"][0]["tool_inventory"]["item_count"], 2)
        private_call = next(call for call in report["tool_uses"] if call["tool_use_id"] == "call-b")
        self.assertEqual(private_call["tool_label"], "other")

        serialized = json.dumps(report, ensure_ascii=False)
        for private_value in (
            "private-model-name", "mcp__private.server__secret", "C:\\private\\project",
            "private skill body", "private prompt phrase", "private input", "private denial detail",
            "private list result", "private string result",
        ):
            with self.subTest(value=private_value):
                self.assertNotIn(private_value, serialized)

    def test_unpaired_surrogate_isolated_to_malformed_line_and_emoji_pair_is_valid(self):
        bad_line = (
            b'{"type":"assistant","message":{"content":[{"type":"tool_use",'
            b'"id":"bad-call","name":"Read","input":{"file_path":"private-\\ud800"}}]}}\n'
        )
        emoji_use = (
            b'{"type":"assistant","message":{"content":[{"type":"tool_use",'
            b'"id":"emoji-call","name":"Bash","input":{"query":"\\ud83d\\ude00"}}]}}\n'
        )
        raw = bad_line + emoji_use + json_line(result_event("emoji-call", "complete"))

        report = trace_index.index_bytes(raw)

        self.assertEqual(len(report["malformed_lines"]), 1)
        malformed = report["malformed_lines"][0]
        self.assertEqual(malformed["line_number"], 1)
        self.assertEqual(malformed["kind"], "non_utf8_json_value")
        self.assertEqual(malformed["sha256"], hashlib.sha256(bad_line[:-1]).hexdigest())
        self.assertEqual([call["tool_use_id"] for call in report["tool_uses"]], ["emoji-call"])
        emoji_call = report["tool_uses"][0]
        normalized_input = '{"query":"😀"}'
        self.assertEqual(emoji_call["input"]["sha256"], hashlib.sha256(normalized_input.encode("utf-8")).hexdigest())
        self.assertEqual(emoji_call["input"]["normalized_json_chars"], len(normalized_input))
        self.assertEqual(emoji_call["statuses"], ["paired"])
        self.assertNotIn("private-", json.dumps(report, ensure_ascii=False))

    def test_cli_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "trace.jsonl"
            output = root / "index.json"
            source.write_bytes(fixture_bytes())
            output.write_text("keep this report", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                status = trace_index.main(["--input", str(source), "--output", str(output)])

            self.assertEqual(status, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep this report")
            self.assertNotIn(str(source), stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
