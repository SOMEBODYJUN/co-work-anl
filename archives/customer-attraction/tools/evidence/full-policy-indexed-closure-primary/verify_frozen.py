"""Independent exact audit of the saved seven-label full-policy witness.

Reads all fields and action records; does not import the original search,
recovery helper, canonical package, NumPy/SciPy, or any outcome-set solver.
The eight historical round records lack their intermediate weights/policies.
Their rational arithmetic and field contracts are checked, not fabricated.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb, isfinite, lcm
from pathlib import Path
import hashlib
import json
import platform
import sys


def integer(x, minimum=0):
    assert isinstance(x, int) and not isinstance(x, bool) and x >= minimum
    return x


def read(path):
    def invalid(token):
        raise ValueError(f"nonfinite JSON number {token}")
    return json.loads(path.read_text(), parse_constant=invalid)


def main():
    original = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "original"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "verification.json"
    report = read(original / "full_policy_p7_m5.json")
    instance = read(original / "full_policy_p7_m5_instance.json")
    certificate = read(original / "full_policy_p7_m5_certificate.json")
    assert set(instance) == {"topics", "customers", "players"}
    assert instance["topics"] == [f"T{i}" for i in range(7)]
    m = integer(instance["players"], 1)
    p = len(instance["topics"])
    assert (m, p) == (5, 7)
    customers = []
    for item in instance["customers"]:
        assert set(item) == {"topics", "multiplicity"}
        liked = tuple(item["topics"])
        assert liked == tuple(sorted(set(liked))) and liked
        assert all(integer(a) < p for a in liked)
        customers.append((liked, integer(item["multiplicity"], 1)))
    assert customers == [((0,), 5)] + [((a,), 1) for a in range(1, p)]
    assert set(certificate) == {"terminal_counts", "actions"}
    declared = tuple(certificate["terminal_counts"])
    assert len(declared) == p and sum(map(integer, declared)) == m
    policy = {}
    supplied_order = []
    for item in certificate["actions"]:
        assert set(item) == {"history", "action"}
        h = tuple(item["history"])
        assert len(h) < m and all(integer(a) < p for a in h)
        a = integer(item["action"])
        assert a < p and h not in policy
        policy[h] = a
        supplied_order.append(h)
    expected = [h for t in range(m) for h in product(range(p), repeat=t)]
    assert supplied_order == expected and len(policy) == 2801
    assert all(a == 0 for a in policy.values())

    @lru_cache(None)
    def utility(counts, action):
        return sum((F(n, sum(counts[a] for a in liked))
                    for liked, n in customers if action in liked), F(0))

    def welfare(counts):
        return sum(n for liked, n in customers if any(counts[a] for a in liked))

    level_histories = Counter()
    strict = Counter()
    ties = Counter()
    slack_histogram = Counter()
    terminal = {}
    leaves = 0
    comparisons = 0
    self_comparisons = 0

    def tree(h):
        nonlocal leaves, comparisons, self_comparisons
        if len(h) == m:
            leaves += 1
            result = tuple(h.count(a) for a in range(p))
            terminal[h] = result
            return result, h
        branches = [tree(h + (a,)) for a in range(p)]
        chosen = policy[h]
        actual, actual_path = branches[chosen]
        level_histories[len(h)] += 1
        terminal[h] = actual
        for a, (counts, _) in enumerate(branches):
            slack = utility(actual, chosen) - utility(counts, a)
            assert slack >= 0, (h, chosen, a, slack)
            if a == chosen:
                self_comparisons += 1
                assert slack == 0
            else:
                comparisons += 1
                slack_histogram[slack] += 1
                (strict if slack else ties)[len(h)] += 1
        return actual, actual_path

    actual, actual_path = tree(())
    assert actual == declared == (5, 0, 0, 0, 0, 0, 0)
    assert leaves == 16807 and comparisons == 16806 and self_comparisons == 2801
    # All 127 possible interest types, not just the seven positive types.
    scale = lcm(*range(1, m + 1))
    masks = tuple(range(1, 1 << p))
    masses = {sum(1 << a for a in liked): n for liked, n in customers}

    @lru_cache(None)
    def coefficients(counts, action):
        out = []
        for mask in masks:
            if not (mask >> action & 1):
                out.append(0)
            else:
                load = sum(counts[a] for a in range(p) if mask >> a & 1)
                assert load > 0 and scale % load == 0
                out.append(scale // load)
        return tuple(out)

    G = set()
    generated_rows = 0
    analytical_rows = 0
    for h in expected:
        chosen = policy[h]
        lhs = coefficients(terminal[h], chosen)
        b = h.count(0)
        remaining = m - len(h)
        prescribed = F(5, b + remaining)
        assert prescribed >= 1
        for a in range(p):
            analytical = prescribed if a == 0 else F(1, h.count(a) + 1)
            assert prescribed >= analytical
            analytical_rows += 1
            if a != chosen:
                rhs = coefficients(terminal[h + (a,)], a)
                row = tuple(u - v for u, v in zip(lhs, rhs))
                generated_rows += 1
                if any(row):
                    G.add(row)
    assert generated_rows == comparisons and len(G) == 1260
    cone_slacks = [sum(coef * masses.get(mask, 0) for coef, mask in zip(row, masks))
                   for row in G]
    assert min(cone_slacks) == 0
    all_portfolios = []
    for size in range(min(p, m) + 1):
        for selected in combinations(range(p), size):
            counts = tuple(int(a in selected) for a in range(p))
            all_portfolios.append((welfare(counts), selected))
    W = welfare(actual)
    optimum = max(value for value, _ in all_portfolios)
    ratio = F(optimum, W)
    assert (W, optimum, ratio) == (5, 9, F(9, 5))
    assert sum(n for _, n in customers) == 11
    coverages = [tuple(i for i, (liked, _) in enumerate(customers) if a in liked) for a in range(p)]
    assert len(set(coverages)) == p and all(coverages)

    assert set(report) == {"status", "p", "m", "seeds", "iterations", "random_seed",
                           "best_verified_ratio_at_least", "half_counterexample_found",
                           "rounds", "cone_optimality_certified", "exact_cone_ratio_meaning"}
    assert report["status"] == "finite exact verified full-policy search; no general theorem"
    assert report["exact_cone_ratio_meaning"] == "exact attained feasible ratio; not a certified LP optimum"
    assert (integer(report["p"]), integer(report["m"]), integer(report["seeds"]),
            integer(report["iterations"]), integer(report["random_seed"])) == (7, 5, 3, 3, 9051284)
    assert report["half_counterexample_found"] is False
    assert report["cone_optimality_certified"] is False
    assert F(report["best_verified_ratio_at_least"]) == ratio
    expected_rounds = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
    assert len(report["rounds"]) == len(expected_rounds)
    record_audit = []
    row_keys = {"seed", "iteration", "initial_exact_ratio", "initial_welfare",
                "initial_optimum", "count_states", "unique_full_tree_deviation_rows",
                "full_history_nodes", "fixed_path_counts", "chosen_comparison_support",
                "exact_cone_ratio", "floating_cone_ratio", "minimum_exact_cone_slack",
                "certificate_verified"}
    for rec, (seed, iteration) in zip(report["rounds"], expected_rounds):
        assert set(rec) == row_keys
        assert (integer(rec["seed"]), integer(rec["iteration"])) == (seed, iteration)
        initial_welfare = integer(rec["initial_welfare"], 1)
        initial_optimum = integer(rec["initial_optimum"], 1)
        initial_ratio = F(rec["initial_exact_ratio"])
        attained = F(rec["exact_cone_ratio"])
        assert initial_ratio == F(initial_optimum, initial_welfare)
        assert attained >= initial_ratio and attained <= ratio
        assert integer(rec["count_states"]) == comb(p + m, p) == 792
        assert integer(rec["full_history_nodes"]) == len(policy)
        rows = integer(rec["unique_full_tree_deviation_rows"], 1)
        assert rows <= comparisons
        counts = tuple(rec["fixed_path_counts"])
        assert len(counts) == p and sum(map(integer, counts)) == m
        selected = tuple(rec["chosen_comparison_support"])
        assert len(selected) == m and selected == tuple(sorted(set(selected)))
        assert all(integer(a) < p for a in selected)
        assert F(rec["minimum_exact_cone_slack"]) == 0
        assert rec["certificate_verified"] is True
        assert isinstance(rec["floating_cone_ratio"], (float, int))
        assert isfinite(rec["floating_cone_ratio"])
        assert abs(float(attained) - rec["floating_cone_ratio"]) < 1e-10
        record_audit.append({"seed": seed, "iteration": iteration,
                             "initial_ratio_arithmetic": str(initial_ratio),
                             "reported_attained_comparison_ratio": str(attained),
                             "reported_unique_IC_rows": rows,
                             "all_fields_read": True,
                             "scope": "historical field/arithmetic consistency; intermediate mass/policy absent"})
    first = report["rounds"][0]
    assert first["fixed_path_counts"] == list(actual)
    assert first["unique_full_tree_deviation_rows"] == len(G)
    selected = first["chosen_comparison_support"]
    assert F(welfare(tuple(int(a in selected) for a in range(p))), W) == ratio
    result = {
        "scope": "Saved original full policy exactly checked; eight historical rounds fully read but not rediscovered.",
        "python": platform.python_version(),
        "primary_sha256": {q.name: hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(original.iterdir())},
        "witness": {
            "unit_customers": 11, "players": m, "labels": p,
            "distinct_nonempty_coverages": p, "positive_customer_types": len(customers),
            "complete_history_nodes": len(policy), "all_actions_zero": True,
            "ordered_terminal_histories": leaves, "actual_path": actual_path,
            "terminal_counts": actual, "payoffs": [str(utility(actual, a)) for a in actual_path],
            "nonself_deviations": comparisons, "self_comparisons": self_comparisons,
            "strict": sum(strict.values()), "ties": sum(ties.values()), "violations": 0,
            "levels": [{"length": t, "nodes": level_histories[t], "strict": strict[t], "ties": ties[t]} for t in range(m)],
            "slack_histogram": {str(x): n for x, n in sorted(slack_histogram.items())},
            "analytical_constant_big_comparisons": analytical_rows,
            "all_interest_type_columns": len(masks), "integer_IC_scale": scale,
            "nonself_rows_before_deduplication": generated_rows,
            "unique_nonzero_integer_IC_rows": len(G),
            "integer_matrix_entries": len(G) * len(masks),
            "minimum_unique_integer_cone_slack": min(cone_slacks),
            "portfolio_subsets_checked": len(all_portfolios),
            "welfare": W, "optimal_welfare": optimum, "ratio": str(ratio),
            "half_slack": 2 * W - optimum,
        },
        "historical_report": {
            "top_level_fields_read": sorted(report), "round_records": len(record_audit),
            "rounds": record_audit,
            "unavailable_intermediate_data": ["eight complete policies", "eight rational mass vectors",
                                              "LP primal/dual states", "all 168 portfolio outcomes", "original argv/environment"],
            "pairwise_distinct_policies_or_cones_not_claimed": True,
        },
        "new_LP_calls": 0, "original_discovery_replays": 0, "outcome_set_solver_calls": 0,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"nodes": len(policy), "deviations": comparisons, "strict": sum(strict.values()),
                      "ties": sum(ties.values()), "unique_IC_rows": len(G), "ratio": str(ratio),
                      "round_records": len(record_audit), "violations": 0}))


if __name__ == "__main__":
    main()
