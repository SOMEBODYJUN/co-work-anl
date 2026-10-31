#!/usr/bin/env python3
"""Verify source identities and declared hash references, without running audits."""
from pathlib import Path
import argparse
import hashlib
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("--existing-root", type=Path)
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
PRIMARY_ROOT = ROOT.parents[4]
manifest = json.loads((ROOT / "manifest.json").read_text())
known = {}
paths = {}
checks = []
for role in ("originals", "comparisons", "existing_evidence_dependencies"):
    for item in manifest[role]:
        path = PRIMARY_ROOT / item["evidence_path"]
        if not path.is_file() and args.existing_root is not None:
            path = args.existing_root / item["evidence_path"]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == item["sha256"] and len(data) == item["size"], item["id"]
        known[digest] = item["id"]
        paths[item["id"]] = path
        checks.append({"id": item["id"], "role": role, "size": len(data),
                       "sha256": digest, "matches_frozen_inventory": True})

unmaterialized = {x["sha256"] for x in manifest["unmaterialized_historical_hashes"]}
references = []
for item in manifest["originals"]:
    for digest in re.findall(r"\b[0-9a-f]{64}\b", paths[item["id"]].read_text()):
        assert digest in known or digest in unmaterialized, (item["id"], digest)
        references.append({"source_id": item["id"], "referenced_sha256": digest,
                           "referenced_id": known.get(digest),
                           "status": "preserved-source-bytes-match" if digest in known
                           else "historical-c50-hash-only; old-whole-file-not-materialized"})

result = {
    "scope": "source-byte identities and hash-reference routing only",
    "checked_files": checks,
    "primary_source_hash_references": references,
    "old_c50_canonical_obtained": False,
    "old_c50_double_reverse_replacement_reexecuted": False,
    "original_audit_program_reexecuted": False,
    "matching_or_scheduling_algorithm_implemented": False,
    "finite_mathematical_experiments_run": False,
    "original_files_modified": False,
}
(ROOT / "integrity-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_files_checked": len(checks),
                  "named_hash_occurrences_accounted_for": len(references),
                  "preserved_source_hash_occurrences": sum(x["referenced_id"] is not None for x in references),
                  "historical_c50_occurrences": sum(x["referenced_id"] is None for x in references),
                  "all_accounted_for": True}, ensure_ascii=False))
