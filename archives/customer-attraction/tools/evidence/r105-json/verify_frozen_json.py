#!/usr/bin/env python3
"""Definition-level, all-field verification of the frozen R105 assignment JSON.

This checker does not import or run the original audit. It reads the existing
raw instance/policy, builds both literal unit clients and a compressed scaled
integer evaluator, and reconstructs every mathematical field of the JSON.
Historical paths and epistemic declarations are checked as provenance strings,
not certified as mathematical consequences. Only the optional report is written.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import platform


HERE = Path(__file__).resolve().parent
SOURCE_SHA = "a860f144805263ece3aa034a2e66f1e54adc740d38777cdad6713bd1df997d29"
INSTANCE_SHA = "2ae935f6980037f3526eee447021a6e2d8d5987e0bb2b2c31d4017afad7126c4"
POLICY_SHA = "1c59b0406e8fdd56e01fc4a2d1c03b9dd15a9aefc0748a556fb08cf593fa27ac"
OLD_ROOT = "/workspace/scratch/84b70c36e8dc/co-work-anl/research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        check(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_exact(path, expected_hash):
    raw = path.read_bytes()
    check(sha(raw) == expected_hash, "unexpected bytes: " + str(path))
    return json.loads(raw, object_pairs_hook=unique_object), raw


def rational(value):
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator,
            "text": str(value)}


def compare_all(actual, expected, counts, path="$"):
    """Visit every node, rejecting missing/extra keys, order, types and values."""
    check(type(actual) is type(expected), path + ": type mismatch")
    if isinstance(expected, dict):
        counts["objects"] += 1
        check(set(actual) == set(expected), path + ": key mismatch")
        for key, value in expected.items():
            compare_all(actual[key], value, counts, path + "." + key)
    elif isinstance(expected, list):
        counts["arrays"] += 1
        check(len(actual) == len(expected), path + ": length mismatch")
        for index, (av, ev) in enumerate(zip(actual, expected)):
            compare_all(av, ev, counts, path + "[" + str(index) + "]")
    else:
        counts["scalar_leaves"] += 1
        counts["scalar_" + type(expected).__name__] += 1
        check(actual == expected, path + ": value mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=HERE / "original/independent_assignment_audit.json")
    parser.add_argument("--instance", type=Path,
                        default=HERE.parent / "dynamic-exchange/original/assignment_instance.json")
    parser.add_argument("--policy", type=Path,
                        default=HERE.parent / "dynamic-exchange/original/assignment_full_policy.json")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    source, source_bytes = load_exact(args.source, SOURCE_SHA)
    instance, instance_bytes = load_exact(args.instance, INSTANCE_SHA)
    submitted, policy_bytes = load_exact(args.policy, POLICY_SHA)
    check(set(instance) == {"topics", "players", "customers"}, "instance schema")
    check(instance["players"] == 3 and type(instance["players"]) is int, "three players")
    check(instance["topics"] == list(map(str, range(6))), "six catalog labels")
    check(set(submitted) == {"policy", "actual"}, "policy schema")
    n, p, scale = 3, 6, 6

    # A customer identifier is one distinct position of this literal list.
    unit_clients = []
    type_rows = []
    seen_types = set()
    for row in instance["customers"]:
        check(set(row) == {"topics", "multiplicity"}, "customer row schema")
        topics, mult = row["topics"], row["multiplicity"]
        check(all(type(a) is int and 0 <= a < p for a in topics), "legal interest")
        check(topics == sorted(set(topics)) and topics, "nonempty distinct interests")
        check(type(mult) is int and mult > 0, "positive unit multiplicity")
        mask = sum(1 << a for a in topics)
        check(mask not in seen_types, "duplicate interest type")
        seen_types.add(mask)
        type_rows.append((mask, mult))
        unit_clients.extend([frozenset(topics)] * mult)
    check(seen_types == set(range(1, 1 << p)), "all 63 nonempty types")
    topic_sets = [{i for i, interest in enumerate(unit_clients) if a in interest}
                  for a in range(p)]
    check(len({frozenset(s) for s in topic_sets}) == p, "distinct topic coverages")

    histories = [h for depth in range(n) for h in product(range(p), repeat=depth)]
    policy = {}
    for key, action in submitted["policy"].items():
        history = tuple(map(int, key.split(","))) if key else ()
        check(",".join(map(str, history)) == key, "canonical history key")
        check(history not in policy and type(action) is int and 0 <= action < p,
              "legal unique policy row")
        policy[history] = action
    check(set(policy) == set(histories), "complete ordered-history policy")

    terminals = list(product(range(p), repeat=n))
    values = {}
    for z in terminals:
        # Literal path: direct Fraction shares for distinct individual clients.
        unit_pay = [Fraction(0) for _ in range(n)]
        unit_coverage = 0
        for interest in unit_clients:
            owners = [i for i in range(n) if z[i] in interest]
            if owners:
                unit_coverage += 1
                for i in owners:
                    unit_pay[i] += Fraction(1, len(owners))
        # Compressed path: bit tests and integers scaled by six, no unit shares.
        compressed_pay = [0] * n
        compressed_coverage = 0
        for mask, mult in type_rows:
            selected = tuple(bool(mask & (1 << a)) for a in z)
            load = sum(selected)
            if load:
                compressed_coverage += mult
                for i in range(n):
                    if selected[i]:
                        compressed_pay[i] += mult * (scale // load)
        check(unit_coverage == compressed_coverage, "coverage disagreement " + str(z))
        check(tuple(unit_pay) == tuple(Fraction(v, scale) for v in compressed_pay),
              "payoff disagreement " + str(z))
        check(sum(unit_pay) == unit_coverage, "payoffs do not conserve coverage")
        values[z] = (tuple(unit_pay), unit_coverage)

    # Backward table of actual continuation leaves, including all off-path nodes.
    leaves = {z: z for z in terminals}
    for depth in range(n - 1, -1, -1):
        for h in product(range(p), repeat=depth):
            leaves[h] = leaves[h + (policy[h],)]
    actual = leaves[()]
    check(list(actual) == submitted["actual"], "actual metadata disagreement")
    comparisons = []
    nonself_slacks = []
    depth_stats = {}
    for h in histories:
        i = len(h)
        base_leaf = leaves[h]
        base = values[base_leaf][0][i]
        for action in range(p):
            forced_leaf = leaves[h + (action,)]
            alternative = values[forced_leaf][0][i]
            slack = base - alternative
            is_self = action == policy[h]
            comparisons.append({
                "history": list(h), "player_zero_based": i,
                "prescribed_action": policy[h], "forced_action": action,
                "prescribed_terminal": list(base_leaf),
                "forced_terminal": list(forced_leaf),
                "actual_player_payoff": rational(base),
                "forced_player_payoff": rational(alternative),
                "slack": rational(slack), "self_action": is_self,
            })
            if not is_self:
                nonself_slacks.append(slack)
                depth_stats.setdefault(i, Counter())["strict" if slack > 0 else
                                                        "tie" if slack == 0 else "negative"] += 1
    violations = [row for row in comparisons if row["slack"]["numerator"] < 0]
    actual_pay, welfare = values[actual]
    optimum = max(w for _, w in values.values())
    optimal_tuples = [t for t in terminals if values[t][1] == optimum]
    supports = sorted({tuple(sorted(set(t))) for t in optimal_tuples})
    static_matrix = []
    for topic in range(p):
        query_row = []
        for i in range(n):
            altered = tuple(topic if j == i else actual[j] for j in range(n))
            query_row.append(values[altered][0][i])
        static_matrix.append(query_row)
    assignment_checks, assignments = [], {}
    for t in optimal_tuples:
        for pi in permutations(range(n)):
            assignment = tuple(t[pi[i]] for i in range(n))
            pieces = [static_matrix[assignment[i]][i] for i in range(n)]
            total = sum(pieces, Fraction(0))
            assignments[assignment] = total
            assignment_checks.append({
                "optimal_ordered_tuple": list(t), "slot_permutation": list(pi),
                "assigned_topics_by_actual_player": list(assignment),
                "static_player_payoffs": [rational(v) for v in pieces],
                "sum": rational(total),
                "sum_minus_actual_welfare": rational(total - welfare),
            })
    minimum, maximum = min(assignments.values()), max(assignments.values())
    expected = {
        "audit": "independent unit-client expansion plus compressed Fraction cross-check",
        "author_derivation_or_code_read": False, "imports_project_code": False,
        "raw_inputs": {
            "instance_path": OLD_ROOT + "assignment_instance.json",
            "instance_sha256": INSTANCE_SHA,
            "policy_path": OLD_ROOT + "assignment_full_policy.json",
            "policy_sha256": POLICY_SHA,
        },
        "dimensions": {
            "players": n, "topics": p, "positive_types": len(type_rows),
            "distinct_unit_customers": len(unit_clients),
            "topic_sizes": [len(s) for s in topic_sets],
            "empty_catalog_topics": [a for a, s in enumerate(topic_sets) if not s],
            "payoff_integer_scale": scale,
        },
        "terminal_enumeration": {
            "ordered_legal_tuples_including_repetitions": len(terminals),
            "all_unit_and_compressed_evaluations_agree": True,
            "all_payoff_sums_equal_welfare": True, "optimum_welfare": optimum,
            "optimal_ordered_tuples": [list(t) for t in optimal_tuples],
            "distinct_optimal_supports": [list(s) for s in supports],
            "coverage_by_ordered_tuple": [
                {"terminal": list(t), "welfare": values[t][1]} for t in terminals],
        },
        "full_history_spe": {
            "ordered_decision_histories": len(histories),
            "all_actions_including_self_comparisons": len(comparisons),
            "nonself_comparisons": len(nonself_slacks),
            "strict_nonself_comparisons": sum(v > 0 for v in nonself_slacks),
            "tied_nonself_comparisons": sum(v == 0 for v in nonself_slacks),
            "minimum_nonself_slack": rational(min(nonself_slacks)),
            "violation_count": len(violations), "is_full_pure_spe": not violations,
            "all_comparisons": comparisons,
        },
        "actual": {
            "terminal": list(actual), "payoffs": [rational(v) for v in actual_pay],
            "welfare": welfare, "twice_welfare_minus_optimum": 2 * welfare - optimum,
        },
        "static_assignment": {
            "definition": "sum_i u_i(T_pi(i), z_-i), with all other actual topics frozen",
            "topic_by_player_payoff_matrix": [
                [rational(v) for v in row] for row in static_matrix],
            "optimal_tuple_permutation_checks": len(assignment_checks),
            "distinct_topic_assignments": len(assignments),
            "minimum_sum": rational(minimum), "maximum_sum": rational(maximum),
            "minimum_minus_actual_welfare": rational(minimum - welfare),
            "minimizing_assignments": [list(t) for t, v in sorted(assignments.items())
                                       if v == minimum],
            "every_optimal_assignment_exceeds_actual_welfare": all(
                v > welfare for v in assignments.values()),
            "all_checks": assignment_checks,
        },
        "conclusion": {
            "seq242_existential_optimal_assignment_bridge_is_refuted_by_this_input":
                not violations and minimum > welfare,
            "q_cag_half_is_refuted_by_this_input": 2 * welfare < optimum,
            "general_q_cag_half_status": "OPEN", "novelty_claim": False,
        },
    }
    counts = Counter()
    compare_all(source, expected, counts)
    for path, raw in ((args.source, source_bytes), (args.instance, instance_bytes),
                      (args.policy, policy_bytes)):
        check(path.read_bytes() == raw, "input changed during audit: " + str(path))
    report = {
        "status": "all-frozen-fields-match-definition-level-reconstruction",
        "python": platform.python_version(), "assertions_enabled": __debug__,
        "original_audit_imported_or_executed": False,
        "source_sha256": SOURCE_SHA, "source_bytes": len(source_bytes),
        "instance_sha256": INSTANCE_SHA, "policy_sha256": POLICY_SHA,
        "complete_json_traversal": dict(sorted(counts.items())),
        "historical_metadata_not_derived_from_math": [
            "audit", "author_derivation_or_code_read", "imports_project_code",
            "raw_inputs.instance_path", "raw_inputs.policy_path",
            "conclusion.general_q_cag_half_status", "conclusion.novelty_claim"],
        "all_terminals_cross_checked": len(terminals),
        "covered_payoff_coordinates": n * len(terminals),
        "all_true_spe_rows_verified": len(comparisons),
        "nonself_by_zero_based_player": {str(i): dict(sorted(v.items()))
                                             for i, v in sorted(depth_stats.items())},
        "nonself_slack_histogram": dict(sorted(Counter(map(str, nonself_slacks)).items())),
        "coverage_histogram": {str(k): v for k, v in sorted(Counter(
            w for _, w in values.values()).items())},
        "distinct_topic_count_coverage_range": {
            str(k): {"ordered_tuples": sum(len(set(t)) == k for t in terminals),
                     "minimum": min(values[t][1] for t in terminals if len(set(t)) == k),
                     "maximum": max(values[t][1] for t in terminals if len(set(t)) == k)}
            for k in range(1, n + 1)},
        "actual": {"terminal": list(actual), "payoffs": list(map(str, actual_pay)),
                   "W": welfare, "OPT": optimum, "half_slack": 2 * welfare - optimum},
        "static_matrix_multiplied_by_three": [
            [int(3 * v) for v in row] for row in static_matrix],
        "all_36_assignment_rows_verified": len(assignment_checks),
        "distinct_assignments": [
            {"assignment": list(t), "sum": str(v), "gap": str(v - welfare)}
            for t, v in sorted(assignments.items())],
        "input_bytes_unchanged": True,
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "limitations": "One given game and policy. Provenance declarations are not "
            "independently certified historical facts. No global search, novelty, "
            "current all-n status or six-player theorem is inferred.",
    }
    # Count rather than assume how many rational value records were inspected.
    def rational_count(node):
        if isinstance(node, dict):
            return int(set(node) == {"numerator", "denominator", "text"}) + sum(
                rational_count(v) for v in node.values())
        if isinstance(node, list):
            return sum(map(rational_count, node))
        return 0
    report["rational_objects"] = rational_count(source)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        check(args.report.resolve() not in {args.source.resolve(), args.instance.resolve(),
                                           args.policy.resolve()}, "report cannot overwrite input")
        args.report.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
