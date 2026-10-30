"""Read every frozen JSON field and replay all ordered histories without a solver.

The finite all-matching and cross-node checks below supplement the frozen
auditor. They do not infer an all-m theorem from four computed members.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def keys(obj, expected):
    assert set(obj) == set(expected.split()), (set(obj), expected)


def structure(obj):
    counts = Counter()
    def visit(x):
        counts[type(x).__name__] += 1
        if isinstance(x, dict):
            for v in x.values(): visit(v)
        elif isinstance(x, list):
            for v in x: visit(v)
    visit(obj)
    return dict(counts)


def engine(instance, certificate):
    keys(instance, "topics customers players")
    keys(certificate, "terminal_counts actions")
    p, m = len(instance["topics"]), instance["players"]
    assert len(set(instance["topics"])) == p and p > 0
    assert type(m) is int and m >= 1
    customers = []
    for item in instance["customers"]:
        keys(item, "topics multiplicity")
        interest = tuple(item["topics"])
        assert list(interest) == sorted(set(interest))
        assert all(type(a) is int and 0 <= a < p for a in interest)
        assert type(item["multiplicity"]) is int and item["multiplicity"] > 0
        customers.append((frozenset(interest), item["multiplicity"]))
    actions = {}
    for item in certificate["actions"]:
        keys(item, "history action")
        h, a = tuple(item["history"]), item["action"]
        assert h not in actions
        assert all(type(b) is int and 0 <= b < p for b in h)
        assert type(a) is int and 0 <= a < p
        actions[h] = a
    expected = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert set(actions) == expected
    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))
    @lru_cache(None)
    def count(z): return tuple(z.count(a) for a in range(p))
    @lru_cache(None)
    def utility_counts(a, q):
        return sum((F(n, sum(q[b] for b in t)) for t, n in customers if a in t), F(0))
    def utility(a, z): return utility_counts(a, count(z))
    def coverage(z): return sum(n for t, n in customers if any(a in t for a in z))
    actual = terminal(())
    assert list(count(actual)) == certificate["terminal_counts"]
    ties, strict, comparisons = 0, 0, 0
    for h, a in actions.items():
        u = utility(a, terminal(h))
        for b in range(p):
            difference = u - utility(b, terminal(h + (b,)))
            assert difference >= 0, (h, a, b, difference)
            comparisons += 1
            ties += difference == 0
            strict += difference > 0
    return locals()


def check_cyclic():
    data = json.loads((HERE / "original/audit_cyclic_budget.json").read_text())
    keys(data, "status source_unit_customers source_complete_histories source_comparisons_including_self actual payoffs W OPT unique_optimal_supports matchings matrix weights kernels weighted_real_queries weighted_actual_budget source_type_checks cyclic_matrix_kernels")
    env = engine(json.loads((HERE / "dependencies/examples/customer_attraction/portfolio_matching_failure.json").read_text()),
                 json.loads((HERE / "dependencies/evidence/certificates/customer_attraction/portfolio_matching_failure.json").read_text()))
    customers, z = env["customers"], env["actual"]
    terminal, utility, coverage = env["terminal"], env["utility"], env["coverage"]
    assert data["status"] == "exact_definition_level_checks_passed"
    assert data["source_unit_customers"] == sum(n for t, n in customers) == 86
    assert data["source_complete_histories"] == len(env["actions"]) == 6
    assert data["source_comparisons_including_self"] == env["comparisons"] == 30
    assert data["actual"] == list(z) == [4, 0]
    u = [utility(a, z) for a in z]
    assert data["payoffs"] == list(map(str, u)) == ["22", "22"]
    assert data["W"] == coverage(z) == 44
    supports = list(combinations(range(5), 2)) + [(i, i) for i in range(5)]
    optimum = max(map(coverage, supports))
    assert data["OPT"] == optimum == 45
    assert data["unique_optimal_supports"] == [list(s) for s in supports if coverage(s) == optimum] == [[1, 3]]
    def r(pi, t):
        eligible = [j for j, a in enumerate(pi) if a in t]
        if not eligible: return F(0)
        c = sum(a in t for a in z)
        return min(F(1, c + 1 - int(z[j] in t)) for j in eligible)
    for item, pi in zip(data["matchings"], ((1, 3), (3, 1)), strict=True):
        keys(item, "assignment branches real_query_payoffs real_query_sum partitioned_frozen_R")
        branches = [terminal(z[:j] + (a,)) for j, a in enumerate(pi)]
        query = [utility(a, b) for a, b in zip(pi, branches)]
        assert item == {"assignment": list(pi), "branches": list(map(list, branches)),
                        "real_query_payoffs": list(map(str, query)), "real_query_sum": str(sum(query)),
                        "partitioned_frozen_R": str(sum(n * r(pi, t) for t, n in customers))}
    P = [[F(x) for x in row] for row in data["matrix"]]
    weights = list(map(F, data["weights"]))
    assert P == [[F(1), F(0)], [F(0), F(0)]] and weights == [2, 1]
    subsets = [(0,), (1,), (0, 1)]
    def kernel(P, w, J): return sum((w[j] / (1 + sum(P[j][l] for l in J)) for j in J), F(0))
    assert data["kernels"] == {str(J): str(kernel(P, weights, J)) for J in subsets}
    pi = (1, 3); branches = [terminal(z[:j] + (a,)) for j, a in enumerate(pi)]
    type_checks = []
    for t, n in customers:
        J = tuple(j for j, a in enumerate(pi) if a in t)
        if not J: continue
        c = sum(a in t for a in z)
        for j in J:
            assert sum(a in t for a in branches[j]) <= c - int(z[j] in t) + 1 + sum(P[j][l] for l in J)
        query = sum((weights[j] / sum(a in t for a in branches[j]) for j in J), F(0))
        assert query >= r(pi, t) * kernel(P, weights, J) >= r(pi, t)
        type_checks.append({"topics": sorted(t), "multiplicity": n, "J": list(J),
                            "R_coefficient": str(r(pi, t)), "weighted_real_query_coefficient": str(query)})
    assert data["source_type_checks"] == type_checks
    assert F(data["weighted_real_queries"]) == sum(weights[j] * utility(pi[j], branches[j]) for j in range(2)) == 60
    assert F(data["weighted_actual_budget"]) == sum(weights[j] * u[j] for j in range(2)) == 66
    cyclic = [[F(0), F(3)], [F(1, 10), F(0)]]
    assert data["cyclic_matrix_kernels"] == {str(J): str(kernel(cyclic, [1, 1], J)) for J in subsets}
    return {"structure_counts": structure(data), "histories": 6, "comparisons_including_self": 30,
            "strict_comparisons": env["strict"], "ties_including_self": env["ties"],
            "all_fields_reconstructed": True}


def check_padding(record):
    keys(record, "players topics W OPT actual histories comparisons_including_self all_actual_payoffs unique_optimal_support kernel_budget_lower_bound attained_kernel_budget on_path_old_query_load_witnesses upper_witness_assignment upper_witness_weights instance certificate")
    e = engine(record["instance"], record["certificate"])
    p, m = e["p"], e["m"]
    customers, z, terminal = e["customers"], e["actual"], e["terminal"]
    utility, coverage = e["utility"], e["coverage"]
    aux = tuple(range(5, m + 3)); target = aux + (1, 3)
    base = json.loads((HERE / "dependencies/examples/customer_attraction/portfolio_matching_failure.json").read_text())
    assert record["instance"] == {"topics": base["topics"] + [f"Z{i+1}" for i in range(m - 2)],
        "customers": base["customers"] + [{"topics": [a], "multiplicity": 22} for a in aux], "players": m}
    assert record["players"] == m and record["topics"] == p == m + 3
    assert record["actual"] == list(z) == list(aux + (4, 0))
    assert record["histories"] == len(e["actions"]) == sum(p ** d for d in range(m))
    assert record["comparisons_including_self"] == e["comparisons"] == p * len(e["actions"])
    assert record["all_actual_payoffs"] == "22" and all(utility(a, z) == 22 for a in z)
    assert record["W"] == coverage(z) == 22 * m
    supports = [s for size in range(m + 1) for s in combinations(range(p), size)]
    optimum = max(map(coverage, supports))
    optimal = [list(s) for s in supports if coverage(s) == optimum]
    assert record["OPT"] == optimum == 22 * m + 1
    assert [record["unique_optimal_support"]] == optimal == [sorted(target)]
    witnesses = []
    for i in range(m):
        for S, interest in ((1, {1, 2}), (3, {2, 3})):
            b = terminal(z[:i] + (S,)); load = sum(a in interest for a in b)
            assert load == (1 if i == m - 1 else 2)
            witnesses.append({"actual_node": list(z[:i]), "query": S, "witness_interest": sorted(interest),
                              "terminal": list(b), "load": load})
    assert record["on_path_old_query_load_witnesses"] == witnesses
    assert record["upper_witness_assignment"] == list(target)
    assert record["upper_witness_weights"] == [1] * (m - 2) + [2, 1]
    def row_need(S, a, b):
        return max([0] + [sum(t in interest for t in b) - sum(t in interest for t in z)
                           + int(a in interest) - 1 for interest, n in customers if S in interest])
    budgets = Counter()
    for assignment in permutations(target):
        weights = [1 + row_need(S, z[j], terminal(z[:j] + (S,))) for j, S in enumerate(assignment)]
        budgets[22 * sum(weights)] += 1
    assert min(budgets) == record["kernel_budget_lower_bound"] == record["attained_kernel_budget"] == 22 * (m + 1)
    attained = [1 + row_need(S, z[j], terminal(z[:j] + (S,))) for j, S in enumerate(target)]
    assert attained == record["upper_witness_weights"]
    # Explicit cross-topic matching from the analytic source, all queries at last A node.
    assigned = (0, 4) if m == 2 else (0, aux[0]) + tuple(aux[1:]) + (4,)
    comparison = (1, 3) + aux
    assert sorted(assigned) == sorted(z) and len(comparison) == m
    query_sum = F(0); frozen = F(0)
    for S, a in zip(comparison, assigned):
        b = terminal(z[:-1] + (S,))
        query_sum += utility(S, b)
        for interest, n in customers:
            if S not in interest: continue
            c = sum(t in interest for t in z)
            assert sum(t in interest for t in b) == c - int(a in interest) + 1
            frozen += F(n, c - int(a in interest) + 1)
    assert query_sum == frozen == 44 + 11 * (m - 2) <= 22 * m
    assert m * utility(0, z) == 22 * m
    return {"players": m, "topics": p, "unit_customers": sum(n for t, n in customers),
            "structure_counts": structure(record), "decision_histories_by_depth": {str(d): p ** d for d in range(m)},
            "histories": len(e["actions"]), "comparisons_including_self": e["comparisons"],
            "strict_comparisons": e["strict"], "ties_including_self": e["ties"],
            "all_fields_reconstructed": True, "all_matchings_budget_histogram": dict(sorted(budgets.items())),
            "minimum_restricted_kernel_budget": min(budgets), "cross_node_query_sum": str(query_sum),
            "cross_node_payoff_budget": 22 * m, "W": 22 * m, "OPT": optimum}


def main():
    if not __debug__: raise RuntimeError("Assertions must be enabled")
    path = HERE / "original/padding_kernel_boundary.json"
    data = json.loads(path.read_text())
    keys(data, "status general_claim members")
    assert data["status"] == "finite_complete_strategy_members_verified_exactly"
    assert data["general_claim"] == "analytic all-m construction is proved separately in padding_kernel_boundary.md"
    assert [r["players"] for r in data["members"]] == [2, 3, 4, 5]
    report = {"status": "PASS", "python": sys.version, "assertions_enabled": __debug__,
              "padding_file_bytes": len(path.read_bytes()), "padding_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "padding_structure_counts": structure(data), "cyclic": check_cyclic(),
              "members": [check_padding(r) for r in data["members"]],
              "scope": "All fields and every ordered node of four stored members; no solver, no all-m extrapolation"}
    replay = HERE / "replay"; replay.mkdir(exist_ok=True)
    (replay / "independent-full-data.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__": main()
