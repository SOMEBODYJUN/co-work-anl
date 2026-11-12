"""Run the frozen read-only 4433-byte independent entry once for this packet.

Only this packet receives outputs. The child reads the complete old input;
it does not run the 3889 verifier, author's 6952B program, LP, or SPE solver.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT / "archives/customer-attraction/tools/evidence/frechet-fixed-reply-marginal-separation-primary"
SOURCE_ROOT = BASE / "source-root"
ENTRY = SOURCE_ROOT / "research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/independent_zz_bound.py"
INPUT = SOURCE_ROOT / "research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json"
REPORT = SOURCE_ROOT / "research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/zz_bound_exact.json"
EXPECTED_ENTRY_SHA = "4f5c2a58d43e2d7945291a84a0ed8bb75aa4217db635deebad981f26aa65e622"
EXPECTED_INPUT_SHA = "cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1"


def fingerprint(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(raw),
            "sha256": sha256(raw).hexdigest()}


def main():
    stdout_path = HERE / "frechet-independent-stdout.json"
    metadata_path = HERE / "frechet-replay.json"
    assert not stdout_path.exists() and not metadata_path.exists(), "Do not rerun an already saved event"
    before = [fingerprint(ENTRY), fingerprint(INPUT)]
    assert before[0]["sha256"] == EXPECTED_ENTRY_SHA and before[0]["bytes"] == 4433
    assert before[1]["sha256"] == EXPECTED_INPUT_SHA and before[1]["bytes"] == 816498
    argv = [sys.executable, "-I", "-B", str(ENTRY)]
    started = datetime.now(timezone.utc).isoformat()
    clock = perf_counter()
    completed = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=60, check=False)
    elapsed = perf_counter() - clock
    ended = datetime.now(timezone.utc).isoformat()
    stdout_path.write_bytes(completed.stdout)
    after = [fingerprint(ENTRY), fingerprint(INPUT)]
    assert after == before
    parsed = json.loads(completed.stdout)
    prior_stdout = json.loads((BASE / "stdout.json").read_bytes())
    saved_report = json.loads(REPORT.read_bytes())
    report_bound = saved_report["unrestricted_pairwise_upper_bounds"]["minimum_upper_bound"]
    assert completed.returncode == 0 and not completed.stderr
    assert parsed == prior_stdout
    assert parsed["unrestricted_joint_upper_bound"] == report_bound
    assert parsed["source_sha256"] == EXPECTED_INPUT_SHA
    assert parsed["histograms"] == 16 and parsed["labelled_comparisons"] == 1920
    assert parsed["nonzero_histogram_contributions"] == 7 and parsed["strictly_negative"]
    metadata = {
        "scope": "One current execution of the frozen read-only independent strongest-class calculation; its complete 816498B input was read and parsed by that entry; no 3889/LP/author-program/full-SPE/half execution",
        "started_utc": started, "ended_utc": ended,
        "argv": argv, "cwd": str(ROOT), "elapsed_seconds": elapsed,
        "exit_code": completed.returncode, "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr), "stderr": completed.stderr.decode(),
        "before": before, "after": after, "unchanged": after == before,
        "stdout": fingerprint(stdout_path),
        "frozen_report": fingerprint(REPORT),
        "prior_stdout": fingerprint(BASE / "stdout.json"),
        "matches_prior_stdout_semantics": parsed == prior_stdout,
        "matches_frozen_report_bound": parsed["unrestricted_joint_upper_bound"] == report_bound,
        "matches_parent_diagnostic_semantics": "The child's flag compares its embedded expected fraction; the outer wrapper separately compares the frozen saved report and stdout",
        "not_executed": ["old 3889 verifier", "LP", "author 6952B program", "all 60 classes", "complete SPE", "half proof"],
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"exit_code": completed.returncode, "input_bytes": before[1]["bytes"],
                      "histograms": parsed["histograms"], "comparisons": parsed["labelled_comparisons"],
                      "strictly_negative": parsed["strictly_negative"],
                      "metadata": str(metadata_path.relative_to(ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
