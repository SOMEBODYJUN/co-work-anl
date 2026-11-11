"""Summarize certified results and create a reproducible file manifest."""
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
    point = json.loads((HERE / "augmented_lp_exact.json").read_text())
    dual = json.loads((HERE / "exact_dual_certificate.json").read_text())
    verified = json.loads((HERE / "certificate_verification.json").read_text())
    assert verified["exact_primal_verified"] and verified["exact_dual_verified"]
    with gzip.open(HERE / "exact_matrix.json.gz", "rt") as stream:
        matrix = json.load(stream)
    audit = json.loads((HERE / "primal_exact_audit.json").read_text())
    structure = json.loads((HERE / "epigraph_structure.json").read_text())
    inputs = json.loads((HERE / "inputs.json").read_text())
    old = json.loads((HERE / "old_point_audit.json").read_text())
    W = F(point["W"])
    assert W == F(dual["normalization_multiplier"])
    full = [F(col["weight"]) for col in point["columns"]]
    original_n = structure["original_columns"]
    slacks = list(map(F, audit["row_slacks"]))
    budget_slacks = [slacks[i] for i in structure["budget_rows"]]
    epigraph_rows = {record["row"] for record in structure["records"]}
    multipliers = {i: F(v) for i, v in dual["row_multipliers"]}
    baseline_rows = inputs["baseline_rows"]
    new_dual = [{"row": i, "name": matrix["row_names"][i], "weight": str(v)}
                for i, v in multipliers.items() if i >= baseline_rows]
    result = {"scope": "exact optimum of this finite fixed16hist necessary LP only; original six-player problem remains OPEN",
              "rows": len(matrix["rows"]), "columns": len(full), "new_rows": len(matrix["rows"])-baseline_rows,
              "W": str(W), "W_float": float(W), "below_half": W < F(1, 2),
              "strict_half_gap": str(1-2*W), "strict_half_gap_float": float(1-2*W),
              "exact_increase_from_sorting13853": str(W-F(old["W"])),
              "increase_float": float(W-F(old["W"])),
              "positive_original_columns": sum(v > 0 for v in full[:original_n]),
              "positive_auxiliary_columns": sum(v > 0 for v in full[original_n:]),
              "positive_original_by_kind": dict(Counter(c["kind"] for c, v in zip(point["columns"][:original_n], full[:original_n]) if v > 0)),
              "positive_dual_rows": len(multipliers), "positive_new_dual_rows": new_dual,
              "positive_epigraph_dual_rows": [[i, str(v)] for i, v in multipliers.items() if i in epigraph_rows],
              "minimum_budget_slack": str(min(budget_slacks)), "minimum_budget_slack_float": float(min(budget_slacks)),
              "zero_budget_rows": [i for i in structure["budget_rows"] if slacks[i] == 0],
              "zero_new_cut_rows": [i for i in range(baseline_rows, len(slacks)) if slacks[i] == 0],
              "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest(),
              "point_sha256": sha256((HERE / "augmented_lp_exact.json").read_bytes()).hexdigest(),
              "dual_sha256": sha256((HERE / "exact_dual_certificate.json").read_bytes()).hexdigest(),
              "primal_recovery": {k: audit["recovery"][k] for k in ("variables", "rank", "processed_equations", "free_variables", "seconds")},
              "dual_recovery": dual["recovery"]}
    write("result_summary.json", result)
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "scope": result["scope"], "result": {k: result[k] for k in ("rows", "columns", "W", "below_half")},
                "files": {path.name: {"bytes": path.stat().st_size, "sha256": sha256(path.read_bytes()).hexdigest()}
                          for path in sorted(HERE.iterdir()) if path.is_file() and path.name != "final_manifest.json"}}
    write("final_manifest.json", manifest)
    print(json.dumps({k: v for k, v in result.items() if k not in ("positive_new_dual_rows", "dual_recovery")}, indent=2))


if __name__ == "__main__":
    main()
