"""Recheck the named finite point; never optimize or assert a game completion.

The whole matrix is reconstructed with the frozen original builder. The 27
omitted cut records are independently reconstructed by the archived literal-bit
audit implementation, and then evaluated at both saved vectors as applicable.
Only the compact current verification report is written inside this task.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import ast
import hashlib
import importlib
import importlib.util
import json
import platform
import shutil
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
POINTS = ROOT / "archives/customer-attraction/tools/evidence/combined-latest-local-points-boss3"
PACKS = ROOT / "archives/customer-attraction/tools/evidence/requery-capacity-cut-packs-boss3"
BASE = "research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def metadata(column):
    # Frozen builders use tuples; saved JSON necessarily uses arrays. Normalize
    # only serialization form, while preserving every descriptor and its order.
    return json.loads(json.dumps({key: value for key, value in column.items() if key != "weight"}))


def dot(row, positive):
    return sum((row[index] * weight for index, weight in positive if row[index]), F())


def main():
    start = time.monotonic()
    assert sys.flags.optimize == 0
    task = read_json(ROOT / "research/operations/map-v2/tasks/customer-attraction-3a-3a-1c0523cb3504a537.json")
    checked_refs = []
    for ref in task["definition"]["context_plan"]["reading_refs"]:
        raw = (ROOT / ref["path"]).read_bytes()
        assert digest(raw) == ref["sha256"]
        checked_refs.append({"path": ref["path"], "sha256": digest(raw), "bytes": len(raw)})

    source_manifest = read_json(POINTS / "source-manifest.json")
    points = {}
    for record in source_manifest:
        raw = (POINTS / record["stored_path"]).read_bytes()
        assert len(raw) == record["size"] and digest(raw) == record["sha256"]
        point = json.loads(raw)
        assert len(point) == 11 and len(point["columns"]) == 1905
        points[Path(record["path"]).name] = point
    latest = points["combined_branch_latest_exact.json"]
    local = points["combined_branch_local_exact.json"]
    assert [metadata(c) for c in latest["columns"]] == [metadata(c) for c in local["columns"]]
    vectors = {name: [F(c["weight"]) for c in point["columns"]] for name, point in points.items()}
    schemas = {
        "K": ("kind", "weight"),
        "hist": ("kind", "actual_bits", "d", "hist", "weight"),
        "joint-reply": ("kind", "hist_column_old", "group", "state", "weight"),
        "overlap": ("kind", "hist_column", "groups", "weight"),
    }
    for name, point in points.items():
        assert Counter(c["kind"] for c in point["columns"]) == {"K": 1, "hist": 16, "joint-reply": 582, "overlap": 1306}
        assert all(tuple(c) == schemas[c["kind"]] for c in point["columns"])
        assert min(vectors[name]) >= 0
        assert sum(w > 0 for w in vectors[name]) == point["positive_columns"]
        for column in point["columns"]:
            if column["kind"] == "hist":
                assert column["d"] == 1 and len(column["hist"]) == 8 and sum(column["hist"]) == 6
    changes = [index for index, (a, b) in enumerate(zip(vectors["combined_branch_latest_exact.json"], vectors["combined_branch_local_exact.json"])) if a != b]
    assert len(changes) == 218
    assert Counter(local["columns"][index]["kind"] for index in changes) == {"K": 1, "hist": 11, "joint-reply": 102, "overlap": 104}
    old_report = read_json(POINTS / "replay/two-point-full-verification.json")
    assert [row["column"] for row in old_report["comparison"]["changed_columns"]] == changes
    for entry in old_report["comparison"]["changed_columns"]:
        index = entry["column"]
        assert entry["kind"] == local["columns"][index]["kind"]
        assert F(entry["latest_weight"]) == vectors["combined_branch_latest_exact.json"][index]
        assert F(entry["local_weight"]) == vectors["combined_branch_local_exact.json"][index]

    runtime_manifest = read_json(POINTS / "runtime-dependency-manifest.json")
    assert digest((ROOT / runtime_manifest["base_package_manifest"]).read_bytes()) == runtime_manifest["base_manifest_sha256"]
    assert len(runtime_manifest["base_frozen_sources"]) == 47
    runtime = Path(tempfile.mkdtemp(prefix="local5189-runtime-", dir=ROOT.parent))
    try:
        (runtime / "work.py").write_text(runtime_manifest["synthetic_root_marker"])
        for record in runtime_manifest["base_frozen_sources"]:
            raw = (ROOT / record["stored_path"]).read_bytes()
            assert len(raw) == record["size"] and digest(raw) == record["sha256"]
            destination = runtime / record["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
        for record in source_manifest:
            destination = runtime / record["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((POINTS / record["stored_path"]).read_bytes())
        builder = runtime / BASE / "research_5/combined_branch_master.py"
        tree = ast.parse(builder.read_text())
        build_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build")
        if_tests = [ast.get_source_segment(builder.read_text(), node.test) for node in build_node.body if isinstance(node, ast.If)]
        assert if_tests == ["'--latest' in sys.argv", "'--new-local' in sys.argv or '--local-v2' in sys.argv"]
        local_cut_data = read_json(builder.parent / "joint_local_cuts.json")
        assert set(local_cut_data) == {"scope", "nested", "requery"}
        assert len(local_cut_data["nested"]) == 5 and len(local_cut_data["requery"]) == 4
        sys.argv = [str(builder), "--latest", "--new-local"]
        sys.path.insert(0, str(builder.parent))
        build_start = time.monotonic()
        module = importlib.import_module("combined_branch_master")
        columns, names, rows, objective, norm = module.build()
        build_seconds = time.monotonic() - build_start
        assert len(columns) == len(objective) == len(norm) == 1905
        assert len(names) == len(rows) == 5189 and all(len(row) == 1905 for row in rows)
        assert [metadata(c) for c in columns] == [metadata(c) for c in local["columns"]]
        assert all(name.startswith("actual4-force-new-reply-local:") for name in names[5180:5185])
        assert all(name.startswith("same-source-reply-requery:") for name in names[5185:])
        matrix_results = {}
        for filename, point in points.items():
            positive = [(j, weight) for j, weight in enumerate(vectors[filename]) if weight]
            actual_O = dot(norm, positive)
            actual_W = dot(objective, positive)
            assert actual_O == F(point["O"]) == 1
            assert actual_W == F(point["W"])
            assert actual_O - 2 * actual_W == F(point["strict_half_gap"]) > 0
            slacks = [dot(row, positive) for row in rows]
            included = 5180 if filename == "combined_branch_latest_exact.json" else 5189
            assert point["verified_rows"] == included
            assert min(slacks[:included]) == F(point["minimum_slack"]) == 0
            assert all(value >= 0 for value in slacks[:included])
            archived = old_report["points"][filename]
            assert archived["complete_input_header"] == {k: v for k, v in point.items() if k != "columns"}
            assert archived["included_zero_rows"] == sum(value == 0 for value in slacks[:included])
            for item in archived["latest_seventy_two"] + archived["local_nine"]:
                assert item["name"] == names[item["row"]]
                assert F(item["slack"]) == slacks[item["row"]]
            nine = [{"row": index, "name": names[index], "slack": str(slacks[index])} for index in range(5180, 5189)]
            matrix_results[filename] = {
                "included_rows": included,
                "all_included_rows_nonnegative": True,
                "minimum_slack": str(min(slacks[:included])),
                "zero_rows": sum(value == 0 for value in slacks[:included]),
                "positive_columns": len(positive),
                "positive_by_kind": dict(Counter(point["columns"][j]["kind"] for j, _ in positive)),
                "O": str(actual_O), "W": str(actual_W), "K": str(vectors[filename][0]),
                "strict_half_gap_O_minus_2W": str(actual_O - 2 * actual_W),
                "local_nine": nine,
            }
        assert all(F(x["slack"]) < 0 for x in matrix_results["combined_branch_latest_exact.json"]["local_nine"])
        assert all(F(x["slack"]) >= 0 for x in matrix_results["combined_branch_local_exact.json"]["local_nine"])
        actual_argv = ["combined_branch_master.py", *sys.argv[1:]]
        builder_sha256 = digest(builder.read_bytes())
    finally:
        shutil.rmtree(runtime)

    # Import defines pure functions; the archived main, file writers and LPs are
    # not executed. The independent path explicitly enumerates named indices
    # and literal successor memberships before it takes the joint minimum.
    audit_source = PACKS / "audit_cut_packs.py"
    spec = importlib.util.spec_from_file_location("local5189_literal_cut_audit", audit_source)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    sparse = read_json(PACKS / "runs/all-sparse-row-coefficients.json")
    transfer = read_json(POINTS / "replay/certified-cuts-at-local5189.json")
    assert len(sparse) == len(transfer["results"]) == 27
    indexed = {(record["pack"], record["field"], record["number"]): record for record in sparse}
    assert len(indexed) == 27 and sum(len(record["nonzero"]) for record in sparse) == 3718
    cut_results = []
    coordinate_comparisons = 0
    for saved in transfer["results"]:
        key = (saved["pack"], saved["field"], saved["number"])
        frozen = indexed[key]
        cut = saved["cut"]
        kind = "requery" if "parameters" in cut else "portfolio"
        row = audit.independent_row(local["columns"], kind, cut)
        assert len(row) == 1905
        original_length = frozen["length"]
        assert original_length in (1905, 2033)
        padded = row + [F()] * (original_length - 1905)
        expected = [F()] * original_length
        positions = []
        for position, coefficient in frozen["nonzero"]:
            assert isinstance(position, int) and 0 <= position < original_length and F(coefficient) != 0
            expected[position] = F(coefficient)
            positions.append(position)
        assert positions == sorted(set(positions))
        assert padded == expected
        assert audit.row_hash(padded) == frozen["row_sha256"] == saved["row_sha256"]
        assert all(value == 0 for value in expected[1905:])
        coordinate_comparisons += original_length
        assert all(not coefficient or local["columns"][index]["kind"] in ("K", "hist", "joint-reply") for index, coefficient in enumerate(row))
        local_slack = sum((coefficient * weight for coefficient, weight in zip(row, vectors["combined_branch_local_exact.json"])), F())
        assert local_slack == F(saved["local5189_slack"])
        old_slack = None
        if saved["original_bound_point_sha256"] == source_manifest[0]["sha256"]:
            old_slack = sum((coefficient * weight for coefficient, weight in zip(row, vectors["combined_branch_latest_exact.json"])), F())
            assert old_slack == F(saved["original_reported_and_previously_checked_slack"]) < 0
        cut_results.append({
            "pack": key[0], "field": key[1], "number": key[2], "cut": cut,
            "original_length": original_length, "original_row_sha256": frozen["row_sha256"],
            "common_1905_row_sha256": audit.row_hash(row),
            "local5189_slack": str(local_slack),
            "current_latest5180_slack": str(old_slack) if old_slack is not None else None,
        })
    assert coordinate_comparisons == 52075
    groups = {}
    for pack in {result["pack"] for result in cut_results}:
        records = [record for record in cut_results if record["pack"] == pack]
        slacks = [F(record["local5189_slack"]) for record in records]
        groups[pack] = {
            "records": len(records), "negative": sum(v < 0 for v in slacks),
            "zero": sum(v == 0 for v in slacks), "positive": sum(v > 0 for v in slacks),
            "distinct_negative_vectors": len({record["common_1905_row_sha256"] for record in records if F(record["local5189_slack"]) < 0}),
        }
    requery = [result for result in cut_results if result["pack"] == "early_reply_requery_master_all_queries.json"]
    assert [record["number"] for record in requery if F(record["local5189_slack"]) < 0] == list(range(5, 12))
    assert requery[7]["common_1905_row_sha256"] == requery[8]["common_1905_row_sha256"]
    assert groups["early_reply_requery_master_all_queries.json"] == {"records": 14, "negative": 7, "zero": 4, "positive": 3, "distinct_negative_vectors": 6}
    assert all(record["cut"] == cut for record, cut in zip([requery[2], requery[0], requery[1], requery[3]], local_cut_data["requery"]))
    report = {
        "status": "passed", "python": platform.python_version(), "seconds": time.monotonic() - start,
        "checked_task_reading_refs": checked_refs,
        "reading_scope": {
            "both_original_JSONs": "All eleven fields and all 1905 column descriptors/weights parsed and compared; no raw JSON displayed in full.",
            "two_point_report": "All fields parsed; all 218 changed-coordinate entries and all 72+9 named archived slacks per point checked against current reconstruction.",
            "runtime_manifest": "All 47 dependency entries read and their complete bytes hashed before temporary materialization.",
            "omitted_cut_data": "All 27 records; all 3718 saved nonzero entries; all 52075 positions including pending zero tails; literal reconstruction and current local-point Fraction dot products.",
            "source_text": "Complete mathematical point/model/method/cut-pack prose and complete two verification scripts read as text; frozen builder AST append order inspected, rest executed as frozen implementation rather than claimed independent textual review.",
        },
        "matrix_reconstruction": {
            "successful_run_builder_calls": 1, "same_archived_implementation": True,
            "builder_sha256": builder_sha256, "build_seconds": build_seconds, "argv": actual_argv,
            "rows": 5189, "columns": 1905, "archived_dependency_files_hashed": 47,
            "points": matrix_results,
        },
        "weight_changes": {"total": 218, "by_kind": {"K": 1, "hist": 11, "joint-reply": 102, "overlap": 104}},
        "literal_cut_reconstruction": {
            "implementation_path": str(audit_source.relative_to(ROOT)), "implementation_sha256": digest(audit_source.read_bytes()),
            "records": 27, "full_length_coefficient_comparisons": coordinate_comparisons,
            "saved_nonzero_entries_checked": 3718, "original_helper_calls": 0,
            "original_pending5277_point_replayed": False, "groups": groups, "results": cut_results,
        },
        "optimizer_calls": 0,
        "limits": "Only these frozen exact vectors and necessary rows. Matrix replay reuses the original builder; literal cut reconstruction reuses the archived independent audit. No full-catalog completion, whole-system infeasibility, LP optimum or general half result is inferred.",
    }
    output = HERE / "local5189-verification.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "output": str(output), "seconds": report["seconds"], "matrix": {name: {k: v for k, v in result.items() if k != "local_nine"} for name, result in matrix_results.items()}, "cut_groups": groups}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
