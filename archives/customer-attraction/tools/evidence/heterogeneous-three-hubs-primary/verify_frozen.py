"""Read every primary JSON field and verify the saved SPE with Fraction only.

No imports from the original generator, cone Engine, canonical package, NumPy,
SciPy, or any SPE outcome-set solver. The run's floats remain historical
proposals: their missing customer masses and policies cannot be reconstructed
from its five-field records.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import platform
import sys


def integer(x, minimum=0):
    assert isinstance(x, int) and not isinstance(x, bool) and x >= minimum
    return x


def read_json(path):
    def invalid(token):
        raise ValueError(f"nonfinite JSON number {token}")
    return json.loads(path.read_text(), parse_constant=invalid)


def main():
    original = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "original"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "verification.json"
    best = read_json(original / "heterogeneous_three_hubs_best.json")
    run = read_json(original / "heterogeneous_three_hubs_run.json")
    assert set(best) == {"scope", "ratio", "instance", "strategy", "checked_histories", "checked_deviations"}
    assert best["scope"] == "One actual finite CAG with all ordered-history actions certified; not a universal bound."
    assert set(best["instance"]) == {"topics", "customers", "players"}
    topics = best["instance"]["topics"]
    assert topics == ["B", "C", "D", "T1", "T2", "T3", "T4", "T5"]
    m = integer(best["instance"]["players"], 1)
    p = len(topics)
    assert (m, p) == (5, 8)
    customers = []
    for item in best["instance"]["customers"]:
        assert set(item) == {"topics", "multiplicity"}
        liked = tuple(item["topics"])
        assert liked == tuple(sorted(set(liked))) and liked
        assert all(integer(a) < p for a in liked)
        customers.append((liked, integer(item["multiplicity"], 1)))
    assert customers == [((3,), 1), ((4,), 1), ((5,), 1), ((0, 1, 2, 6), 5), ((7,), 1)]
    assert set(best["strategy"]) == {"terminal_counts", "actions"}
    declared = tuple(best["strategy"]["terminal_counts"])
    assert len(declared) == p and sum(map(integer, declared)) == m
    policy = {}
    supplied_order = []
    for item in best["strategy"]["actions"]:
        assert set(item) == {"history", "action"}
        history = tuple(item["history"])
        assert len(history) < m and all(integer(a) < p for a in history)
        action = integer(item["action"])
        assert action < p and history not in policy
        policy[history] = action
        supplied_order.append(history)
    expected_order = [h for t in range(m) for h in product(range(p), repeat=t)]
    assert supplied_order == expected_order
    assert set(policy) == set(expected_order)

    @lru_cache(None)
    def utility(counts, action):
        return sum((F(n, sum(counts[a] for a in liked))
                    for liked, n in customers if action in liked), F(0))

    def welfare(counts):
        return sum(n for liked, n in customers if any(counts[a] for a in liked))

    level_counts = Counter()
    level_strict = Counter()
    level_ties = Counter()
    slack_histogram = Counter()
    self_checks = 0
    comparisons = 0
    leaf_histories = 0

    def tree(history):
        nonlocal self_checks, comparisons, leaf_histories
        if len(history) == m:
            leaf_histories += 1
            return tuple(history.count(a) for a in range(p)), history
        branches = [tree(history + (a,)) for a in range(p)]
        action = policy[history]
        chosen_counts, chosen_path = branches[action]
        current = utility(chosen_counts, action)
        level_counts[len(history)] += 1
        for a, (alternative_counts, _) in enumerate(branches):
            slack = current - utility(alternative_counts, a)
            assert slack >= 0, (history, action, a, slack)
            if a == action:
                self_checks += 1
                assert slack == 0
            else:
                comparisons += 1
                slack_histogram[slack] += 1
                if slack:
                    level_strict[len(history)] += 1
                else:
                    level_ties[len(history)] += 1
        return chosen_counts, chosen_path

    actual, actual_path = tree(())
    assert actual == declared
    assert integer(best["checked_histories"]) == len(policy)
    assert integer(best["checked_deviations"]) == comparisons
    assert len(policy) == 4681 and comparisons == 32767 and leaf_histories == 32768
    assert all(action == 0 for action in policy.values())
    # Independently check the analytical constant-B continuation at every node:
    # big load b+r <= m, whereas every singleton deviation gives 1/(k+1).
    analytical_rows = 0
    for history in expected_order:
        b = sum(a in {0, 1, 2, 6} for a in history)
        r = m - len(history)
        prescribed = F(5, b + r)
        assert prescribed >= 1
        for a in range(p):
            alternative = prescribed if a in {0, 1, 2, 6} else F(1, history.count(a) + 1)
            assert prescribed >= alternative
            analytical_rows += 1

    portfolio_values = []
    for size in range(min(m, p) + 1):
        for selected in combinations(range(p), size):
            counts = tuple(int(a in selected) for a in range(p))
            portfolio_values.append((welfare(counts), selected))
    optimum = max(v for v, _ in portfolio_values)
    actual_welfare = welfare(actual)
    exact_ratio = F(optimum, actual_welfare)
    assert F(best["ratio"]) == exact_ratio == F(9, 5)
    assert actual_welfare == 5 and optimum == 9
    assert sum(n for _, n in customers) == 9

    # Every field in each historical run record is read and checked for its
    # actual representational contract; no float LP optimality is asserted.
    assert set(run) == {"scope", "best_exact_ratio", "cones", "records", "elapsed"}
    assert run["scope"] == "Directed finite fixed-policy cone search in disjoint-petal/three-lure catalogs; zero counterexamples is not a theorem."
    assert F(run["best_exact_ratio"]) == exact_ratio
    assert integer(run["cones"]) == 59
    assert isinstance(run["elapsed"], (float, int)) and math.isfinite(run["elapsed"]) and run["elapsed"] >= 0
    record_audit = []
    previous = -1
    for rec in run["records"]:
        assert set(rec) == {"step", "input_ratio_proposal", "optimized_ratio_proposal", "root", "rows"}
        step = integer(rec["step"])
        assert previous < step < 60
        previous = step
        for key in ("input_ratio_proposal", "optimized_ratio_proposal"):
            assert isinstance(rec[key], (float, int)) and not isinstance(rec[key], bool)
            assert math.isfinite(rec[key]) and rec[key] > 0
        root = rec["root"]
        assert len(root) == p and sum(map(integer, root)) == m
        rows = integer(rec["rows"], 1)
        assert rows <= comparisons
        record_audit.append({"step": step, "root_sum": sum(root), "distinct_nonzero_IC_rows_reported": rows,
                             "input_ratio_proposal_read": rec["input_ratio_proposal"],
                             "optimized_ratio_proposal_read": rec["optimized_ratio_proposal"],
                             "structural_contract": "pass; proposal not rationally certified"})
    assert len(record_audit) == run["cones"] == 59
    missing_steps = sorted(set(range(60)) - {r["step"] for r in record_audit})
    assert missing_steps == [57]
    coverage_columns = [tuple(i for i, (liked, _) in enumerate(customers) if a in liked) for a in range(p)]
    groups = defaultdict(list)
    for a, column in enumerate(coverage_columns):
        groups[column].append(a)
    metadata = {
        "scope": "Definition-level exact audit of this saved witness; all historical run fields read; zero discovery/LP/SPE-solver calls.",
        "python": platform.python_version(),
        "primary_sha256": {q.name: hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(original.iterdir())},
        "full_json_fields_checked": {"best_top_level": sorted(best), "run_top_level": sorted(run)},
        "witness": {
            "players": m, "labels": p, "distinct_coverages": len(groups),
            "coverage_equivalence_classes": list(groups.values()), "unit_customers": 9,
            "customer_records": len(customers), "action_records": len(policy),
            "all_actions_zero": True, "ordered_leaf_histories": leaf_histories,
            "checked_nonself_deviations": comparisons, "checked_self_comparisons": self_checks,
            "analytical_constant_B_comparisons": analytical_rows,
            "strict_nonself_deviations": sum(level_strict.values()),
            "tie_nonself_deviations": sum(level_ties.values()),
            "levels": [{"length": t, "histories": level_counts[t], "strict": level_strict[t], "ties": level_ties[t]} for t in range(m)],
            "slack_histogram": {str(q): n for q, n in sorted(slack_histogram.items())},
            "violations": 0, "actual_path": actual_path, "actual_counts": actual,
            "player_payoffs": [str(utility(actual, a)) for a in actual_path],
            "welfare": actual_welfare, "optimal_welfare": optimum,
            "portfolio_subsets_checked": len(portfolio_values), "ratio": str(exact_ratio),
            "half_slack": 2 * actual_welfare - optimum,
        },
        "run": {"historical_elapsed_seconds": run["elapsed"], "cone_coverage_keys_reported": run["cones"],
                "records_read": len(record_audit), "missing_steps": missing_steps,
                "distinct_nonzero_IC_rows_range": [min(r["rows"] for r in run["records"]), max(r["rows"] for r in run["records"])],
                "optimized_proposal_range": [min(r["optimized_ratio_proposal"] for r in run["records"]), max(r["optimized_ratio_proposal"] for r in run["records"])],
                "record_audit": record_audit,
                "not_recoverable_from_run": ["customer masses", "complete policies", "LP multipliers or dual bounds", "full process argv/environment"]},
        "new_optimization_calls": 0, "original_discovery_replays": 0,
    }
    output.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"histories": len(policy), "deviations": comparisons,
                      "strict": sum(level_strict.values()), "ties": sum(level_ties.values()),
                      "ratio": str(exact_ratio), "run_records": len(record_audit), "violations": 0}))


if __name__ == "__main__":
    main()
