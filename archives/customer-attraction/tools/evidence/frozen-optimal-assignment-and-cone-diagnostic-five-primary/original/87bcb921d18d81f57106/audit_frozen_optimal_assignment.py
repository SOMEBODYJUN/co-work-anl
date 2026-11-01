"""Exact stored-target attack on the general FOMA candidate; no new SPE scan.

All history IC and frozen costs are reconstructed directly from unit-customer
types. The output only records these finite targets and makes no general claim.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[6]
SIMPLE = (
    "fractional_actual_load_failure", "worst_cce_welfare_failure",
    "portfolio_matching_failure", "prefix_balance_failure",
    "coverage_opportunity_failure", "collision_free_occupancy",
    "eight_cce_welfare_gap", "worst_pne_welfare_failure",
    "residual_counterexample", "aggregate_theta_failure",
    "individual_security_failure",
)
OLD_ACTOR = Path("research/workspaces/customer-attraction/") / (
    "R-d22a706a03c5499d941a6a97f94128a8/representation"
)
EMBEDDED = (
    "high_insertion_2cycle_348_exact", "terminal_pushforward_34_D_lt_C_exact",
)


def sources():
    for name in SIMPLE:
        ip = Path("examples/customer_attraction") / (name + ".json")
        cp = Path("evidence/certificates/customer_attraction") / (name + ".json")
        raw = json.loads((ROOT / cp).read_text())
        yield name, json.loads((ROOT / ip).read_text()), raw.get("strategy", raw), (ip, cp)
    for name in EMBEDDED:
        cp = OLD_ACTOR / (name + ".json")
        raw = json.loads((ROOT / cp).read_text())
        yield name, raw["instance"], raw["certificate"], (cp,)


def audit(name, instance, certificate, paths):
    m, k = instance["players"], len(instance["topics"])
    types = [(frozenset(row["topics"]), row.get("multiplicity", 1))
             for row in instance["customers"]]
    assert m >= 1 and k >= 1
    assert all(isinstance(n, int) and n > 0 for _, n in types)
    actions = {tuple(row["history"]): row["action"] for row in certificate["actions"]}
    assert len(actions) == sum(k ** i for i in range(m))

    def finish(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def utility(h, i):
        return sum((F(n, sum(a in mask for a in h))
                    for mask, n in types if h[i] in mask), F(0))

    def welfare(h):
        return sum(n for mask, n in types if any(a in mask for a in h))

    nodes = comparisons = 0
    for i in range(m):
        for h in product(range(k), repeat=i):
            assert h in actions and 0 <= actions[h] < k
            value = utility(finish(h), i)
            for a in range(k):
                assert value >= utility(finish(h + (a,)), i), (name, h, a)
                comparisons += 1
            nodes += 1

    z = finish(())
    W = welfare(z)
    actual = [utility(z, i) for i in range(m)]
    assert sum(actual) == W
    tuples = list(combinations_with_replacement(range(k), m))
    OPT = max(welfare(t) for t in tuples)
    optimal = [t for t in tuples if welfare(t) == OPT]
    costs = [[utility(z[:i] + (a,) + z[i + 1:], i) for a in range(k)]
             for i in range(m)]
    base = [sum((F(n, 1 + sum(a in mask for a in z))
                 for mask, n in types if topic in mask), F(0))
            for topic in range(k)]
    bonus = [[sum((F(n, c * (c + 1))
                   for mask, n in types
                   if z[i] in mask and a in mask
                   for c in [sum(b in mask for b in z)]), F(0))
              for a in range(k)] for i in range(m)]
    assert all(costs[i][a] == base[a] + bonus[i][a]
               for i in range(m) for a in range(k))

    rows = []
    cost_identity_checks = 0
    for t in optimal:
        assignments = []
        for p in sorted(set(permutations(t))):
            direct = sum((costs[i][a] for i, a in enumerate(p)), F(0))
            customer_cost = F(0)
            for mask, n in types:
                c = sum(a in mask for a in z)
                d = sum(a in mask for a in t)
                common_positions = sum(z[i] in mask and p[i] in mask for i in range(m))
                each = F(d) if c == 0 else F(d, c + 1) + F(common_positions, c * (c + 1))
                customer_cost += n * each
            assert direct == customer_cost
            assert OPT <= W + direct
            assignments.append((direct, p))
            cost_identity_checks += 1
        minimum, argmin = min(assignments)
        uniform = sum((x[0] for x in assignments), F(0)) / len(assignments)
        rows.append({"optimal_tuple": list(t), "minimum_cost": str(minimum),
                     "best_assignment": list(argmin), "uniform_cost": str(uniform),
                     "assignment_count": len(assignments), "K_le_W": minimum <= W})

    min_row = min(rows, key=lambda row: (F(row["minimum_cost"]), row["optimal_tuple"]))
    max_row = max(rows, key=lambda row: (F(row["minimum_cost"]), row["optimal_tuple"]))
    result = {"name": name, "players": m, "topic_count": k,
              "unit_customers": sum(n for _, n in types), "actual": list(z),
              "actual_payoffs": [str(x) for x in actual], "W": W, "OPT": OPT,
              "full_history_nodes": nodes, "SPE_comparisons_with_self": comparisons,
              "compared_multisets": len(tuples), "optimal_multiset_count": len(optimal),
              "cost_identity_checks": cost_identity_checks,
              "least_optimal_tuple_K": min_row["minimum_cost"],
              "greatest_optimal_tuple_K": max_row["minimum_cost"],
              "FOMA_EXISTS_on_this_target": any(row["K_le_W"] for row in rows),
              "FOMA_ALL_on_this_target": all(row["K_le_W"] for row in rows),
              "optimal_rows": rows,
              "source_sha256": {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                                for p in paths}}
    if name == "eight_cce_welfare_gap":
        assert tuple(z) == (0, 1, 1) and W == 6
        assert sum(costs[i][2] for i in range(m)) == 7
        assert min_row["minimum_cost"] == "16/3"
        assert min_row["uniform_cost"] == "58/9"
        result["unique_optimal_cost_matrix"] = [[str(costs[i][a]) for a in (1, 2, 3)]
                                               for i in range(m)]
        result["nonoptimal_repeated_222_cost"] = "7"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = [audit(*source) for source in sources()]
    out = {"status": "finite exact candidate attack only; general FOMA and HALF open",
           "new_instances_generated": 0, "targets": rows,
           "summary": {"target_count": len(rows),
                       "full_history_nodes": sum(r["full_history_nodes"] for r in rows),
                       "SPE_comparisons_with_self": sum(r["SPE_comparisons_with_self"] for r in rows),
                       "all_stored_targets_pass_FOMA_ALL": all(r["FOMA_ALL_on_this_target"] for r in rows)}}
    output = json.dumps(out, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
