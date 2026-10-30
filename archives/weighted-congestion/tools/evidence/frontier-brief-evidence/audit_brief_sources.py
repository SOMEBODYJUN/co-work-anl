"""Exact source-map data audit; does not execute any mathematical proof program."""
from pathlib import Path
import hashlib
import json
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


root = Path(__file__).resolve().parent
source_manifest = json.loads((root / "source-manifest.json").read_text())
for row in source_manifest["sources"]:
    data = (root / row["preserved_path"]).read_bytes()
    require(len(data) == row["size"], row["id"] + " size")
    require(hashlib.sha256(data).hexdigest() == row["sha256"], row["id"] + " hash")
mapping_path = root / "original/research/weighted_congestion_frontier/PRO_BRIEF_SOURCES.json"
mapping = json.loads(mapping_path.read_text())
brief_data = (root / "original" / mapping["brief_source"]).read_bytes()
brief = brief_data.decode()
inventory = json.loads((root / "dependency-inventory.json").read_text())
labels = [row["id"] for row in mapping["sources"]]
expected_labels = [f"S{i}" for i in range(21)]
require(labels == expected_labels, "S0 through S20 exactly once")
definitions = re.findall(r"^\[(S\d+)\]:\s+(\S+)\s*$", brief, re.M)
require([row[0] for row in definitions] == labels, "reference definition labels/order")
definitions = dict(definitions)
math_commit = mapping["brief_mathematical_source_commit"]
claim_ids = []
records = []
all_source_paths = set()
all_review_paths = set()
for row in mapping["sources"]:
    source_paths = [item["path"] for item in row["source_files"]]
    all_source_paths.update(source_paths)
    all_review_paths.update(row["review_paths"])
    claim_ids.extend(row["claim_ids"])
    prefix = mapping["source_repository"] + "/blob/" + math_commit + "/"
    require(definitions[row["id"]].startswith(prefix), row["id"] + " URL commit")
    reference_path = definitions[row["id"]][len(prefix):]
    require(reference_path in source_paths, row["id"] + " reference destination")
    candidates = []
    for path in source_paths + row["review_paths"]:
        matches = [item for item in inventory if item["path"] == path]
        require(matches, row["id"] + " missing metadata: " + path)
        candidates.append({
            "path": path,
            "current_frozen_inventory_versions": [
                {"id": item["id"], "sha256": item["sha256"], "bytes": item["size"],
                 "source_locations": item["sources"]} for item in matches],
            "historical_d549_bytes_retrieved_or_verified_by_this_audit": False,
        })
    records.append({
        "id": row["id"], "brief_sections": row["brief_sections"],
        "source_files": row["source_files"], "claim_ids": row["claim_ids"],
        "review_paths": row["review_paths"], "reference_url": definitions[row["id"]],
        "optional_path": row.get("optional_path"),
        "scope_note": row.get("scope_note"),
        "references_without_ledger_entry": row.get("claim_references_without_review_ledger_entry", []),
        "metadata_matches": candidates,
    })
require(len(claim_ids) == len(set(claim_ids)) == 38, "38 distinct scope Claim IDs")
optional_paths = [row["optional_path"] for row in mapping["sources"] if "optional_path" in row]
require(len(optional_paths) == len(set(optional_paths)) == 19, "19 unique optional destinations")
require(hashlib.sha256(brief_data).hexdigest() == mapping["reviewed_brief_sha256"],
        "canonical full brief matches reviewed brief hash")
task_versions = [item for item in inventory if item["path"] == mapping["task_source"]]
require(task_versions, "current task metadata")
historical_task_present = any(item["sha256"] == mapping["reviewed_task_source_sha256"]
                              for item in task_versions)
result = {
    "schema": 1,
    "scope": "finite exact data/metadata consistency audit; no mathematical program execution",
    "status": "all data assertions passed",
    "source_files_checked": len(source_manifest["sources"]),
    "source_bytes_checked": sum(row["size"] for row in source_manifest["sources"]),
    "source_labels": labels, "source_labels_count": len(labels),
    "source_file_references": sum(len(row["source_files"]) for row in mapping["sources"]),
    "source_file_unique_paths": len(all_source_paths),
    "review_path_references": sum(len(row["review_paths"]) for row in mapping["sources"]),
    "review_path_unique_count": len(all_review_paths),
    "claim_id_references": len(claim_ids), "claim_ids_unique": len(set(claim_ids)),
    "optional_destinations_count": len(optional_paths), "optional_destinations": optional_paths,
    "brief_storage_source_locations": next(row["sources"] for row in source_manifest["sources"]
                                            if row["id"] == "ff9fc2edcae1cd6fac79"),
    "brief_internal_mathematical_commit": math_commit,
    "canonical_brief_sha256": hashlib.sha256(brief_data).hexdigest(),
    "reviewed_brief_hash_matches": True,
    "historical_task_sha256": mapping["reviewed_task_source_sha256"],
    "current_task_inventory_versions": task_versions,
    "historical_task_hash_found_among_current_task_versions": historical_task_present,
    "task_bytes_read_or_export_task_reconstructed_by_this_audit": False,
    "mapping_contains_actual_export_commit": "export_commit" in mapping or "exported_commit" in mapping,
    "mapping_contains_actual_exported_claim_status_payloads": False,
    "mapping_contains_per_mathematical_source_content_hashes": any(
        "sha256" in item for row in mapping["sources"] for item in row["source_files"]),
    "actual_packet_zip_or_export_verified": False,
    "reference_records": records,
    "limits": [
        "Current inventory metadata does not verify the historical d549 blob bytes.",
        "38 mapped Claim IDs describe selected scopes, not all claims in optional full files.",
        "19 destination names do not prove a 22-file packet was generated or verified.",
        "The reviewed task hash does not authenticate a different current same-path task.",
        "No linked theorem, old review, mathematical audit or external paper is executed/validated by this data audit.",
    ],
}
print(json.dumps(result, ensure_ascii=False, indent=2))
