#!/usr/bin/env python3
"""Replay the five frozen parent audits once each in an isolated exact layout."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sources = json.loads((packet / "source-manifest.json").read_text())
    dependencies = json.loads((packet / "dependency-manifest.json").read_text())
    source_by_name = {Path(item["path"]).name: item for item in sources}
    for item in sources:
        assert sha(packet / "original" / item["path"]) == item["sha256"]
    for item in dependencies:
        assert sha(packet / "dependencies-original" / item["path"]) == item["sha256"]
    names = [
        "audit_deletion_contract",
        "audit_uniform_bank_domain",
        "audit_uniform_price_rows",
        "audit_price_lower_cuts",
        "audit_signed_repair",
    ]
    events = []
    with tempfile.TemporaryDirectory(prefix="isolated-runtime-", dir=out) as td:
        runtime = Path(td)
        shutil.copytree(packet / "original", runtime, dirs_exist_ok=True)
        shutil.copytree(packet / "dependencies-original", runtime, dirs_exist_ok=True)
        for name in names:
            source = source_by_name[name + ".py"]
            expected = source_by_name[name + ".json"]
            entry = runtime / source["path"]
            generated = runtime / expected["path"]
            generated.unlink()
            run_dir = out / name
            run_dir.mkdir()
            started = datetime.now(timezone.utc).isoformat()
            tic = time.perf_counter()
            result = subprocess.run(
                [sys.executable, "-B", str(entry)], cwd=runtime,
                capture_output=True, timeout=300, check=False,
            )
            elapsed = time.perf_counter() - tic
            (run_dir / "stdout.txt").write_bytes(result.stdout)
            (run_dir / "stderr.txt").write_bytes(result.stderr)
            if generated.exists():
                shutil.copyfile(generated, run_dir / "report.json")
            event = {
                "execution_type": "unmodified_original_main",
                "original_main_invocations": 1,
                "source_id": source["id"],
                "source_path": source["path"],
                "source_sha256": source["sha256"],
                "expected_report_source_id": expected["id"],
                "expected_report_sha256": expected["sha256"],
                "started_utc": started,
                "elapsed_seconds": elapsed,
                "exit_code": result.returncode,
                "python": sys.version,
                "platform": platform.platform(),
                "command_relative_to_isolated_root": ["python", "-B", source["path"]],
                "stdout_bytes": len(result.stdout),
                "stderr_bytes": len(result.stderr),
                "generated_report_sha256": sha(generated) if generated.exists() else None,
                "generated_report_bytes": generated.stat().st_size if generated.exists() else None,
                "byte_equal_to_frozen_report": generated.exists() and generated.read_bytes() == (packet / "original" / expected["path"]).read_bytes(),
                "fresh_independent_math_verifier_invocations": 0,
                "full_strategy_certificate_verifier_invocations": 0,
                "lp_solver_invocations": 0,
                "random_search_invocations": 0,
            }
            (run_dir / "event.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
            events.append(event)
            print(json.dumps({k: event[k] for k in ("source_id", "elapsed_seconds", "exit_code", "generated_report_bytes", "byte_equal_to_frozen_report")}), flush=True)
            assert result.returncode == 0, (name, result.stderr.decode(errors="replace"))
            assert event["byte_equal_to_frozen_report"], name
            assert json.loads(generated.read_text())["all_checks_passed"] is True
    summary = {
        "scope": "Five original finite audits replayed once each; no general theorem or seed-existence proof is supplied by these executions.",
        "original_main_invocations": 5,
        "generated_reports_byte_equal": 5,
        "new_independent_math_program_invocations": 0,
        "events": [{k: e[k] for k in ("source_id", "elapsed_seconds", "exit_code", "generated_report_sha256", "byte_equal_to_frozen_report")} for e in events],
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
