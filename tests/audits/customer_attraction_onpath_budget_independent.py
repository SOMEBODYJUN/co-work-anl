#!/usr/bin/env python3
"""Independent unit-customer audit of the existing 36-customer budget failure.

No project module or uploaded verifier is imported. The instance and all ordered
history actions are reconstructed from the mathematical construction. Optional
--repo checks that the existing frozen JSON stores exactly the same objects.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path


def construction():
    X, Y = range(3), range(3, 6)
    weights = {frozenset((x, y)): 1 for x in X for y in Y}
    weights.update({frozenset(I + J): 3
                    for I in combinations(X, 2) for J in combinations(Y, 2)})
    customers = tuple(T for T, multiplicity in weights.items()
                      for _ in range(multiplicity))

    def action(h):
        if not h:
            return 0
        if len(h) == 1:
            return 3 if h[0] < 3 else 0
        group = X if h[1] < 3 else Y
        return min(a for a in group if a not in h)

    histories = tuple(h for k in range(3)
                      for h in product(range(6), repeat=k))
    policy = {h: action(h) for h in histories}
    return weights, customers, histories, policy


def main():
    parser = ArgumentParser()
    parser.add_argument("--repo", type=Path)
    args = parser.parse_args()
    weights, customers, histories, policy = construction()
    topics = tuple(frozenset(i for i, T in enumerate(customers) if a in T)
                   for a in range(6))
    assert len(customers) == 36 and len(set(topics)) == 6
    assert len(histories) == len(policy) == 43

    if args.repo:
        example = json.loads((args.repo / "examples/customer_attraction/"
                             "aggregate_theta_failure.json").read_text())
        frozen_weights = {frozenset(row["topics"]): row["multiplicity"]
                          for row in example["customers"]}
        assert example["topics"] == ["X0", "X1", "X2", "Y0", "Y1", "Y2"]
        assert frozen_weights == weights
        frozen = json.loads((args.repo / "evidence/certificates/customer_attraction/"
                            "aggregate_theta_failure.json").read_text())
        frozen_policy = {tuple(row["history"]): row["action"]
                         for row in frozen["strategy"]["actions"]}
        assert frozen_policy == policy

    def terminal(h):
        while len(h) < 3:
            h += (policy[h],)
        return h

    def utilities(z):
        loads = tuple(sum(a in T for a in z) for T in customers)
        return tuple(sum((F(1, loads[x]) for x in topics[a]), F(0))
                     for a in z)

    def f(a, rivals):
        return utilities((a,) + tuple(rivals))[0]

    comparisons = 0
    for h in histories:
        i = len(h)
        current = utilities(terminal(h))[i]
        for a in range(6):
            deviated = utilities(terminal(h + (a,)))[i]
            assert current >= deviated, (h, a, current, deviated)
            comparisons += 1
    assert comparisons == 258

    z = terminal(())
    u = utilities(z)
    W = len(frozenset().union(*(topics[a] for a in z)))
    assert z == (0, 3, 4) and u == (F(10), F(12), F(12))
    assert sum(u) == W == 34

    # The budget distribution is supported on the two unused labels X2, Y2.
    p = {2: F(1, 2), 5: F(1, 2)}
    rows = []
    for i in range(3):
        h = z[:i]
        rivals = {}
        for a in p:
            zz = terminal(h + (a,))
            rivals[a] = zz[:i] + zz[i + 1:]
        matrix = [[f(a, rivals[b]) for b in p] for a in p]
        D = sum((p[a] * f(a, rivals[a]) for a in p), F(0))
        C = sum((p[a] * p[b] * f(a, rivals[b])
                 for a in p for b in p), F(0))
        rows.append({"player": i + 1, "history": h,
                     "rivals_by_query": {str(a): rivals[a] for a in p},
                     "matrix_rows_cols_X2_Y2": [[str(v) for v in row]
                                                for row in matrix],
                     "u": u[i], "D": D, "C": C,
                     "kappa": D - C, "e": u[i] - D})
    expected = [(F(10), F(11), F(-1), F(0)),
                (F(12), F(23, 2), F(1, 2), F(0)),
                (F(12), F(12), F(0), F(0))]
    assert [(r["D"], r["C"], r["kappa"], r["e"])
            for r in rows] == expected
    aggregate_kappa = sum((r["kappa"] for r in rows), F(0))
    aggregate_slack = sum((r["e"] for r in rows), F(0))
    budget = F(W) - sum((r["C"] for r in rows), F(0))
    assert aggregate_kappa == budget == F(-1, 2)
    assert aggregate_slack == 0
    assert budget == aggregate_kappa + aggregate_slack

    # Independent exact certificates for the unrestricted static value v_3=10.
    backgrounds = tuple(product(range(6), repeat=2))
    primary = [sum((f(a, B) for a in range(6)), F(0)) / 6
               for B in backgrounds]
    dual_support = tuple(combinations(range(3), 2)) + tuple(combinations(range(3, 6), 2))
    dual = [sum((f(a, B) for B in dual_support), F(0)) / 6
            for a in range(6)]
    assert min(primary) == max(dual) == F(10)
    assert all(value == 10 for value in dual)
    assert F(W) - 3 * min(primary) == 4

    def encode(value):
        if isinstance(value, F):
            return str(value)
        raise TypeError(type(value).__name__)

    print(json.dumps({
        "claim": "CA-ONPATH-DECOUPLED-BUDGET-NO",
        "unit_customers": 36, "topic_labels": ["X0", "X1", "X2", "Y0", "Y1", "Y2"],
        "budget_p": {"X2": "1/2", "Y2": "1/2"},
        "ordered_histories": 43, "exact_action_comparisons": comparisons,
        "same_as_frozen_repo_certificate": bool(args.repo),
        "outcome": z, "utilities": u, "W": W, "rows": rows,
        "aggregate_decorrelation": aggregate_kappa,
        "aggregate_incentive_slack": aggregate_slack,
        "GB_left_side": budget, "v_3": min(primary), "W_minus_3v_3": F(4),
        "interpretation": "GB is false; BR and half coverage are not refuted."
    }, default=encode, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
