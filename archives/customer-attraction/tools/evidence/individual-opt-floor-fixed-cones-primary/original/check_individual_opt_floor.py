"""Freeze two targeted fixed-strategy tests of u_i >= OPT_m/(2m-1).

This does not search new games or prove an all-input result. Every nonempty
customer-interest type is free within each of two already published complete
strategy cones. Floating LP only proposes certificates; Fraction arithmetic
checks the returned primal and dual certificates independently of LP status.
Run from any directory. Output is written only inside this personal folder.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

import numpy as np
from scipy.optimize import linprog


HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "AGENTS.md").is_file())


def fraction(v):
    return F(float(v)).limit_denominator(10**7)


def test(source, players, tested_roles, expected_bounds):
    path = ROOT / source
    source_bytes = path.read_bytes()
    policy = {
        tuple(row["history"]): row["action"]
        for row in json.loads(source_bytes)["strategy"]["actions"]
    }
    topics = 6
    masks = tuple(range(1, 1 << topics))

    def leaf(history):
        history = tuple(history)
        while len(history) < players:
            history += (policy[history],)
        return history

    def utility(outcome, role):
        return tuple(
            F(1, sum((mask >> a) & 1 for a in outcome))
            if (mask >> outcome[role]) & 1 else F(0)
            for mask in masks
        )

    def coverage(outcome):
        return tuple(F(any((mask >> a) & 1 for a in outcome)) for mask in masks)

    rows = []
    row_labels = []
    for depth in range(players):
        for history in product(range(topics), repeat=depth):
            prescribed = utility(leaf(history), depth)
            for action in range(topics):
                deviating = utility(leaf(history + (action,)), depth)
                rows.append(tuple(a - b for a, b in zip(prescribed, deviating)))
                row_labels.append((history, action))

    actual = leaf(())
    matrix = np.array([[float(v) for v in row] for row in rows])
    result = {
        "source": source,
        "source_sha256": sha256(source_bytes).hexdigest(),
        "players": players,
        "topics": topics,
        "interest_types": len(masks),
        "ordered_nodes": len(policy),
        "whole_IC_rows_including_self": len(rows),
        "actual_path": actual,
        "normalization": "sum of all nonempty interest-type masses = 1",
        "scope": "one fixed complete strategy; arbitrary nonnegative type masses",
        "roles": [],
    }

    for role, bound in zip(tested_roles, expected_bounds):
        payoff = utility(actual, role)
        tested = []
        best_primal = None
        for comparison in combinations_with_replacement(range(topics), players):
            objective = tuple(a - (2 * players - 1) * b
                              for a, b in zip(coverage(comparison), payoff))
            lp = linprog(
                [-float(v) for v in objective],
                A_ub=-matrix, b_ub=np.zeros(len(rows)),
                A_eq=[np.ones(len(masks))], b_eq=[1.0],
                bounds=(0, None), method="highs",
            )
            if not lp.success:
                raise AssertionError(lp.message)
            weights = tuple(fraction(v) for v in lp.x)
            multipliers = tuple(fraction(-v) for v in lp.ineqlin.marginals)
            upper = fraction(-lp.eqlin.marginals[0])

            # Primal: nonnegative masses, one unit total, every ordered IC.
            assert min(weights) >= 0 and sum(weights) == 1
            assert all(sum(a * b for a, b in zip(row, weights)) >= 0 for row in rows)
            value = sum(a * b for a, b in zip(objective, weights))

            # Dual: upper*1 - Gamma^T*lambda >= objective, lambda >= 0.
            assert min(multipliers) >= 0
            slack = tuple(
                upper - objective[j] - sum(lam * rows[r][j]
                                          for r, lam in enumerate(multipliers) if lam)
                for j in range(len(masks))
            )
            assert min(slack) >= 0
            assert value == upper and upper <= bound
            if best_primal is None or value > best_primal["value"]:
                best_primal = {
                    "comparison": comparison,
                    "value": value,
                    "weights": [(mask, weight) for mask, weight in zip(masks, weights) if weight],
                }
            tested.append({
                "comparison": comparison,
                "exact_upper": str(upper),
                "dual": [
                    {"history": row_labels[r][0], "action": row_labels[r][1], "multiplier": str(lam)}
                    for r, lam in enumerate(multipliers) if lam
                ],
            })
        assert best_primal["value"] == bound
        best_primal["value"] = str(best_primal["value"])
        best_primal["weights"] = [(mask, str(weight)) for mask, weight in best_primal["weights"]]
        result["roles"].append({
            "role_one_based": role + 1,
            "exact_maximum_gap": str(bound),
            "attaining_primal": best_primal,
            "comparison_duals": tested,
        })
    return result


if __name__ == "__main__":
    result = {
        "candidate": "For every full-history pure SPE and player i: (2m-1) u_i >= OPT_m",
        "status": "Candidate not proved or falsified; only two fixed-strategy cone tests",
        "tests": [
            test("evidence/certificates/customer_attraction/individual_security_failure.json",
                 3, (0, 1, 2), (F(-1, 6), F(-1, 6), F(-1, 19))),
            test("evidence/certificates/customer_attraction/root_tax_failure.json",
                 4, (0,), (F(0),)),
        ],
    }
    output = HERE / "individual_opt_floor_fixed_cones.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(output), "exact_primal_dual_checks": "PASS",
                      "role_maxima": [[row["exact_maximum_gap"] for row in test["roles"]]
                                      for test in result["tests"]]}))
