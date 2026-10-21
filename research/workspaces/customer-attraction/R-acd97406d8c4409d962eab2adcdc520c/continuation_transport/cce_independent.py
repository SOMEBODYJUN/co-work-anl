"""Independent replay of the full-history SPE / every-static-CCE separation.

No project model, cone, generator, solver, or author audit code is imported.
All stated certificate checks use Fraction; scipy only proposes CCE supports.
Clients are expanded into different unit-value individuals before payoffs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def exact_primal(support, active, regrets):
    rows = [[F(1) for _ in support]]
    rhs = [F(1)]
    for a in active:
        rows.append([regrets[z][a] for z in support]); rhs.append(F(0))
    matrix = [row + [b] for row, b in zip(rows, rhs)]
    pivot = 0
    where = {}
    for col in range(len(support)):
        selected = next((i for i in range(pivot, len(matrix)) if matrix[i][col]), None)
        if selected is None:
            continue
        matrix[pivot], matrix[selected] = matrix[selected], matrix[pivot]
        denominator = matrix[pivot][col]
        matrix[pivot] = [x / denominator for x in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot and matrix[i][col]:
                multiplier = matrix[i][col]
                matrix[i] = [x - multiplier * y for x, y in zip(matrix[i], matrix[pivot])]
        where[col] = pivot
        pivot += 1
    assert len(where) == len(support), "Primal basis is not unique."
    assert all(any(row[:-1]) or not row[-1] for row in matrix)
    return [matrix[where[col]][-1] for col in range(len(support))]


def audit(path):
    d = json.loads(Path(path).read_text())
    n, p = 3, 5
    weights = {int(k): F(v) for k, v in d["weights"].items()}
    assert all(w.denominator == 1 and w >= 0 for w in weights.values())
    clients = [frozenset(a for a in range(p) if mask & (1 << a))
               for mask, w in weights.items() for _ in range(w.numerator)]
    themes = [frozenset(i for i, likes in enumerate(clients) if a in likes)
              for a in range(p)]
    assert len(set(themes)) == p, "Themes should be different sets, even without labels."
    sigma = {tuple(h): int(a) for h, a in d["actions"]}
    expected_histories = {h for k in range(n) for h in product(range(p), repeat=k)}
    assert set(sigma) == expected_histories

    def play(h):
        z = tuple(h)
        while len(z) < n:
            z += (sigma[z],)
        return z

    def payoff(z, i):
        # Directly enumerate individual clients, not customer types or count formulas.
        return sum((F(1, sum(x in themes[a] for a in z))
                    for x in themes[z[i]]), F(0))

    def welfare(z):
        return F(len(set().union(*(themes[a] for a in z))))

    rows, slack_values = [], []
    for h in sorted(expected_histories, key=lambda x: (len(x), x)):
        actual = play(h)
        values = []
        for a in range(p):
            alt = play(h + (a,))
            slack = payoff(actual, len(h)) - payoff(alt, len(h))
            assert slack >= 0, (h, a, actual, alt, slack)
            slack_values.append(slack)
            values.append(str(payoff(alt, len(h))))
        rows.append({"history": list(h), "action": sigma[h],
                     "deviation_values": values})

    ordered = list(product(range(p), repeat=n))
    def regret(z, a):
        return sum((payoff(z, i) - payoff(z[:i] + (a,) + z[i + 1:], i)
                    for i in range(n)), F(0))
    regrets = {z: tuple(regret(z, a) for a in range(p)) for z in ordered}
    fixed_lambda = [F(v) for v in d["lambda"]]
    fixed_bound = min(welfare(z) - sum((fixed_lambda[a] * regrets[z][a]
                                      for a in range(p)), F(0)) for z in ordered)
    assert fixed_bound == F(d["CCE_lower"])

    # Recompute a minimum-CCE primal from scratch on unordered profiles.
    # Randomly permuting players lifts each count profile to an ordered CCE.
    counts = list(combinations_with_replacement(range(p), n))
    A = np.array([[-float(regrets[z][a]) for z in counts] for a in range(p)])
    obj = np.array([float(welfare(z)) for z in counts])
    result = linprog(obj, A_ub=A, b_ub=np.zeros(p),
                     A_eq=np.ones((1, len(counts))), b_eq=[1],
                     bounds=(0, None), method="highs")
    assert result.success
    support = [z for z, x in zip(counts, result.x) if x > 1e-8]
    active = [a for a, slack in enumerate(result.ineqlin.residual) if abs(slack) < 1e-8]
    probabilities = exact_primal(support, active, regrets)
    assert all(prob >= 0 for prob in probabilities) and sum(probabilities) == 1
    count_regret = [sum((prob * regrets[z][a] for z, prob in zip(support, probabilities)), F(0))
                    for a in range(p)]
    assert min(count_regret) >= 0
    primal_value = sum((prob * welfare(z) for z, prob in zip(support, probabilities)), F(0))

    # Propose a dual, then verify all 125 ordered columns using exact arithmetic.
    dual_lambda = [F(float(-x)).limit_denominator(10**7) for x in result.ineqlin.marginals]
    assert min(dual_lambda) >= 0
    dual_columns = {z: welfare(z) - sum((dual_lambda[a] * regrets[z][a]
                                       for a in range(p)), F(0)) for z in ordered}
    dual_value = min(dual_columns.values())
    assert primal_value == dual_value

    simple_lambda = [F(0), F(1, 5), F(1, 5), F(1, 5), F(2, 5)]
    simple_columns = {z: welfare(z) - sum((simple_lambda[a] * regrets[z][a]
                                         for a in range(p)), F(0)) for z in ordered}
    simple_value = min(simple_columns.values())
    assert simple_value == F(137, 15)
    # Independent inverse-load expression for the same aggregate dual.
    inverse_formula_checks = 0
    for z in ordered:
        inverse = F(0)
        for likes in clients:
            load = sum(a in likes for a in z)
            lambda_type = sum((simple_lambda[a] for a in likes), F(0))
            inverse += lambda_type * (F(n) if load == 0 else F(n + 1, load + 1))
        assert inverse == simple_columns[z]
        inverse_formula_checks += 1
    background = (0, 4)
    query_values = [payoff(background + (a,), 2) for a in range(p)]
    assert max(query_values) == 3

    # Lift the primal explicitly and verify all fifteen individual CCE inequalities.
    lifted = {}
    for z, prob in zip(support, probabilities):
        distinct = set(permutations(z))
        for leaf in distinct:
            lifted[leaf] = lifted.get(leaf, F(0)) + prob / len(distinct)
    assert sum(lifted.values()) == 1
    individual_regrets = {}
    for i in range(n):
        for a in range(p):
            value = sum((prob * (payoff(z, i) - payoff(z[:i] + (a,) + z[i + 1:], i))
                         for z, prob in lifted.items()), F(0))
            assert value >= 0
            individual_regrets[i, a] = value
    assert sum((prob * welfare(z) for z, prob in lifted.items()), F(0)) == primal_value
    root = play(())
    W = welfare(root)
    opt = max(map(welfare, ordered))
    assert W == F(d["W"]) and primal_value > W
    return {
        "input": str(path), "scope": "independent exact verification, not general half coverage",
        "unit_clients": len(clients), "theme_client_ids": [sorted(t) for t in themes],
        "players": n, "topics": p, "histories": len(sigma),
        "SPE_comparisons": len(slack_values), "min_SPE_slack": str(min(slack_values)),
        "root": list(root), "root_utilities": [str(payoff(root, i)) for i in range(n)],
        "root_welfare": str(W), "OPT": str(opt), "fixed_dual_lower": str(fixed_bound),
        "optimized_CCE_min": str(primal_value), "gap": str(primal_value - W),
        "optimized_dual_lambda": list(map(str, dual_lambda)),
        "dual_ordered_columns_checked": len(ordered),
        "dual_tight_ordered_columns": sum(v == dual_value for v in dual_columns.values()),
        "simple_dual_lambda": list(map(str, simple_lambda)),
        "simple_dual_lower": str(simple_value), "simple_dual_gap": str(simple_value - W),
        "simple_inverse_load_formula_checks": inverse_formula_checks,
        "safe_static_background": list(background),
        "safe_static_query_values": list(map(str, query_values)),
        "CCE_count_support": [{"profile": list(z), "probability": str(prob),
                               "welfare": str(welfare(z))}
                              for z, prob in zip(support, probabilities)],
        "count_regrets": list(map(str, count_regret)),
        "lifted_ordered_support": len(lifted), "individual_CCE_constraints_checked": 15,
        "min_individual_CCE_regret": str(min(individual_regrets.values())),
        "SPE_rows": rows,
        "dual_columns": [{"profile": list(z), "adjusted_welfare": str(dual_columns[z]),
                          "slack": str(dual_columns[z] - dual_value)} for z in counts]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    out = audit(args.input)
    rendered = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with open(args.output, "x") as f:
            f.write(rendered)
    print(rendered)
