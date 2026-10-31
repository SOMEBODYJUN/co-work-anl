#!/usr/bin/env python3
"""Verify frozen bytes and saved replay results; never rerun a mathematical entry point."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
REPO_OR_STAGE = ROOT.parents[4]
manifest = json.loads((ROOT / "manifest.json").read_text())
checks = []
for role in ("originals", "comparisons"):
    for item in manifest[role]:
        data = (REPO_OR_STAGE / item["evidence_path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == item["sha256"] and len(data) == item["size"], item["id"]
        checks.append({"id": item["id"], "size": len(data), "sha256": digest, "matches": True})
old = json.loads((ROOT / "comparisons/uniform_random_moment_reset_audit.json").read_text())
replays = []
for label, frozen in zip(("main", "independent"), old["commands"]):
    run = ROOT / "runs" / (label + "-001")
    metadata = json.loads((run / "run.json").read_text())
    raw = (run / "stdout.json").read_bytes()
    output = json.loads(raw)
    assert output == frozen["result"]
    assert metadata["exit_code"] == 0 and metadata["stderr_bytes"] == 0
    assert (run / "stderr.txt").stat().st_size == 0
    assert metadata["runs_of_this_entry_point_in_this_batch"] == 1
    assert hashlib.sha256(raw).hexdigest() == metadata["stdout_sha256"]
    assert output["source_sha256"] == metadata["source_sha256"]
    replays.append({"program": label, "exit_code": 0, "stderr_bytes": 0,
                    "all_output_fields_equal_frozen": True,
                    "source_hash_matches": True, "entry_point_runs_recorded": 1})
hash_refs = json.loads((ROOT / "historical-hash-references.json").read_text())
result = {"frozen_files": checks, "replay_results": replays,
          "primary_named_sha_occurrences": len(hash_refs),
          "historical_sha_without_inventory_record": sum(x["inventory_id"] is None for x in hash_refs),
          "mathematical_entry_points_reexecuted_by_this_verifier": False,
          "scope": "Saved source/output identity checks only; the two actual entry point runs are separately recorded."}
(ROOT / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_files_match": len(checks), "successful_replays": len(replays),
                  "all_output_fields_match": True,
                  "historical_unmaterialized_sha": result["historical_sha_without_inventory_record"]}, ensure_ascii=False))
