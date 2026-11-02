"""Check the two restored primary metadata sources, not their research claims.

All inputs are preserved files in this checkout; no network or research entry
point is run. The report distinguishes historical declarations from this check.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "cleanup/inventory.jsonl").is_file())
EVIDENCE = HERE.parent
DOCUMENT = ROOT / "archives/customer-attraction/state/资源/R5662研究checkpoint的版本清单与有限复核--资源.md"
ids = {
    "3913485fc9b9d5810df5": "checkpoint_manifest.json",
    "c6b117b9e8fd491d2d98": "checkpoint_verification.json",
}
inventory = [json.loads(line) for line in (ROOT / "cleanup/inventory.jsonl").read_text().splitlines()]
by_id = {r["id"]: r for r in inventory}
by_path = defaultdict(list)
for record in inventory:
    by_path[record["path"]].append(record)
sources = {}
for source_id, name in ids.items():
    raw = (EVIDENCE / "original" / name).read_bytes()
    assert len(raw) == by_id[source_id]["size"]
    assert hashlib.sha256(raw).hexdigest() == by_id[source_id]["sha256"]
    sources[source_id] = json.loads(raw)
manifest = sources["3913485fc9b9d5810df5"]
verification = sources["c6b117b9e8fd491d2d98"]
rows = []
for item in manifest["files"]:
    candidates = by_path[item["path"]]
    same = [r["id"] for r in candidates if (r["sha256"], r["size"]) == (item["sha256"], item["bytes"])]
    rows.append({
        "path": item["path"], "manifest_sha256": item["sha256"], "manifest_bytes": item["bytes"],
        "frozen_matching_ids": same, "other_frozen_ids": [r["id"] for r in candidates if r["id"] not in same],
    })
assert rows == json.loads((EVIDENCE / "manifest-inventory-comparison.json").read_text())
doc = DOCUMENT.read_text()
blocks = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", doc, re.S)]
assert blocks[0] == verification
prefix = manifest["files"][0]["path"].rsplit("/", 1)[0] + "/"
actual_table = [(int(i), p, int(n)) for i, p, n in re.findall(r"^\|(\d+)\|`([^`]+)`\|(\d+)\|$", doc, re.M)]
expected_table = [(i, r["path"].removeprefix(prefix), r["manifest_bytes"]) for i, r in enumerate(rows)]
assert actual_table == expected_table
report = {
    "scope": "Restored primary metadata identity, complete manifest comparison and formal transcription only; no research program, full matrix or SPE verification run.",
    "source_fingerprints": [{"id": sid, "sha256": by_id[sid]["sha256"], "bytes": by_id[sid]["size"]} for sid in ids],
    "manifest_entries": len(rows), "distinct_paths": len({r["path"] for r in rows}),
    "matching_versions": sum(bool(r["frozen_matching_ids"]) for r in rows),
    "different_versions": [r for r in rows if not r["frozen_matching_ids"]],
    "declared_total_bytes": sum(r["manifest_bytes"] for r in rows),
    "snapshot_commit": manifest["snapshot_commit"],
    "formal_manifest_table_exact": True, "formal_verification_json_exact": True,
    "historical_check_count": len(verification["checks"]),
    "historical_main_target": verification["main_target"],
    "members_not_reviewed_by_this_check": True,
    "historical_runs_not_repeated_or_reconstructed": True,
}
assert report["manifest_entries"] == 174 and report["matching_versions"] == 172
(HERE / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "different_versions"}, ensure_ascii=False))
