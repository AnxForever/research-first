"""Evaluation bookkeeping checks; no model calls are made."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("jev_runner", Path(__file__).resolve().parents[1] / "evals/run_jev_cases.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

CARD = {"id": "test", "checkpoint": "evidence", "state": {"claim": "A", "excerpt": "A"}}


class RunnerTests(unittest.TestCase):
    def run_with(self, directory, output, evaluate, extra=()):
        corpus = Path(directory) / "cases.json"
        corpus.write_text(json.dumps({"cases": [{"card": CARD, "expected": "supported"}]}), encoding="utf-8")
        with patch.object(runner.sys, "argv", ["runner", str(corpus), str(output), *extra]), \
             patch.object(runner, "evaluate_card", side_effect=evaluate) as calls, \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = runner.main()
        return result, calls

    def test_invalid_destination_prevents_all_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SystemExit):
                self.run_with(directory, Path(directory) / "absent/report.json",
                              lambda *_args, **_kwargs: self.fail("Called model before output validation"), ("--live",))

    def test_failed_probe_is_reported_even_when_cases_succeed(self):
        def evaluate(_card, **options):
            if options.get("model") == "jev-latest":
                return {"status": "requires_review", "source": "local", "answer": None}
            return {"status": "advisory", "source": "jev", "answer": {"choice": "supported"},
                    "latency_ms": 1, "usage": {"input_tokens": 10}}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, calls = self.run_with(directory, output, evaluate, ("--live", "--probe-latest"))
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 1)
            self.assertEqual(calls.call_count, 2)
            self.assertEqual(report["summary"]["errors"], 0)
            self.assertTrue(report["summary"]["probe_error"])

    def test_default_preview_keeps_zero_completed_and_no_accuracy(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, _ = self.run_with(directory, output, runner.evaluate_card)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(code, 0)
            self.assertEqual(report["mode"], "preview")
            self.assertEqual(report["summary"]["completed"], 0)
            self.assertIsNone(report["rows"][0]["matches_expected"])
            self.assertIsNone(report["summary"]["mean_latency_ms"])


if __name__ == "__main__":
    unittest.main()
