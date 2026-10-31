#!/usr/bin/env python3
"""Check preserved source bytes and saved runs, never launch a mathematical program."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
STAGE_OR_REPO = ROOT.parents[4]
manifest = json.loads((ROOT / "manifest.json").read_text())
checks = []
for role in ("originals", "comparisons", "derived_page_snapshots"):
    for item in manifest[role]:
        raw = (STAGE_OR_REPO / item["evidence_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        assert len(raw) == item["size"]
        checks.append({"role": role, "id": item.get("id"),
                       "path": item["evidence_path"], "sha256": item["sha256"], "matches": True})
old = (ROOT / "comparisons/cotransversal_uniform_configuration_gap_audit.json").read_bytes()
new = (ROOT / "runs/gap-001/result.json").read_bytes()
assert old == new
review = (ROOT / "original/symmetric_moment_reset_review.md").read_text()
inline = review.split("```python\n", 1)[1].split("\n```", 1)[0] + "\n"
assert inline == (ROOT / "derived/nonsymmetric_five_literal_check.py").read_text()
runs = []
for label in ("gap", "nonsymmetric_inline"):
    run = ROOT / "runs" / (label + "-001")
    metadata = json.loads((run / "run.json").read_text())
    assert metadata["exit_code"] == 0 and metadata["python_optimization_level"] == 0
    assert metadata["entry_point_runs_in_this_batch"] == 1
    assert (run / "stdout.txt").stat().st_size == (run / "stderr.txt").stat().st_size == 0
    runs.append({"label": label, "exit_code": 0, "stdout_stderr_empty": True,
                 "runs_recorded": 1, "assertions_enabled": True})
byte_checks = json.loads((ROOT / "version-byte-checks.json").read_text())
assert byte_checks["one_ascii_space_before_line_310_LF_recovers_old_hash"]
assert byte_checks["unexpected_ascii_controls_except_LF"] == []
result = {"source_and_snapshot_checks": checks, "new_finite_runs": runs,
          "gap_result_byte_identical_frozen": True,
          "gap_result_sha256": hashlib.sha256(new).hexdigest(),
          "inline_extraction_exact": True, "version_byte_checks": byte_checks,
          "previous_reset_entry_points_reexecuted": False,
          "old_Boss2_pages_overwritten": False,
          "mathematical_programs_launched_by_this_verifier": False}
(ROOT / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_sources_checked": len(checks) - 2, "old_page_snapshots_checked": 2,
                  "successful_new_finite_runs": 2, "gap_result_byte_identical": True,
                  "previous_reset_runs": 0}, ensure_ascii=False))
