"""Definition-level recovery of one old counterexample's free-column menus.

The full-p optimization is only for this existing instance, with matching
exact rational primal/dual verification. It proves no general AFC theorem.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def run():
    src = ROOT / "examples/customer_attraction/aggregate_theta_failure.json"
    cert = ROOT / "evidence/certificates/customer_attraction/aggregate_theta_failure.json"
    data, certificate = json.loads(src.read_text()), json.loads(cert.read_text())
    m, k = data["players"], len(data["topics"])
    policy = {tuple(r["history"]): r["action"]
              for r in certificate["strategy"]["actions"]}
    clients = [set(row["topics"]) for row in data["customers"]
               for _ in range(row["multiplicity"])]

    def leaf(h):
        h = list(h)
        while len(h) < m:
            h.append(policy[tuple(h)])
        return tuple(h)

    def query(a, opponents):
        return sum((F(1, 1 + sum(b in x for b in opponents))
                    for x in clients if a in x), F(0))

    def utility(z, i):
        return query(z[i], z[:i] + z[i + 1:])

    z = leaf(())
    ic = [utility(leaf(h), i) - utility(leaf(h + (a,)), i)
          for i in range(m) for h in product(range(k), repeat=i)
          for a in range(k)]
    assert min(ic) >= 0
    W = sum(utility(z, i) for i in range(m))
    menus, table = [], []
    for i in range(m):
        columns, matrix = [], []
        for b in range(k):
            q = leaf(z[:i] + (b,))
            v = q[:i] + q[i + 1:]
            columns.append({"action": b, "leaf": list(q), "opponents": list(v)})
            matrix.append([query(a, v) for a in range(k)])
        menus.append(columns)
        table.append(matrix)
    p_bad = [F(int(a in (2, 5)), 2) for a in range(k)]
    values = [[sum(p * v for p, v in zip(p_bad, col)) for col in matrix]
              for matrix in table]
    a_ub = []
    for i, matrix in enumerate(table):
        for col in matrix:
            a_ub.append([-float(x) for x in col] + [float(j == i) for j in range(m)])
    opt = linprog([0] * k + [-1] * m, A_ub=a_ub, b_ub=[0] * (m * k),
                  A_eq=[[1] * k + [0] * m], b_eq=[1],
                  bounds=[(0, None)] * k + [(None, None)] * m,
                  method="highs")
    assert opt.success
    p = [F(float(x)).limit_denominator(1000000) for x in opt.x[:k]]
    q_flat = [F(float(-x)).limit_denominator(1000000)
              for x in opt.ineqlin.marginals]
    q = [q_flat[i * k:(i + 1) * k] for i in range(m)]
    assert sum(p) == 1 and min(p) >= 0
    assert all(sum(qi) == 1 and min(qi) >= 0 for qi in q)
    h = [min(sum(pa * x for pa, x in zip(p, col)) for col in matrix)
         for matrix in table]
    dual_queries = [sum(q[i][b] * table[i][b][a]
                        for i in range(m) for b in range(k)) for a in range(k)]
    L = sum(h)
    assert max(dual_queries) == L
    report = {"scope": "existing 36-client complete SPE only",
              "source": str(src.relative_to(ROOT)),
              "strategy_source": str(cert.relative_to(ROOT)),
              "topic_labels": data["topics"], "actual_path": list(z),
              "actual_utilities": [str(utility(z, i)) for i in range(m)],
              "welfare": str(W), "full_IC_count": len(ic),
              "menus_by_position": menus,
              "query_rows_0_to_5_column_values":
                  [[[str(table[i][b][a]) for b in range(k)]
                    for a in range(k)] for i in range(m)],
              "bad_query": [str(x) for x in p_bad],
              "bad_query_values_by_position_and_column":
                  [[str(x) for x in row] for row in values],
              "bad_query_minima": [str(min(row)) for row in values],
              "bad_query_sum_minima": str(sum(min(row) for row in values)),
              "full_query_maximum_exact": str(L),
              "full_query_maximum_minus_welfare": str(L - W),
              "matching_primal_query": [str(x) for x in p],
              "matching_dual_columns": [[str(x) for x in row] for row in q],
              "matching_dual_query_caps": [str(x) for x in dual_queries]}
    dest = HERE / "old_36_free_columns_exact.json"
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ["actual_utilities", "welfare", "bad_query_minima",
                       "bad_query_sum_minima", "full_query_maximum_exact",
                       "full_query_maximum_minus_welfare", "matching_primal_query",
                       "matching_dual_columns"]}, indent=2))


if __name__ == "__main__":
    run()
