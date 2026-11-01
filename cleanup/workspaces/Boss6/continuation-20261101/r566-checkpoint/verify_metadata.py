"""Read-only metadata, transcription, and scalar checks for three R5662 sources.

Does not import or run historical research programs, reconstruct their matrices,
enumerate potential multisets, or certify an SPE. Writes only beside this file.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from math import comb
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
FROZEN = OUT.parent
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence/r566-checkpoint-metadata-primary"
RESOURCE = ROOT / "archives/customer-attraction/state/资源/R5662研究checkpoint的版本清单与有限复核--资源.md"
SOURCE_NAMES = {
    "3913485fc9b9d5810df5": "checkpoint_manifest.json",
    "c6b117b9e8fd491d2d98": "checkpoint_verification.json",
    "e68ceb56e0eb937c4162": "potential_menu_replay.json",
}


def read_json(path):
    return json.loads(path.read_text())


def fingerprint(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


sources = {x["id"]: x for x in read_json(FROZEN / "sources.json")}
preserved = {x["id"]: x for x in read_json(EVIDENCE / "source-manifest.json")}
inventory = [json.loads(line) for line in (ROOT / "cleanup/inventory.jsonl").read_text().splitlines()]
by_path = defaultdict(list)
for record in inventory:
    by_path[record["path"]].append(record)

source_checks = []
for source_id, name in SOURCE_NAMES.items():
    frozen = FROZEN / f"{source_id}--{name}"
    original = EVIDENCE / "original" / name
    actual = fingerprint(frozen)
    fields = ("id", "blob", "mode", "path", "sha256", "size", "sources")
    source_checks.append({
        "id": source_id,
        "actual": actual,
        "matches_frozen_fingerprint": actual["sha256"] == sources[source_id]["sha256"] and actual["bytes"] == sources[source_id]["size"],
        "formal_original_byte_identical": frozen.read_bytes() == original.read_bytes(),
        "formal_source_manifest_identity_exact": all(sources[source_id][key] == preserved[source_id][key] for key in fields),
        "preserved_path_resolves_to_checked_original": EVIDENCE / preserved[source_id]["preserved_path"] == original,
    })

manifest = read_json(FROZEN / "3913485fc9b9d5810df5--checkpoint_manifest.json")
rows = []
original_comparison = read_json(EVIDENCE / "manifest-inventory-comparison.json")
for index, item in enumerate(manifest["files"]):
    same = [x for x in by_path[item["path"]] if (x["sha256"], x["size"]) == (item["sha256"], item["bytes"])]
    others = [x for x in by_path[item["path"]] if x not in same]
    normalized = {
        "path": item["path"], "manifest_sha256": item["sha256"], "manifest_bytes": item["bytes"],
        "frozen_matching_ids": [x["id"] for x in same], "other_frozen_ids": [x["id"] for x in others],
    }
    rows.append({
        "index": index, **normalized,
        "frozen_versions": [{k: x[k] for k in ("id", "sha256", "size", "sources")} for x in by_path[item["path"]]],
        "existing_comparison_row_exact": normalized == original_comparison[index],
    })

doc = RESOURCE.read_text()
prefix = manifest["files"][0]["path"].rsplit("/", 1)[0] + "/"
table_rows = [(int(i), p, int(b)) for i, p, b in re.findall(r"^\|(\d+)\|`([^`]+)`\|(\d+)\|$", doc, re.M)]
expected_rows = [(i, x["path"].removeprefix(prefix), x["bytes"]) for i, x in enumerate(manifest["files"])]
blocks = [json.loads(raw) for raw in re.findall(r"```json\n(.*?)\n```", doc, re.S)]
verification = read_json(FROZEN / "c6b117b9e8fd491d2d98--checkpoint_verification.json")
potential = read_json(FROZEN / "e68ceb56e0eb937c4162--potential_menu_replay.json")
finite_path = ROOT / "archives/customer-attraction/tools/evidence/potential-menu-joint/replay/audit_normal.json"
finite = read_json(finite_path)
shared_keys = sorted(potential.keys() & finite.keys())
script_path = finite_path.with_name("audit_potential_menu_joint.py")
positive_input_path = finite_path.with_name("potential_menu_joint.json")
manifest_by_name = {x["path"].removeprefix(prefix): x for x in manifest["files"]}
slacks = [Fraction(s) for s in potential["penultimate_all_alternatives_support_slack"]]
payoffs = [Fraction(s) for s in potential["actual_payoffs"]]
H6_times_60 = sum(60 // denominator for denominator in range(1, 7))

report = {
    "scope": "metadata/transcription/existing-evidence comparison and scalar algebra only; no original entry, import, matrix, potential enumeration, or full SPE check",
    "source_checks": source_checks,
    "manifest_summary": {
        "scope": manifest["scope"], "snapshot_commit": manifest["snapshot_commit"], "note": manifest["note"],
        "entries": len(rows), "unique_paths": len({x["path"] for x in rows}),
        "declared_total_bytes": sum(x["manifest_bytes"] for x in rows),
        "matching_path_sha256_bytes": sum(bool(x["frozen_matching_ids"]) for x in rows),
        "different_known_version": sum(not x["frozen_matching_ids"] and bool(x["other_frozen_ids"]) for x in rows),
        "missing_inventory_path": sum(not x["frozen_versions"] for x in rows),
        "all_existing_comparison_rows_exact": len(original_comparison) == len(rows) and all(x["existing_comparison_row_exact"] for x in rows),
        "resource_all_rows_exact_order_path_bytes": table_rows == expected_rows,
        "manifest_does_not_list_itself": "checkpoint_manifest.json" not in manifest_by_name,
    },
    "manifest_rows": rows,
    "resource_full_json_transcriptions": {
        "verification_exact": len(blocks) == 2 and blocks[0] == verification,
        "potential_replay_exact": len(blocks) == 2 and blocks[1] == potential,
    },
    "verification_shape": {
        "checks": len(verification["checks"]),
        "check_entries": [x["entry"] for x in verification["checks"]],
        "main_target": verification["main_target"],
        "curation_scope": verification["curation_dependency_check"]["scope"],
        "peer_replays_are_historical_report_fields": True,
    },
    "potential_existing_evidence_comparison": {
        "finite_output": fingerprint(finite_path),
        "finite_output_matches_manifest": fingerprint(finite_path)["sha256"] == manifest_by_name["research_6/audit_potential_menu_joint.json"]["sha256"] and finite_path.stat().st_size == manifest_by_name["research_6/audit_potential_menu_joint.json"]["bytes"],
        "shared_top_level_field_count": len(shared_keys), "shared_top_level_fields": shared_keys,
        "all_shared_fields_exact": all(potential[k] == finite[k] for k in shared_keys),
        "replay_only_fields": sorted(potential.keys() - finite.keys()),
        "finite_output_only_fields": sorted(finite.keys() - potential.keys()),
        "saved_script": fingerprint(script_path),
        "saved_script_matches_manifest": fingerprint(script_path)["sha256"] == manifest_by_name["research_6/audit_potential_menu_joint.py"]["sha256"],
        "historical_execution_sha256": potential["audit_source_sha256"],
        "historical_execution_sha256_equals_saved_script": potential["audit_source_sha256"] == fingerprint(script_path)["sha256"],
        "positive_type_input": fingerprint(positive_input_path),
        "positive_type_input_matches_manifest": fingerprint(positive_input_path)["sha256"] == manifest_by_name["research_6/potential_menu_joint.json"]["sha256"],
        "same_numbers_do_not_resolve_code_version_difference": True,
    },
    "scalar_checks_not_new_finite_enumeration": {
        "multiset_count_C23_6": comb(23, 6),
        "reported_multiset_count_matches": comb(23, 6) == potential["potential_multisets"],
        "argmax_width": len(potential["argmax"]), "argmax_total_slots": sum(potential["argmax"]),
        "actual_payoff_count": len(payoffs), "sum_actual_payoffs": str(sum(payoffs)),
        "maximum_minus_budget": str(Fraction(potential["maximum_potential"]) - Fraction(potential["budget_W_plus_C"])),
        "support_slack_count": len(slacks),
        "negative_support_slack_indices_zero_based": [i for i, x in enumerate(slacks) if x < 0],
        "zero_support_slack_indices_zero_based": [i for i, x in enumerate(slacks) if x == 0],
        "positive_support_slack_indices_zero_based": [i for i, x in enumerate(slacks) if x > 0],
        "computed_60H6": H6_times_60,
        "computed_int64_potential_upper_bound": potential["unit_customer_count"] * H6_times_60,
        "bound_matches_report": potential["unit_customer_count"] * H6_times_60 == potential["int64_potential_upper_bound"],
        "bound_below_signed_int64_max": potential["int64_potential_upper_bound"] < 2**63 - 1,
    },
}
(OUT / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
header = "index\tpath\tmanifest_bytes\tmanifest_sha256\tfrozen_versions(id:size:sha256)\n"
lines = []
for x in rows:
    versions = ";".join(f"{v['id']}:{v['size']}:{v['sha256']}" for v in x["frozen_versions"])
    lines.append(f"{x['index']}\t{x['path']}\t{x['manifest_bytes']}\t{x['manifest_sha256']}\t{versions}\n")
(OUT / "manifest-versions.tsv").write_text(header + "".join(lines))
assert all(all(x[k] for k in ("matches_frozen_fingerprint", "formal_original_byte_identical", "formal_source_manifest_identity_exact", "preserved_path_resolves_to_checked_original")) for x in source_checks)
assert report["manifest_summary"]["all_existing_comparison_rows_exact"]
assert report["manifest_summary"]["resource_all_rows_exact_order_path_bytes"]
assert all(report["resource_full_json_transcriptions"].values())
assert report["potential_existing_evidence_comparison"]["all_shared_fields_exact"]
print(json.dumps({"sources": len(source_checks), "manifest": report["manifest_summary"], "shared_finite_fields": len(shared_keys), "negative_slack_indices": report["scalar_checks_not_new_finite_enumeration"]["negative_support_slack_indices_zero_based"]}, ensure_ascii=False, indent=2))
