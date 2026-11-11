"""Create a concise exact result summary and a complete artifact manifest."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")


def main():
    verified = json.loads((HERE / "certificate_verification.json").read_text())
    assert verified["exact_primal_verified"] and verified["exact_dual_verified"]
    point = json.loads((HERE / "augmented_lp_exact.json").read_text())
    baseline_point = json.loads((HERE.parent / "augmented_lp_exact.json").read_text())
    primal = json.loads((HERE / "primal_exact_audit.json").read_text())
    dual = json.loads((HERE / "exact_dual_certificate.json").read_text())
    epi = json.loads((HERE / "epigraph_structure.json").read_text())
    zz = json.loads((HERE / "zz_envelope_structure.json").read_text())
    early = json.loads((HERE / "early_cut_records.json").read_text())
    status = json.loads((HERE / "status.json").read_text())
    source = json.loads((HERE / "old_point_audit.json").read_text())
    with gzip.open(HERE / "exact_matrix.json.gz", "rt") as stream:
        matrix = json.load(stream)
    W, old_W = F(point["W"]), F(source["W"])
    changes = [{"column": j, "kind": col["kind"], "old": old["weight"], "new": col["weight"],
                "difference": str(F(col["weight"])-F(old["weight"]))}
               for j, (col, old) in enumerate(zip(point["columns"][:4849], baseline_point["columns"][:4849]))
               if F(col["weight"]) != F(old["weight"])]
    write("original_coordinate_changes.json", {"baseline_point_sha256": sha256((HERE.parent / "augmented_lp_exact.json").read_bytes()).hexdigest(),
                                               "changed_columns": changes, "changed_by_kind": dict(Counter(record["kind"] for record in changes))})
    slacks = list(map(F, primal["row_slacks"]))
    assert W == F(dual["normalization_multiplier"])
    epigraph_rows = {record["row"] for record in epi["records"]}
    upper_rows, orbit_rows = set(zz["upper_rows"]), set(zz["budget_rows"])
    early_rows = {record["row"] for record in early if record["added"]}
    classes = Counter()
    new_dual = []
    for i, weight in dual["row_multipliers"]:
        kind = "old_epigraph" if i in epigraph_rows else "ZZ_min_upper" if i in upper_rows else "ZZ_min_budget" if i in orbit_rows else "new_early_cut" if i in early_rows else "inherited_original"
        classes[kind] += 1
        if i >= zz["prior_rows"]:
            new_dual.append({"row": i, "name": matrix["row_names"][i], "kind": kind, "weight": weight})
    point_hash = sha256((HERE / "augmented_lp_exact.json").read_bytes()).hexdigest()
    separated = json.loads((HERE / "zz-at-certified-point.json").read_text())
    assert separated["input_sha256"] == point_hash and separated["ZZ_negative_count"] == 0
    nonself = [F(record["value"]) for record in separated["known_ZZ_frechet_bounds_at_this_point"] if record["row"]]
    result = {"scope": "exact fixed16hist necessary optimum with all 39 old-Z/old-Z Frechet minimum envelopes; not SPE or a full-model welfare theorem",
              "rows": len(matrix["rows"]), "columns": len(matrix["columns"]),
              "W": str(W), "W_float": float(W), "strict_half_gap": str(1-2*W), "strict_half_gap_float": float(1-2*W),
              "below_half": W < F(1, 2), "exact_increase": str(W-old_W), "increase_float": float(W-old_W),
              "positive_original_columns": verified["positive_original_columns"],
              "positive_old_max_auxiliaries": verified["positive_old_max_auxiliaries"],
              "positive_new_min_auxiliaries": verified["positive_new_min_auxiliaries"],
              "positive_total_columns": point["positive_columns"],
              "changed_original_coordinates_by_kind": dict(Counter(record["kind"] for record in changes)),
              "all_hist_masses_unchanged": not any(record["kind"] == "hist" for record in changes),
              "K_unchanged": not any(record["kind"] == "K" for record in changes),
              "positive_dual_rows": len(dual["row_multipliers"]), "positive_dual_row_classes": dict(classes),
              "positive_new_dual_rows": new_dual,
              "old_max_budget_minimum_slack": str(min(slacks[i] for i in epi["budget_rows"])),
              "old_max_zero_budget_count": sum(slacks[i] == 0 for i in epi["budget_rows"]),
              "ZZ_minimum_budget_slack": str(min(slacks[i] for i in zz["budget_rows"])),
              "ZZ_zero_budget_count": sum(slacks[i] == 0 for i in zz["budget_rows"]),
              "ZZ_frozen_separator_classes": separated["ZZ_nonempty_literal_classes"],
              "ZZ_frozen_separator_negative_count": separated["ZZ_negative_count"],
              "ZZ_nonself_separator_minimum": str(min(nonself)),
              "early_cut_slacks": [{"row": r["row"], "name": r["name"], "slack": str(slacks[r["row"]])} for r in early],
              "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest(),
              "point_sha256": point_hash, "dual_sha256": sha256((HERE / "exact_dual_certificate.json").read_bytes()).hexdigest(),
              "primal_recovery": {k: primal["recovery"][k] for k in ("variables", "rank", "processed_equations", "free_variables", "min_tie_equations", "seconds")},
              "free_original_coordinates": [{"column": primal["recovery"]["support"][local],
                                              "kind": point["columns"][primal["recovery"]["support"][local]]["kind"],
                                              "value": value}
                                             for local, value in primal["recovery"]["free_values"]],
              "dual_recovery": dual["recovery"],
              "solver_seconds": status["solver_seconds"], "solver_iterations": status["solver_iterations"]}
    write("result_summary.json", result)
    executions = json.loads((HERE / "execution_records.json").read_text())
    assert {record["stage"] for record in executions} == {"solve", "recover", "verify", "separate"}
    for record in executions:
        assert record["exit_code"] == 0
        for stream in ("stdout", "stderr"):
            assert sha256((HERE / record[stream]).read_bytes()).hexdigest() == record[stream+"_sha256"]
        assert sha256((HERE / record["entry_snapshot"]).read_bytes()).hexdigest() == record["entry_sha256"]
    owner_note = HERE.parent.parent / "zz_closure_lp.md"
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "scope": result["scope"],
                "result": {k: result[k] for k in ("rows", "columns", "W", "below_half")},
                "all_execution_records_verified": True,
                "owner_note": {"path": str(owner_note), "sha256": sha256(owner_note.read_bytes()).hexdigest()},
                "files": {str(path.relative_to(HERE)): {"bytes": path.stat().st_size, "sha256": sha256(path.read_bytes()).hexdigest()}
                          for path in sorted(HERE.rglob("*")) if path.is_file() and path.name != "final_manifest.json"}}
    write("final_manifest.json", manifest)
    print(json.dumps({k: v for k, v in result.items() if k not in ("positive_new_dual_rows", "dual_recovery", "early_cut_slacks")}, indent=2))


if __name__ == "__main__":
    main()
