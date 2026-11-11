#!/usr/bin/env python3
"""Build the exact eleven-weight cone from formulas, without optimization.

Only writes this directory. Original model/certificate/table are read-only.
The old eight-support dual is extended first; its feasibility closes the task.
No numerical solver, game-point input, Y/Z quotient, or parameter scan is used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
REPO = RUN.parents[2]
OLD = RUN / "early3_maxx_cone"
ORDER = ["alpha0", "sY", "sZ", "sT", "aY", "aZ", "aT", "delta",
         "eta1", "eta2", "eta3"]
COST = [F(1)] * 4 + [F(0)] * 7
KINDS = list(product(range(1, 4), range(3), *([range(2)] * 5)))


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), F(0))


def pair_coefficients(kind):
    n, k, x, y, z, t, q = kind
    d = n + x + y
    h = F(z, d + t) + F(t, d + z) + F(z, d * (d + 1))
    return [h - F(q + x, d) + F(q * x, d * (d + 1)),
            h - F(2 * q, d) + F(q, d * (d + 1)),
            h - F(2 * x, d) + F(x, d * (d + 1))]


def matrix_row(kind):
    n, k, x, y, z, t, q = kind
    g = [F(x, n + y + z + t) - F(x, n + 3),
         F(y - x, n + 3), F(z - x, n + 3), F(t - x, n + 3),
         F(y - x, n + k), F(z - x, n + k), F(t - x, n + k),
         F(q - t, n + x + y + z)]
    tp = pair_coefficients(kind)
    g += [-value for value in tp]
    rhs = q * (F(x, n + 3) + F(1 - x, n)) - F(x, n + 3)
    return g, rhs, tp


def reduced_base(n, x, m, t):
    if x == 0:
        return (F(2 * m, 3 * (n + 3)) + F(4 * t, n + 3)
                + F(m, n + 2) + F(1 - t, n + m) - F(1, n))
    return (F(15, n + m + t) + F(2 * m + 12 * t - 58, 3 * (n + 3))
            - F(2 - m, n) - F(t, n + 1 + m))


old_certificate = json.loads((OLD / "exact_certificate.json").read_text())
assert old_certificate["variable_order"] == ORDER[:8]
old_primal = list(map(F, old_certificate["primal"]))
assert old_primal == [F(15), F(2, 3), F(2, 3), F(4), F(1), F(1), F(0), F(1)]
primal = old_primal + [F(0)] * 3
dual = [F(0)] * 288
extension_rows = []
for entry in old_certificate["dual_nonzero"]:
    index = entry["index"]
    assert entry["type"] == list(KINDS[index])
    assert dual[index] == 0
    dual[index] = F(entry["lambda"])
    tp = pair_coefficients(KINDS[index])
    extension_rows.append({"index": index, "type": entry["type"],
                           "lambda": entry["lambda"], "T": list(map(str, tp)),
                           "weighted_T": list(map(str, [dual[index] * a for a in tp]))})
new_reduced_cost = [sum((F(row["weighted_T"][j]) for row in extension_rows), F(0))
                    for j in range(3)]
extension = {
    "stage": "Direct extension of original eight-support dual; before any new optimization",
    "optimizer_calls": 0, "rows": extension_rows,
    "new_columns_are_minus_T": True,
    "dual_new_column_sums": list(map(str, [-r for r in new_reduced_cost])),
    "new_dual_reduced_cost": list(map(str, new_reduced_cost)),
    "remains_dual_feasible": all(r >= 0 for r in new_reduced_cost)}
# Preserve and compare the result produced by the initial exact extension.
initial = HERE / "old_dual_extension.json"
if initial.exists():
    assert json.loads(initial.read_text()) == extension
else:
    save("old_dual_extension.json", extension)
assert extension["remains_dual_feasible"]
assert new_reduced_cost == [F(6), F(1, 3), F(139, 6)]

old_table = json.loads((OLD / "local_table_288.json").read_text())
assert len(old_table["rows"]) == 288
rows, matrix, rhs_vector, slacks = [], [], [], []
for index, kind in enumerate(KINDS):
    g, rhs, tp = matrix_row(kind)
    prior = old_table["rows"][index]
    assert prior["index"] == index and prior["type"] == list(kind)
    assert list(map(F, prior["G"])) == g[:8]
    assert F(prior["h"]) == rhs
    slack = dot(g, primal) - rhs
    assert slack == F(prior["optimal_E"]) >= 0
    rows.append({"index": index, "type": list(kind), "G": list(map(str, g)),
                 "h": str(rhs), "T": list(map(str, tp)), "optimal_E": str(slack)})
    matrix.append(g)
    rhs_vector.append(rhs)
    slacks.append(slack)

columns = [sum((dual[i] * matrix[i][j] for i in range(288)), F(0))
           for j in range(11)]
reduced_cost = [c - value for c, value in zip(COST, columns)]
objective = dot(COST, primal)
dual_objective = dot(dual, rhs_vector)
assert objective == dual_objective == F(61, 3)
assert reduced_cost == [F(0)] * 8 + new_reduced_cost
assert all(value >= 0 for value in reduced_cost)
assert all(multiplier * slack == 0 for multiplier, slack in zip(dual, slacks))
assert dot(reduced_cost, primal) == 0

save("local_table_288.json", {
    "scope": "Only the specified eleven global nonnegative weights and all 288 local types",
    "variable_order": ORDER,
    "type_order": ["n", "k", "x", "y", "z", "t", "q"],
    "enumeration": "product(range(1,4),range(3),range(2),range(2),range(2),range(2),range(2))",
    "constraint_orientation": "G*p >= h; p >= 0",
    "objective": [int(value) for value in COST],
    "pair_history": "h=(A1,A2,X,Y); d=n+x+y; Z and T are the two true tails",
    "yz_quotient_used": False, "rows": rows})
with (HERE / "local_table_288.csv").open("w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["index", "n", "k", "x", "y", "z", "t", "q"] + ORDER
                    + ["h", "T1", "T2", "T3", "E_optimal"])
    for row in rows:
        writer.writerow([row["index"]] + row["type"] + row["G"] + [row["h"]]
                        + row["T"] + [row["optimal_E"]])

base_rows = [{"x": x, "n": n,
              "values": [str(reduced_base(n, x, m, t)) for m, t in product(range(3), range(2))]}
             for x, n in product(range(2), range(1, 4))]
save("reduced_36_table.json", {
    "scope": "Only the exhibited optimum, where eta1=eta2=eta3=0; not a quotient of the eleven-weight cone",
    "columns_m_t": list(map(list, product(range(3), range(2)))), "rows": base_rows})

save("exact_certificate.json", {
    "claim": "Exact optimum of the specified eleven-weight pointwise cone only; no SPE sharpness claim",
    "variable_order": ORDER, "primal": list(map(str, primal)), "C": str(objective),
    "dual_nonzero": old_certificate["dual_nonzero"],
    "dual_column_sums": list(map(str, columns)),
    "dual_reduced_cost": list(map(str, reduced_cost)),
    "dual_objective": str(dual_objective), "exact_primal_dual_gap": "0",
    "zero_primal_slack_indices": [i for i, value in enumerate(slacks) if value == 0],
    "positive_primal_slack_min": str(min(value for value in slacks if value > 0)),
    "lower_bound_identity": {
        "form": "C-61/3=sum_i lambda_i E_i+6 eta1+(1/3) eta2+(139/6) eta3",
        "integer_form": "6C-122=76E1+12E22+12E26+32E34+72E66+36E69+36E73+120E220+36eta1+2eta2+139eta3",
        "scale": 6,
        "scaled_dual_support": [{"index": entry["index"],
                                  "coefficient": str(6 * F(entry["lambda"]))}
                                 for entry in old_certificate["dual_nonzero"]],
        "scaled_eta_coefficients": ["36", "2", "139"]},
    "optimal_pair_weights_forced_zero": ["eta1", "eta2", "eta3"],
    "optimizer": {"calls": 0, "reason": "The original eight-support dual is feasible after adding all three columns"}})

save("optimization_log.json", {
    "optimizer_calls": 0, "numerical_optimization_performed": False,
    "reason": "Direct exact old-dual extension has new reduced costs (6,1/3,139/6), all positive",
    "conditional_288x11_lp_needed": False, "numerical_input": None, "numerical_output": None,
    "exact_input": "local_table_288.json", "exact_output": "exact_certificate.json",
    "game_point_files_read": [], "additional_queries_scanned": [],
    "fixed_23676_system_touched": False})

sources = [RUN / "early3_maxx_cone.md", OLD / "exact_certificate.json",
           OLD / "verify_independent.py", OLD / "local_table_288.json",
           RUN / "maxb_h3_pair_strength.md",
           REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md"]
save("source_manifest.json", {
    "source_role": "Read-only mathematical sources; all writes remain in early3_pair_cone and its sibling manuscript",
    "sources": [{"path": str(path.relative_to(REPO)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                 "bytes": path.stat().st_size} for path in sources],
    "original_eight_coefficients_rechecked": 2304,
    "original_288_rhs_and_optimal_slacks_rechecked": True,
    "original_checker_executed": False,
    "original_checker_note": "Read in full; not executed because it writes outside this task's authorized directory"})
print(json.dumps({"status": "PASS", "types": 288, "weights": 11,
                  "C": str(objective), "new_dual_reduced_cost": list(map(str, new_reduced_cost)),
                  "optimizer_calls": 0, "zero_slacks": sum(value == 0 for value in slacks)}, indent=2))
