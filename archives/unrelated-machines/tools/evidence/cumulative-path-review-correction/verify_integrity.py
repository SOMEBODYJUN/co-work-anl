#!/usr/bin/env python3
"""Preserve frozen source identities and the literal 30-row table; no arithmetic audit."""
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
known, paths, checks = {}, {}, []
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

references = []
for item in manifest["originals"]:
    for digest in re.findall(r"\b[0-9a-f]{64}\b", paths[item["id"]].read_text()):
        assert digest in known, (item["id"], digest)
        references.append({"source_id": item["id"], "referenced_sha256": digest,
                           "referenced_id": known[digest], "matches_preserved_bytes": True})

source_text = paths["61c1ab239178da3fd94a"].read_text()
start = source_text.index("| 原 job |")
end = source_text.index("\n\n9 selectors", start)
literal = source_text[start:end]
page = PRIMARY_ROOT / "archives/unrelated-machines/state/审查/累计路径反例的误标签纠正与陈述先行全任务证书--审查.md"
page_text = page.read_text()
preserved = page_text.split("<!-- literal-30-job-table:start -->\n", 1)[1].split(
    "\n<!-- literal-30-job-table:end -->", 1)[0]
assert preserved == literal
assert len(literal.splitlines()) - 2 == 30

result = {
    "scope": "source bytes, named SHA routing and exact literal schedule-table transcription only",
    "checked_files": checks,
    "primary_source_hash_references": references,
    "literal_schedule_table": {"source_id": "61c1ab239178da3fd94a",
                               "data_rows": 30, "exact_text_match": True,
                               "schedule_arithmetic_recomputed": False},
    "old_proof_aware_review_accepted_as_statement_first": False,
    "original_audit_program_reexecuted": False,
    "finite_mathematical_experiments_run": False,
    "original_files_modified": False,
}
(ROOT / "integrity-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"frozen_files_checked": len(checks),
                  "named_hash_occurrences_verified": len(references),
                  "literal_schedule_rows_preserved": 30, "all_match": True}, ensure_ascii=False))
