"""Read every frozen audit row and field against the preserved exact implementation.

This validates the two full TSV domains, all four path matrices and all saved
JSON fields, instead of using report summaries as a substitute for the data.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast
import csv
import hashlib
import importlib.util
import json

BASE = Path(__file__).resolve().parent
ORIG = BASE / "original"
FROZEN = ORIG / "evidence/runs/2026-10-10/global_decorrelation_independent"


def main():
    script = ORIG / "tests/audits/customer_attraction_global_decorrelation_independent.py"
    spec = importlib.util.spec_from_file_location("budget_independent", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    snapshot = json.loads((FROZEN / "certificate_data.json").read_text())
    game = module.TypeGame(6, 4, {int(k): v for k, v in snapshot["weights"].items()}, snapshot["policy"])
    original_weights, original_policy = module.certificate_literals()
    assert original_weights == game.weights and original_policy == snapshot["policy"]
    source_input = json.loads((ORIG / "examples/customer_attraction/global_decorrelation_failure.json").read_text())
    weights_from_input = {sum(1 << a for a in row["topics"]): row["multiplicity"]
                          for row in source_input["customers"]}
    assert weights_from_input == game.weights
    cert = json.loads((ORIG / "evidence/certificates/customer_attraction/global_decorrelation_failure.json").read_text())
    assert {tuple(r["history"]): r["action"] for r in cert["strategy"]["actions"]} == game.policy
    assert tuple(map(F, snapshot["primary"])) == tuple(map(F, cert["security"]["primary"]))
    assert {tuple(r["B"]): F(r["probability"]) for r in snapshot["dual"]} == {
        tuple(r["rivals"]): F(r["probability"]) for r in cert["security"]["dual"]}

    with (FROZEN / "all_incentive_comparisons.tsv").open() as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        assert reader.fieldnames == ["history", "action", "original_terminal", "deviation_terminal", "slack"]
        incentive_rows = list(reader)
    observed, slacks = set(), []
    for row in incentive_rows:
        h, a = ast.literal_eval(row["history"]), int(row["action"])
        z = ast.literal_eval(row["original_terminal"])
        off = ast.literal_eval(row["deviation_terminal"])
        assert (h, a) not in observed
        observed.add((h, a))
        assert z == game.terminal(h) and off == game.terminal(h + (a,))
        slack = game.payoffs[z][0][len(h)] - game.payoffs[off][0][len(h)]
        assert F(row["slack"]) == slack >= 0
        slacks.append(slack)
    assert observed == {(h, a) for h in game.histories for a in range(6)}
    assert len(incentive_rows) == 1554

    with (FROZEN / "all_static_competitors.tsv").open() as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        assert reader.fieldnames == ["competitors"] + [f"f_{a}" for a in range(6)] + ["primary_value"]
        static_rows = list(reader)
    observed = set()
    primary = tuple(map(F, snapshot["primary"]))
    for row in static_rows:
        rivals = ast.literal_eval(row["competitors"])
        assert rivals not in observed
        observed.add(rivals)
        values = tuple(F(row[f"f_{a}"]) for a in range(6))
        assert values == tuple(game.static(a, rivals) for a in range(6))
        assert F(row["primary_value"]) == sum(p*v for p, v in zip(primary, values))
    assert observed == set(product(range(6), repeat=3)) and len(static_rows) == 216

    matrices = json.loads((FROZEN / "on_path_query_matrices.json").read_text())
    root = game.terminal(())
    for i, row in enumerate(matrices):
        assert set(row) == {"player", "history", "rivals_by_action", "full_query_matrix"}
        assert row["player"] == i+1 and tuple(row["history"]) == root[:i]
        rivals = []
        for a in range(6):
            off = game.terminal(root[:i] + (a,))
            rivals.append(off[:i] + off[i+1:])
        assert tuple(map(tuple, row["rivals_by_action"])) == tuple(rivals)
        assert [[F(v) for v in r] for r in row["full_query_matrix"]] == [
            [game.static(a, B) for B in rivals] for a in range(6)]
    assert len(matrices) == 4

    compared = {}
    for name in ["all_incentive_comparisons.tsv", "all_static_competitors.tsv"]:
        assert (FROZEN/name).read_bytes() == (BASE/"replay-independent89"/name).read_bytes()
        compared[name] = "all rows and bytes identical"
    for name in ["certificate_data.json", "on_path_query_matrices.json", "results.json"]:
        assert json.loads((FROZEN/name).read_text()) == json.loads((BASE/"replay-independent89"/name).read_text())
        compared[name] = "all nested fields identical"
    original_main = json.loads((ORIG/"evidence/runs/2026-10-10/customer_attraction_root_security_uploads.json").read_text())
    assert original_main == json.loads((BASE/"replay-combined.json").read_text())
    original36 = json.loads((ORIG/"evidence/runs/2026-10-10/customer_attraction_onpath_budget_independent.json").read_text())
    stamp = original36.pop("audit_source_sha256")
    assert stamp == hashlib.sha256((ORIG/"tests/audits/customer_attraction_onpath_budget_independent.py").read_bytes()).hexdigest()
    assert original36 == json.loads((BASE/"replay-independent36.json").read_text())
    result = {"status": "PASS", "incentive_rows": len(incentive_rows), "incentive_fields_per_row": 5,
              "static_rows": len(static_rows), "static_fields_per_row": 8,
              "path_matrices": len(matrices), "matrix_entries": 144, "actual_rival_tuples": 24,
              "zero_slacks": sum(s == 0 for s in slacks), "strict_slacks": sum(s > 0 for s in slacks),
              "minimum_strict_slack": str(min(s for s in slacks if s > 0)),
              "frozen_independent89_vs_replay": compared,
              "combined_report_all_fields_identical": True,
              "independent36_report": "all runtime fields identical; frozen extra audit_source_sha256 verified against the preserved script",
              "scope": "All complete frozen rows and fields checked against the original exact implementation; no universal budget claim."}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
