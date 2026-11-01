"""One unmodified original invocation; record bytes, hashes, and exact stdout contract.

This runner does not import or reimplement the enumerated mathematical identity.
The original module has top-level effects, so the single subprocess is its only run.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    event_path = out / "execution.json"
    if event_path.exists():
        raise SystemExit("Existing event: do not silently duplicate the original entry")
    expected_sha = "f5f11fe5eb3627e527900b40d3320e1bb0a13484c7eff65e442da1bf4175a403"
    before = sha(source)
    assert before == expected_sha
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    argv = [sys.executable, "-B", str(source)]
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    proc = subprocess.run(argv, cwd=out, env=env, capture_output=True, check=False)
    elapsed = time.monotonic() - tick
    (out / "stdout.txt").write_bytes(proc.stdout)
    (out / "stderr.txt").write_bytes(proc.stderr)
    after = sha(source)
    parsed = ast.literal_eval(proc.stdout.decode("utf-8")) if proc.returncode == 0 else None
    expected = {
        "states": 40,
        "identity": "tail r1 alpha=gamma=1 Q=actual B equals actual strong PAIR(forced Z,B)",
        "exact": True,
    }
    event = {
        "schema": "one-original-entry-v1",
        "source_id": "99fc07ef9726df36da2b",
        "started_utc": started,
        "elapsed_seconds": elapsed,
        "argv": argv,
        "cwd": str(out),
        "python_version": sys.version,
        "pythonoptimize_removed_for_child": True,
        "assertions_enabled_in_child": True,
        "source_path": str(source),
        "source_bytes": source.stat().st_size,
        "source_sha256_before": before,
        "source_sha256_after": after,
        "source_unchanged": before == after,
        "original_invocations_in_this_event": 1,
        "returncode": proc.returncode,
        "stdout_bytes": len(proc.stdout),
        "stdout_sha256": sha(out / "stdout.txt"),
        "stderr_bytes": len(proc.stderr),
        "stderr_sha256": sha(out / "stderr.txt"),
        "stdout_format": "Python dict repr, parsed with ast.literal_eval; not JSON",
        "parsed_stdout": parsed,
        "matches_reviewed_output_contract": parsed == expected,
        "scope": "The original 40 local coefficient assertions only; no external inputs, whole-game solver, LP, or other entrypoint.",
    }
    event_path.write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    assert proc.returncode == 0 and not proc.stderr and before == after
    assert parsed == expected
    print(json.dumps({"status": "PASS", "source_bytes": source.stat().st_size, "states": parsed["states"], "original_invocations": 1}))


if __name__ == "__main__":
    main()
