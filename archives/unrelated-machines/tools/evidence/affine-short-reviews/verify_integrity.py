#!/usr/bin/env python3
"""Verify source identities and review hash tables, not mathematical bounds."""
from pathlib import Path
import argparse
import hashlib
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("--existing-root", type=Path,
                    help="Fallback repository root while running from external staging")
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
PRIMARY_ROOT = ROOT.parents[4]
manifest = json.loads((ROOT / "manifest.json").read_text())
records = {}
checked = []
paths = {}
for role in ("originals", "comparisons", "existing_evidence_dependencies"):
    for item in manifest[role]:
        path = PRIMARY_ROOT / item["evidence_path"]
        if not path.is_file() and args.existing_root is not None:
            path = args.existing_root / item["evidence_path"]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert len(data) == item["size"] and digest == item["sha256"], item["id"]
        records[Path(item["path"]).name] = item
        paths[item["id"]] = path
        checked.append({"id": item["id"], "role": role,
                        "size": len(data), "sha256": digest, "matches": True})

table_checks = []
pattern = re.compile(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|")
for source_id in ("b897a118ab937abf10e6", "0af7d2ee776f315372e3", "9320ff95c0dd4dcbfd90"):
    source_text = paths[source_id].read_text()
    rows = pattern.findall(source_text)
    assert rows, source_id
    for original_path, expected in rows:
        item = records[Path(original_path).name]
        assert expected == item["sha256"], original_path
        table_checks.append({"review_id": source_id, "referenced_id": item["id"],
                             "sha256": expected, "matches_preserved_source": True})
assert len(table_checks) == 17

bindings = []
for review_id, canonical_id in (("b897a118ab937abf10e6", "5181ee7a09c56933cfcd"),
                                ("0af7d2ee776f315372e3", "014d2e9f589349d24a86"),
                                ("9320ff95c0dd4dcbfd90", "cc3fc3849a2e96e053fb")):
    digest = hashlib.sha256(paths[canonical_id].read_bytes()).hexdigest()
    assert digest in paths[review_id].read_text()
    bindings.append({"review_id": review_id, "canonical_id": canonical_id,
                     "sha256": digest, "binding_matches": True})

result = {
    "scope": "source-byte identities, 17 original-hash table entries, and three final canonical bindings only",
    "checked_files": checked,
    "original_hash_table_checks": table_checks,
    "final_canonical_bindings": bindings,
    "old_c50_canonical_reverse_replacement_reexecuted": False,
    "mathematical_algorithm_implemented": False,
    "optimization_or_finite_mathematical_experiment_run": False,
    "original_files_modified": False,
}
(ROOT / "integrity-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_files_checked": len(checked), "hash_table_entries_checked": len(table_checks),
                  "canonical_bindings_checked": len(bindings), "all_match": True}, ensure_ascii=False))
