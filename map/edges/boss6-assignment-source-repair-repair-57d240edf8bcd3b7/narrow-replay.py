#!/usr/bin/env python3
"""Recheck one saved witness's acceptance formulas, without an SPE/LP rerun.

Usage: python -B narrow-replay.py /absolute/read-only/clone > narrow-audit.json
Only the root continuation and nine actual-prefix query continuations are used.
The complete 43-history/258-IC certificate is reused from its pinned theorem
and original report. This program neither enumerates that tree nor verifies it.
"""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import sys


def main():
    root = Path(sys.argv[1]).resolve()
    relative = "archives/customer-attraction/tools/evidence/dynamic-exchange/original/"
    expected = {
        "assignment_instance.json": "2ae935f6980037f3526eee447021a6e2d8d5987e0bb2b2c31d4017afad7126c4",
        "assignment_full_policy.json": "1c59b0406e8fdd56e01fc4a2d1c03b9dd15a9aefc0748a556fb08cf593fa27ac",
        "assignment_exact_audit.json": "82dc1b7fb23311983fe67f0b794f1a0a36e991f3a870897752eb07be307d799b",
    }
    loaded = {}
    refs = []
    for name, digest in expected.items():
        path = relative + name
        data = (root / path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest, path
        loaded[name] = json.loads(data)
        refs.append({"path": path, "sha256": digest})
    instance = loaded["assignment_instance.json"]
    policy_record = loaded["assignment_full_policy.json"]
    saved = loaded["assignment_exact_audit.json"]
    customers = [(frozenset(r["topics"]), r["multiplicity"])
                 for r in instance["customers"]]
    policy = policy_record["policy"]
    actual = tuple(policy_record["actual"])
    optimum = (1, 2, 5)
    assert instance["players"] == 3 and len(instance["topics"]) == 6
    assert len(customers) == 63 and len(policy) == 43
    assert sum(w for _, w in customers) == 1953
    assert min(w for _, w in customers) == 1
    assert max(w for _, w in customers) == 61

    def continue_policy(prefix):
        history = tuple(prefix)
        while len(history) < 3:
            history += (policy[",".join(map(str, history))],)
        return history

    def payoff(terminal, player):
        return sum((Fraction(weight, sum(a in interest for a in terminal))
                    for interest, weight in customers
                    if terminal[player] in interest), Fraction())

    def cover(support):
        return sum(weight for interest, weight in customers
                   if interest.intersection(support))

    assert continue_policy(()) == actual == (0, 3, 4)
    payoffs = [payoff(actual, i) for i in range(3)]
    assert [str(x) for x in payoffs] == saved["payoffs"]
    welfare = sum(payoffs)
    assert welfare == saved["W"] == cover(actual) == 1735

    # Twenty static comparison supports, not a game-tree enumeration.
    coverage = {",".join(map(str, s)): cover(s)
                for s in combinations(range(6), 3)}
    assert max(coverage.values()) == saved["OPT"] == 1740
    assert [s for s, v in coverage.items() if v == 1740] == ["1,2,5"]
    # Every label has positive singleton-only clients. A support of size < 3
    # strictly increases coverage when any missing label is added. A repeated
    # three-slot tuple therefore cannot attain OPT. No repeated tuple scan.
    singleton_masses = {
        next(iter(s)): w for s, w in customers if len(s) == 1
    }
    assert len(singleton_masses) == 6 and min(singleton_masses.values()) > 0

    frozen = [[payoff(actual[:i] + (a,) + actual[i + 1:], i)
               for a in optimum] for i in range(3)]
    query_terminals = [[continue_policy(actual[:i] + (a,))
                        for a in optimum] for i in range(3)]
    real = [[payoff(query_terminals[i][j], i)
             for j in range(3)] for i in range(3)]
    frozen_costs = {}
    real_costs = {}
    for perm in permutations(optimum):
        key = ",".join(map(str, perm))
        frozen_costs[key] = sum((frozen[i][optimum.index(perm[i])]
                                 for i in range(3)), Fraction())
        real_costs[key] = sum((real[i][optimum.index(perm[i])]
                               for i in range(3)), Fraction())
    assert {k: str(v) for k, v in frozen_costs.items()} == saved["assignment_costs"]
    assert min(frozen_costs.values()) == 1736
    assert max(real_costs.values()) == min(real_costs.values()) == 1734
    scale = Fraction(1, 1735)
    t = Fraction(1, 1735)
    assert welfare * scale == 1
    assert min(frozen_costs.values()) * scale == 1 + t
    assert all(v * scale >= 1 + t for v in frozen_costs.values())
    assert max(coverage.values()) - welfare == 5
    assert 2 * welfare - max(coverage.values()) == 1730

    def matrix_strings(matrix):
        return [[str(v) for v in row] for row in matrix]

    result = {
        "schema": 1,
        "purpose": "Same-input exact acceptance-formula regression only",
        "executed_scope": {
            "static_three_label_supports": 20,
            "frozen_cost_entries": 9,
            "frozen_assignments": 6,
            "true_actual_prefix_query_entries": 9,
            "true_assignments": 6,
            "full_history_IC_recomputed": False,
            "LP_or_original_audit_or_sixteen_policy_probe_executed": False,
        },
        "pinned_input_refs": refs,
        "customer_count": 1953,
        "type_count": 63,
        "policy_row_count_structure_only": 43,
        "actual": list(actual),
        "actual_payoffs": [str(v) for v in payoffs],
        "actual_welfare": str(welfare),
        "reused_complete_SPE_certificate": {
            "full_histories": saved["full_histories"],
            "full_comparisons": saved["full_comparisons"],
            "minimum_SPE_slack": saved["minimum_SPE_slack"],
            "basis": "Pinned original report and proved v5 source; not freshly recomputed",
        },
        "all_twenty_support_coverages": coverage,
        "unique_optimal_support": list(optimum),
        "optimum_coverage": 1740,
        "repeated_optimal_tuple_excluded": True,
        "repeated_tuple_exclusion_reason": "All six private singleton types have positive mass; any support with fewer than three labels can be strictly enlarged.",
        "frozen_matrix": matrix_strings(frozen),
        "frozen_assignment_costs": {k: str(v) for k, v in frozen_costs.items()},
        "true_query_terminals": [[list(h) for h in row] for row in query_terminals],
        "true_query_matrix": matrix_strings(real),
        "true_assignment_costs": {k: str(v) for k, v in real_costs.items()},
        "normalization": {
            "customer_scale": str(scale),
            "W": "1",
            "t": str(t),
            "min_frozen_cost": str(min(frozen_costs.values()) * scale),
            "all_six_frozen_constraints_exact": True,
            "all_optimality_constraints_preserved": True,
            "true_IC_preservation": "Every original true-IC slack is linear in customer mass, so scaling by positive 1/1735 preserves it; full-IC validity is reused from the complete certificate.",
        },
        "true_best_matching": "1734",
        "net_gap": "5",
        "half_margin": "1730",
        "conclusion": "The witness meets the probe's exact acceptance inequalities. It refutes the strong frozen budget only; it is neither a true-net-matching counterexample nor a half-coverage counterexample.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
