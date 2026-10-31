#!/usr/bin/env python3
"""Verify frozen source bytes and the sole historical canonical correction.

This does not implement the scheduling algorithm or test a mathematical bound.
Run from any working directory; the JSON result is written beside this script.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
STAGE_OR_REPO = ROOT.parents[4]
manifest = json.loads((ROOT / "manifest.json").read_text())
checked = []
for role in ("originals", "comparisons"):
    for item in manifest[role]:
        path = STAGE_OR_REPO / item["evidence_path"]
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash != item["sha256"] or len(data) != item["size"]:
            raise AssertionError(item["id"])
        checked.append({"id": item["id"], "role": role,
                        "size": len(data), "sha256": actual_hash,
                        "matches_frozen_inventory": True})

canonical = (ROOT / "comparisons" /
             "affine_line_tuple_groups_global_dummy_compilation_escape.md").read_bytes()
corrected = rb"[n(d+1)+vR^2+d]\cdot n(D+d+1)."
draft = rb"[n(d+1)+vR^2+d],n(D+d+1)."
assert canonical.count(corrected) == 1
assert canonical.count(draft) == 0
restored_hash = hashlib.sha256(canonical.replace(corrected, draft)).hexdigest()
expected_draft_hash = "22c9377c33b1167827d3d89636d91820de94808fe9ded724273f6768bb162f36"
assert restored_hash == expected_draft_hash

result = {
    "scope": "source-byte integrity and in-memory reversal of one typography correction only",
    "mathematical_algorithm_implemented": False,
    "optimization_or_finite_mathematical_experiment_run": False,
    "checked_files": checked,
    "canonical_correction": {
        "replacement_occurrences": 1,
        "final_sha256": hashlib.sha256(canonical).hexdigest(),
        "restored_draft_sha256": restored_hash,
        "matches_historical_draft_sha256": True,
        "original_files_modified": False,
    },
}
(ROOT / "integrity-check.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_files_checked": len(checked),
                  "all_frozen_bytes_match": True,
                  "single_correction_restores_draft_hash": True},
                 ensure_ascii=False))
