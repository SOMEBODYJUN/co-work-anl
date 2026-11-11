#!/usr/bin/env python3
"""Freeze only this unbound symbolic package after its direct exact checks."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ADJACENT = HERE.with_suffix(".md")
MANIFEST = HERE / "freeze_manifest.json"
SUMS = HERE / "SHA256SUMS"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_json(name):
    return json.loads((HERE / name).read_text())


assert not MANIFEST.exists() and not SUMS.exists(), "Already frozen; no overwrite."
assert ADJACENT.is_file()
pins = read_json("source_pins.json")
assert pins["source_count"] == len(pins["sources"]) == 24
assert pins["old_numeric_primal_or_optimal_face_files_read"] is False
for relative, expected in pins["sources"].items():
    assert digest(REPO / relative) == expected, relative

template = read_json("symbolic_template.json")
release = read_json("future_point_release_template.json")
checks = read_json("symbolic_check_result.json")
build = read_json("build_result.json")
full = read_json("full751_audit_view.json")
active = read_json("active734_catalogue.json")
migration = read_json("migration_audit.json")
routing = read_json("visible_prerequisite_routing.json")
fixtures = read_json("literal_static_fixtures.json")
assert template["status"] == "SYMBOLIC_UNBOUND_FIXED_C"
for key in [
    "fixed_input", "fixed_atom_masses", "fixed_K", "fixed_O", "support",
    "fixed_matrix", "phaseI", "certificate", "projection_weights"
]:
    assert template[key] is None, key
assert template["outer_q_moment_rows"] == []
assert template["optimizer_calls"] == 0
assert template["optimizer_authorized"] is False
assert release["status"] == "UNBOUND_NO_AUTHORIZATION"
assert release["old1002_and1003_candidates_not_eligible"] is True
assert all(value is None for key, value in release.items()
           if key not in {"status", "old1002_and1003_candidates_not_eligible"})
assert checks["status"] == "PASS_SYMBOLIC_FIXED_C_734_UNBOUND_WITH_FULL751_MIGRATION"
assert checks["optimizer_calls"] == build["optimizer_calls"] == fixtures["optimizer_calls"] == 0
for key in [
    "fixed_point_bound", "matrix_constructed", "old_numerical_point_files_read",
    "old_producer_kernel_executed"
]:
    assert checks[key] is False, key
assert len(full["rows"]) == full["count"] == 751
assert len(active["rows"]) == active["row_count"] == 734
assert Counter(row["family"] for row in active["rows"]) == active["family_counts"]
assert len(migration["all751_row_records"]) == 751
assert migration["inapplicable_genuine_kernel_indices"] == []
assert all(row["valid_for_any_fixed_legal_outer_label"]
           and not row["depends_on_outer_six_index_average"]
           for row in migration["all751_row_records"])
assert routing["route_count"] == 17
assert routing["nonnegative_visible_rows"] == 16
assert routing["free_C_size_equalities"] == 1
assert routing["all_coefficient_checks"] == 8721
assert routing["future_reconfirmation_required"] is True
assert build["full_joint_states"] == checks["all8192_C30_state_routes"] == 8192

copy_pairs = {
    "legacy_751_catalogue.json": "actual_source2_nested_requery/row_catalogue.json",
    "legacy_751_kernel.py.txt": "actual_source2_nested_requery/symbolic_coefficients.py",
    "legacy_243_kernel.py.txt": "actual_source2_opt_requery/symbolic_coefficients.py",
}
for local, source in copy_pairs.items():
    assert digest(HERE / local) == digest(HERE.parent / source)

files = sorted(path for path in HERE.iterdir() if path.is_file()) + [ADJACENT]
assert all(path.is_file() for path in HERE.iterdir()), "Unexpected subdirectory."
assert len(files) == 20, [path.name for path in files]
links_checked = 0
for path in files:
    text = path.read_text()
    assert not any(line.endswith((" ", "\t")) for line in text.splitlines()), path
    assert text.endswith("\n"), path
    if path.suffix == ".json":
        json.loads(text)
    if path.suffix == ".md":
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            assert not link.startswith(("http:", "https:", "file:")), link
            assert (path.parent / link).is_file(), (path.name, link)
            links_checked += 1

artifacts = {str(path.relative_to(REPO)): digest(path) for path in files}
manifest = {
    "status": "FROZEN_SYMBOLIC_FIXED_C_734_UNBOUND",
    "owner": "Boss1",
    "RUN": "six-boss1-20261111",
    "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
    "authorization_scope": (
        "Main authorized fixed-C symbolic migration only: full751 audit view, "
        "734 active hidden rows,17 explicit visible routes, no old-point "
        "binding, no phaseI and no optimizer."
    ),
    "model_scope": (
        "Finite unit clients, common finite nonempty label catalogue with "
        "empty/alias labels, repeats and weak off-path ties; complete ordered "
        "pure SPE. Fixed true branch(A1,C,R3,R4,R5,R6), global |C|=K."
    ),
    "full_audit_rows": 751,
    "active_hidden_rows": 734,
    "visible_prerequisite_inequalities": 16,
    "C_size_equality_routes": 1,
    "inapplicable_genuine_kernel_count": 0,
    "full_visible_types": 512,
    "tail_states_per_type": 16,
    "full_joint_state_domain": 8192,
    "outer_q_moment_rows": 0,
    "future_physical_dimensions": "16s columns, s mass equations,734 hidden rows",
    "visible_prerequisites_must_be_reconfirmed": True,
    "visible_prerequisites_inferred_from_hidden_rows": False,
    "inner_C30_query_moments_preserved": True,
    "optimizer_calls": 0,
    "optimizer_authorized": False,
    "fixed_point_bound": False,
    "matrix_constructed": False,
    "old_numerical_point_files_read": False,
    "old_producer_kernel_executed": False,
    "direct_check_result": checks,
    "source_count": len(pins["sources"]),
    "source_sha256": pins["sources"],
    "artifact_count_excluding_manifest_and_checksums": len(artifacts),
    "artifact_sha256": artifacts,
    "local_document_links_checked": links_checked,
    "trailing_whitespace_found": False,
    "boundary": (
        "Necessary unbound symbolic contract, not an SPE characterization, "
        "fixed-point feasibility result, universal projected cut, numerical "
        "welfare improvement or solution of the original six-player half problem."
    ),
}
with MANIFEST.open("x") as output:
    output.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
sum_files = sorted([*files, MANIFEST], key=lambda path: str(path))
with SUMS.open("x") as output:
    for path in sum_files:
        relative = path.name if path.parent == HERE else "../" + path.name
        output.write(digest(path) + "  " + relative + "\n")
for relative, expected in artifacts.items():
    assert digest(REPO / relative) == expected
for relative, expected in pins["sources"].items():
    assert digest(REPO / relative) == expected
print(json.dumps({
    "status": manifest["status"],
    "manifest_sha256": digest(MANIFEST),
    "SHA256SUMS_sha256": digest(SUMS),
    "artifact_files_excluding_manifest_and_checksums": len(artifacts),
    "checksum_entries": len(sum_files),
    "source_files_unchanged": len(pins["sources"]),
    "local_document_links_checked": links_checked,
    "optimizer_calls": 0,
    "fixed_point_bound": False,
}, indent=2))
