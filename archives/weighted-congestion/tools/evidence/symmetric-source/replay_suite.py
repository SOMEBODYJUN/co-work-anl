#!/usr/bin/env python3
"""Replay the three unchanged frozen verifiers in isolated output directories.

Only standard-library exact computations are used by the child scripts.
Original source bytes and frozen reports are never modified.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE / "original"
REPLAY = BASE / "replay"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    if not __debug__:
        raise RuntimeError("Run without -O")
    provenance = load(BASE / "provenance.json")
    identities = []
    for source in provenance["sources"]:
        raw = (ORIGINAL / source["path"]).read_bytes()
        digest = sha256(raw).hexdigest()
        assert digest == source["sha256"]
        identities.append({"id": source["id"], "sha256": digest, "size": len(raw)})
    cases = [
        ("topology-author", "tests/audits/weighted_congestion/source_topology/verify.py",
         "evidence/runs/weighted_congestion/source_topology/results.json", "results.json"),
        ("topology-review", "tests/audits/weighted_congestion/source_topology_review/check_review.py",
         "evidence/runs/weighted_congestion/source_topology_review/review_results.json", "review_results.json"),
        ("source32", "tests/audits/weighted_congestion/source_degree32/verify.py",
         "evidence/runs/weighted_congestion/source_degree32/verification.json", None),
    ]
    runs = []
    for name, script, frozen_path, output_name in cases:
        target = REPLAY / name
        target.mkdir(parents=True, exist_ok=True)
        local_script = target / Path(script).name
        shutil.copyfile(ORIGINAL / script, local_script)
        if name == "source32":
            shutil.copyfile(ORIGINAL / "evidence/certificates/weighted_congestion/source_degree32/certificate.json",
                            target / "certificate.json")
        started = time.monotonic_ns()
        command = [sys.executable, str(local_script)]
        result = subprocess.run(command, cwd=target, capture_output=True, text=True, check=False)
        elapsed = (time.monotonic_ns() - started) // 1_000_000
        (target / "stdout.json").write_text(result.stdout, encoding="utf-8")
        (target / "stderr.txt").write_text(result.stderr, encoding="utf-8")
        assert result.returncode == 0, result.stderr
        replay = load(target / output_name) if output_name else json.loads(result.stdout)
        frozen = load(ORIGINAL / frozen_path)
        shared = {key: replay[key] == frozen[key] for key in replay if key in frozen}
        nondeterministic = {"elapsed_milliseconds"}
        assert all(same for key, same in shared.items() if key not in nondeterministic)
        if name != "source32":
            assert replay == frozen
        runs.append({
            "name": name,
            "command": ["python3", str(local_script.relative_to(BASE))],
            "exit_code": result.returncode,
            "wall_milliseconds": elapsed,
            "stdout": str((target / "stdout.json").relative_to(BASE)),
            "report": str((target / output_name).relative_to(BASE)) if output_name else str((target / "stdout.json").relative_to(BASE)),
            "frozen_report": "original/" + frozen_path,
            "shared_field_equalities": shared,
            "frozen_only_fields": sorted(set(frozen) - set(replay)),
            "replay_only_fields": sorted(set(replay) - set(frozen)),
            "mathematical_fields_match": True,
        })
    certificate = load(ORIGINAL / "evidence/certificates/weighted_congestion/source_degree32/certificate.json")
    split = [{"n": row["n"], "k": row["k"], "paths": [leaf["path"] for leaf in row["leaves"]]}
             for row in certificate["records"] if len(row["leaves"]) > 1]
    result = {
        "status": "pass",
        "python": platform.python_version(),
        "python_full": sys.version,
        "source_identities": identities,
        "runs": runs,
        "certificate_summary": certificate["summary"],
        "subdivided_records": split,
        "interpretation": "two finite literal-game suites and a complete finite interval sign certificate after analytic domain reduction; no universal all-game upper claim",
    }
    (BASE / "replay-comparison.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "unchanged_sources": len(identities),
                      "runs": len(runs), "certificate_summary": result["certificate_summary"]}, indent=2))


if __name__ == "__main__":
    main()
