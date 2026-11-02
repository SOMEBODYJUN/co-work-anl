"""Read-only comparison of the frozen floating point and exact witnesses.

The original audit is not imported or run. Literal tables are read with AST;
the plane formula is used to display all 60 local lattice DR slacks. This is
an informed source comparison, not a new optimization or blind review.
"""
import ast
import json
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path

base = Path(__file__).resolve().parent
tree = ast.parse((base / "original/audit_concave_potential.py").read_text())
literals = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {"F", "G", "PLANES", "POLICY"}:
                literals[target.id] = ast.literal_eval(node.value)
F, G, planes, policy = (literals[k] for k in ("F", "G", "PLANES", "POLICY"))
candidate = json.loads((base / "original/concave_potential_candidate.json").read_text())
f = {tuple(x["q"]): x["value"] for x in candidate["values"]}
g = {tuple(x["q"]): x["gradient"] for x in candidate["supergradients"]}
p = {tuple(x["counts"]): x["action"] for x in candidate["sigma"]}
assert len(f) == len(candidate["values"]) == 35
assert len(g) == len(candidate["supergradients"]) == 35
assert len(p) == len(candidate["sigma"]) == 10
assert set(f) == set(g) == set(F) == set(G)
assert p == policy
value_error = max(abs(f[q] - F[q] / 44) for q in F)
gradient_error = max(abs(g[q][a] - G[q][a] / 44) for q in G for a in range(3))
assert value_error < 1e-12 and gradient_error < 1e-12

def phi(q):
    return min(h + sum(a * b for a, b in zip(v, q)) for h, *v in planes)

def add(q, a):
    return tuple(v + (i == a) for i, v in enumerate(q))

pairs = list(combinations_with_replacement(range(3), 2))
dr_rows = []
for q in sorted(q for q in product(range(3), repeat=3) if sum(q) <= 2):
    slacks = [phi(add(q, a)) + phi(add(q, b)) - phi(q) - phi(add(add(q, a), b))
              for a, b in pairs]
    assert min(slacks) >= 0
    dr_rows.append({"q": q, "slacks": slacks})
assert all(phi(q) == F[q] for q in F)
report = {
    "scope": "complete frozen JSON comparison and exact DR table extraction; no LP run",
    "candidate_top_level_keys": list(candidate),
    "candidate_grid_points": len(f),
    "candidate_supergradient_points": len(g),
    "candidate_count_policy_states": len(p),
    "normalization_scale": 44,
    "max_float_value_error_vs_F_over_44": value_error,
    "max_float_gradient_error_vs_G_over_44": gradient_error,
    "policy_identical_to_exact_audit": p == policy,
    "candidate_actual_is_count_vector": candidate["actual"] == [0, 2, 1],
    "candidate_query": candidate["query"],
    "candidate_iteration_is_zero_based": candidate["iteration"],
    "candidate_float_gap": candidate["value"],
    "exact_normalized_gap": str(Fraction(2, 44)),
    "gap_float_error": abs(candidate["value"] - 2 / 44),
    "DR_column_pairs": pairs,
    "DR_rows": dr_rows,
    "all_35_exact_values": [{"q": q, "value": F[q]} for q in sorted(F, key=lambda q: (sum(q), q))],
}
print(json.dumps(report, ensure_ascii=False, indent=2))
