"""Preview or evaluate the explicit labeled corpus; labels are never sent to Jev."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from jev_check import evaluate_card, validate_card


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("report", type=Path, help="New output file; existing reports are preserved")
    parser.add_argument("--live", action="store_true", help="Send each card once using TYPESAFE_API_KEY")
    parser.add_argument("--probe-latest", action="store_true", help="Also resolve jev-latest with one separate card")
    args = parser.parse_args()
    if args.report.exists():
        parser.error("The report already exists; choose a new output path.")
    raw = args.cases.read_bytes()
    corpus = json.loads(raw)
    cases = corpus["cases"]
    if not 1 <= len(cases) <= 24:
        parser.error("Supply 1-24 cases per run.")
    for item in cases:
        validate_card(item["card"])
    try:
        report_stream = args.report.open("x", encoding="utf-8")
    except OSError:
        parser.error("Cannot create the report. No model calls have been made.")
    # Reserve the destination before any paid request and retain progress as it arrives.
    def persist(value):
        report_stream.seek(0)
        json.dump(value, report_stream, ensure_ascii=False, indent=2)
        report_stream.write("\n")
        report_stream.truncate()
        report_stream.flush()

    progress = {"status": "running", "input_sha256": hashlib.sha256(raw).hexdigest(),
                "latest_probe": None, "rows": []}
    persist(progress)
    probe = None
    if args.probe_latest:
        probe = evaluate_card({
            "id": "latest-version-probe", "checkpoint": "evidence",
            "state": {"claim": "The documentation identifies jev-1.13.0 as the current stable model.",
                      "excerpt": "Current models: Jev 1.13 — jev-1.13.0. jev-latest points to jev-1.13.0, the most recent stable official release."}
        }, live=args.live, model="jev-latest")
        progress["latest_probe"] = probe
        persist(progress)
    rows = []
    for item in cases:
        # Expected labels and evaluation explanations never enter the request.
        result = evaluate_card(item["card"], live=args.live)
        choice = result["answer"]["choice"] if result["answer"] else None
        expected = item.get("expected")
        rows.append({"id": item["card"]["id"], "expected": expected,
                     "matches_expected": None if expected is None or choice is None else choice == expected,
                     "result": result})
        progress["rows"] = rows
        persist(progress)
        print(json.dumps({"id": item["card"]["id"], "choice": choice,
                          "expected": expected, "status": result["status"]}), flush=True)
    completed = [row for row in rows if row["result"]["source"] == "jev"]
    labeled = [row for row in completed if row["expected"] is not None]
    usage = [row["result"]["usage"]["input_tokens"] for row in completed]
    tokens = sum(usage) if usage and all(isinstance(value, int) for value in usage) else None
    report = {
        "status": "complete",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "mode": "live" if args.live else "preview",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "description": corpus.get("description"),
        "method": "One request per card in live mode; labels withheld; no retry or answer override.",
        "latest_probe": probe,
        "summary": {
            "cases": len(cases), "completed": len(completed),
            "errors": sum(row["result"]["status"] == "requires_review" for row in rows),
            "probe_error": bool(probe and probe["status"] == "requires_review"),
            "labeled_completed": len(labeled),
            "matches_expected": sum(row["matches_expected"] for row in labeled),
            "mean_latency_ms": round(statistics.mean(row["result"]["latency_ms"] for row in completed), 1) if completed else None,
            "input_tokens": tokens,
            "estimated_input_usd_excluding_probe": tokens * 0.042 / 1_000_000 if tokens is not None else None,
            "cost_note": "Estimate at the documented 2026-09-22 input rate; verify current pricing, not a provider invoice."
        },
        "rows": rows
    }
    persist(report)
    report_stream.close()
    print(json.dumps(report["summary"]))
    return 1 if report["summary"]["errors"] or report["summary"]["probe_error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
