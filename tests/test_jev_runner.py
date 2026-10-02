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

    def test_existing_report_is_preserved_and_prevents_all_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            output.write_text("existing report", encoding="utf-8")
            with self.assertRaises(SystemExit):
                self.run_with(directory, output,
                              lambda *_args, **_kwargs: self.fail("Called model before output validation"),
                              ("--live", "--probe-latest"))
            self.assertEqual(output.read_text(encoding="utf-8"), "existing report")

    def test_failed_probe_is_reported_even_when_cases_succeed(self):
        def evaluate(_card, **options):
            if options.get("model") == "jev-latest":
                return {"status": "requires_review", "source": "local", "answer": None,
                        "requested_model": "jev-latest", "model": None,
                        "request_attempted": True}
            return {"status": "advisory", "source": "jev", "answer": {"choice": "supported"},
                    "requested_model": "jev-1.13.0", "model": "jev-1.13.0",
                    "request_attempted": True, "latency_ms": 1,
                    "usage": {"input_tokens": 10}}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, calls = self.run_with(directory, output, evaluate, ("--live", "--probe-latest"))
            report = json.loads(output.read_text(encoding="utf-8"))
            probe_call = next(call for call in calls.call_args_list
                              if call.kwargs.get("model") == "jev-latest")
            self.assertEqual(code, 1)
            self.assertEqual(calls.call_count, 2)
            self.assertTrue(probe_call.kwargs["live"])
            self.assertEqual(report["summary"]["errors"], 0)
            self.assertEqual(report["summary"]["probe_status"], "failed")
            self.assertTrue(report["summary"]["probe_error"])
            self.assertEqual(report["latest_probe"]["mode"], "live")
            self.assertTrue(report["latest_probe"]["request_attempted"])
            self.assertIsNone(report["latest_probe"]["resolved_model"])

    def test_preview_probe_is_not_run_and_never_requests_live(self):
        def evaluate(_card, **options):
            self.assertFalse(options["live"])
            return {"status": "preview", "source": "local", "answer": None,
                    "requested_model": options.get("model", "jev-1.13.0"),
                    "model": None, "request_attempted": False,
                    "payload": {"preview_only": True}, "latency_ms": None,
                    "usage": {"input_tokens": None}}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, calls = self.run_with(directory, output, evaluate, ("--probe-latest",))
            report = json.loads(output.read_text(encoding="utf-8"))
            probe_call = next(call for call in calls.call_args_list
                              if call.kwargs.get("model") == "jev-latest")
            self.assertEqual(code, 0)
            self.assertEqual(calls.call_count, 2)
            self.assertFalse(probe_call.kwargs["live"])
            self.assertEqual(report["latest_probe"]["mode"], "preview")
            self.assertEqual(report["latest_probe"]["status"], "preview")
            self.assertEqual(report["latest_probe"]["probe_status"], "not_run")
            self.assertFalse(report["latest_probe"]["request_attempted"])
            self.assertEqual(report["latest_probe"]["requested_model"], "jev-latest")
            self.assertIsNone(report["latest_probe"]["resolved_model"])
            self.assertEqual(report["summary"]["probe_status"], "not_run")
            self.assertIsNone(report["summary"]["probe_error"])

    def test_live_probe_records_requested_alias_and_resolved_model(self):
        def evaluate(_card, **options):
            if options.get("model") == "jev-latest":
                return {"status": "advisory", "source": "jev",
                        "answer": {"choice": "supported"},
                        "requested_model": "jev-latest", "model": "jev-1.14.0",
                        "request_attempted": True}
            return {"status": "advisory", "source": "jev",
                    "answer": {"choice": "supported"},
                    "requested_model": "jev-1.13.0", "model": "jev-1.13.0",
                    "request_attempted": True, "latency_ms": 1,
                    "usage": {"input_tokens": 10}}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, calls = self.run_with(directory, output, evaluate, ("--live", "--probe-latest"))
            report = json.loads(output.read_text(encoding="utf-8"))
            probe = report["latest_probe"]
            probe_call = next(call for call in calls.call_args_list
                              if call.kwargs.get("model") == "jev-latest")
            self.assertEqual(code, 0)
            self.assertTrue(probe_call.kwargs["live"])
            self.assertEqual(report["summary"]["probe_status"], "resolved")
            self.assertFalse(report["summary"]["probe_error"])
            self.assertEqual(probe["probe_status"], "resolved")
            self.assertTrue(probe["request_attempted"])
            self.assertEqual(probe["requested_model"], "jev-latest")
            self.assertEqual(probe["resolved_model"], "jev-1.14.0")

    def test_invalid_response_model_is_preserved_but_not_marked_resolved(self):
        def evaluate(_card, **options):
            if options.get("model") == "jev-latest":
                return {"status": "requires_review", "source": "local",
                        "reason": "invalid_response", "answer": None,
                        "requested_model": "jev-latest", "model": "jev-1.14.0",
                        "request_attempted": True}
            return {"status": "advisory", "source": "jev",
                    "answer": {"choice": "supported"},
                    "requested_model": "jev-1.13.0", "model": "jev-1.13.0",
                    "request_attempted": True, "latency_ms": 1,
                    "usage": {"input_tokens": 10}}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            code, calls = self.run_with(directory, output, evaluate, ("--live", "--probe-latest"))
            report = json.loads(output.read_text(encoding="utf-8"))
            probe = report["latest_probe"]
            probe_call = next(call for call in calls.call_args_list
                              if call.kwargs.get("model") == "jev-latest")
            self.assertEqual(code, 1)
            self.assertTrue(probe_call.kwargs["live"])
            self.assertTrue(probe["request_attempted"])
            self.assertEqual(probe["probe_status"], "failed")
            self.assertEqual(probe["model"], "jev-1.14.0")
            self.assertIsNone(probe["resolved_model"])
            self.assertEqual(report["summary"]["probe_status"], "failed")
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
