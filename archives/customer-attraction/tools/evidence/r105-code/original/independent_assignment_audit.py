#!/usr/bin/env python3
"""Independent raw-input audit of the seq242 existential-assignment bridge.

No project model, equilibrium solver, author audit, or numerical library is
imported.  One path expands every multiplicity into separate unit customers
and uses integer payoffs scaled by lcm(1,...,m).  A second path evaluates the
compressed types with Fraction and is checked against the unit path on every
legal terminal tuple.  The submitted raw policy is replayed at every ordered
history and every one-action deviation.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from math import lcm
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rational(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def main() -> None:
    own = Path(__file__).resolve().parent
    defaults = own.parent / "dynamic_exchange"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", type=Path,
                        default=defaults / "assignment_instance.json")
    parser.add_argument("--policy", type=Path,
                        default=defaults / "assignment_full_policy.json")
    parser.add_argument("--output", type=Path,
                        default=own / "independent_assignment_audit.json")
    args = parser.parse_args()

    instance_bytes = args.instance.read_bytes()
    policy_bytes = args.policy.read_bytes()
    instance = json.loads(instance_bytes)
    submitted_policy = json.loads(policy_bytes)
    m = instance["players"]
    labels = instance["topics"]
    p = len(labels)
    assert isinstance(m, int) and m >= 1
    assert p >= 1 and len(set(labels)) == p
    assert isinstance(instance["customers"], list)

    # Literal unit-client construction, independent of a bitmask evaluator.
    unit_interests: list[frozenset[int]] = []
    compressed: list[tuple[frozenset[int], int]] = []
    for row in instance["customers"]:
        interests = frozenset(row["topics"])
        count = row["multiplicity"]
        assert len(interests) == len(row["topics"])
        assert all(isinstance(a, int) and 0 <= a < p for a in interests)
        assert isinstance(count, int) and count >= 0
        compressed.append((interests, count))
        for _ in range(count):
            unit_interests.append(interests)
    topic_clients = [
        frozenset(x for x, interests in enumerate(unit_interests) if a in interests)
        for a in range(p)
    ]

    policy: dict[tuple[int, ...], int] = {}
    for key, action in submitted_policy["policy"].items():
        history = tuple(int(v) for v in key.split(",")) if key else ()
        assert history not in policy
        assert len(history) < m
        assert all(0 <= a < p for a in history)
        assert isinstance(action, int) and 0 <= action < p
        policy[history] = action
    histories = [h for k in range(m) for h in product(range(p), repeat=k)]
    assert set(policy) == set(histories), "policy must cover exactly every legal history"

    scale = lcm(*range(1, m + 1))
    terminals = list(product(range(p), repeat=m))
    unit_values: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
    for terminal in terminals:
        # Count individual clients directly, retaining repeated topic actions.
        loads = [0] * len(unit_interests)
        for action in terminal:
            for x in topic_clients[action]:
                loads[x] += 1
        profits = tuple(
            sum(scale // loads[x] for x in topic_clients[action])
            for action in terminal
        )
        welfare = sum(c > 0 for c in loads)
        assert sum(profits) == scale * welfare
        unit_values[terminal] = (profits, welfare)

        # Independent compressed, rational definition; no scaled payoffs reused.
        type_profits = [Fraction(0) for _ in range(m)]
        type_welfare = 0
        for interests, count in compressed:
            liking_players = [j for j, action in enumerate(terminal)
                              if action in interests]
            if liking_players:
                type_welfare += count
                piece = Fraction(count, len(liking_players))
                for j in liking_players:
                    type_profits[j] += piece
        assert type_welfare == welfare
        assert tuple(type_profits) == tuple(Fraction(v, scale) for v in profits)

    def rollout(prefix: tuple[int, ...]) -> tuple[int, ...]:
        path = list(prefix)
        while len(path) < m:
            path.append(policy[tuple(path)])
        return tuple(path)

    comparisons = []
    violations = []
    strict = tied = 0
    min_nonself: Fraction | None = None
    for history in histories:
        player = len(history)
        prescribed_leaf = rollout(history)
        base = unit_values[prescribed_leaf][0][player]
        for action in range(p):
            deviating_leaf = rollout(history + (action,))
            alternative = unit_values[deviating_leaf][0][player]
            delta = Fraction(base - alternative, scale)
            is_self = action == policy[history]
            if not is_self:
                min_nonself = delta if min_nonself is None else min(min_nonself, delta)
                strict += int(delta > 0)
                tied += int(delta == 0)
            row = {
                "history": list(history),
                "player_zero_based": player,
                "prescribed_action": policy[history],
                "forced_action": action,
                "prescribed_terminal": list(prescribed_leaf),
                "forced_terminal": list(deviating_leaf),
                "actual_player_payoff": rational(Fraction(base, scale)),
                "forced_player_payoff": rational(Fraction(alternative, scale)),
                "slack": rational(delta),
                "self_action": is_self,
            }
            comparisons.append(row)
            if delta < 0:
                violations.append(row)

    actual = rollout(())
    assert actual == tuple(submitted_policy["actual"])
    actual_profits_scaled, actual_welfare = unit_values[actual]
    opt = max(unit_values[t][1] for t in terminals)
    opt_tuples = [t for t in terminals if unit_values[t][1] == opt]
    opt_supports = sorted({tuple(sorted(set(t))) for t in opt_tuples})

    # Static replacement payoff u_i(T,z_-i): only position i changes; the
    # remaining actions are exactly those of the original actual terminal.
    static_table = []
    for action in range(p):
        row = []
        for player in range(m):
            altered = list(actual)
            altered[player] = action
            row.append(Fraction(unit_values[tuple(altered)][0][player], scale))
        static_table.append(row)

    # Literal double quantifier: every optimal ordered tuple and every
    # permutation of its slots, including duplicate slot permutations.
    assignment_checks = []
    distinct_assignments: dict[tuple[int, ...], Fraction] = {}
    for optimum_tuple in opt_tuples:
        for slot_permutation in permutations(range(m)):
            assignment = tuple(optimum_tuple[slot_permutation[i]] for i in range(m))
            pieces = [static_table[assignment[i]][i] for i in range(m)]
            total = sum(pieces, Fraction(0))
            distinct_assignments[assignment] = total
            assignment_checks.append({
                "optimal_ordered_tuple": list(optimum_tuple),
                "slot_permutation": list(slot_permutation),
                "assigned_topics_by_actual_player": list(assignment),
                "static_player_payoffs": [rational(v) for v in pieces],
                "sum": rational(total),
                "sum_minus_actual_welfare": rational(total - actual_welfare),
            })
    minimum = min(distinct_assignments.values())
    maxima = max(distinct_assignments.values())
    minimum_assignments = [list(t) for t, total in sorted(distinct_assignments.items())
                           if total == minimum]

    # Ensure the witness did not change while the audit ran.
    assert args.instance.read_bytes() == instance_bytes
    assert args.policy.read_bytes() == policy_bytes
    result = {
        "audit": "independent unit-client expansion plus compressed Fraction cross-check",
        "author_derivation_or_code_read": False,
        "imports_project_code": False,
        "raw_inputs": {
            "instance_path": str(args.instance),
            "instance_sha256": digest(instance_bytes),
            "policy_path": str(args.policy),
            "policy_sha256": digest(policy_bytes),
        },
        "dimensions": {
            "players": m,
            "topics": p,
            "positive_types": sum(count > 0 for _, count in compressed),
            "distinct_unit_customers": len(unit_interests),
            "topic_sizes": [len(clients) for clients in topic_clients],
            "empty_catalog_topics": [a for a in range(p) if not topic_clients[a]],
            "payoff_integer_scale": scale,
        },
        "terminal_enumeration": {
            "ordered_legal_tuples_including_repetitions": len(terminals),
            "all_unit_and_compressed_evaluations_agree": True,
            "all_payoff_sums_equal_welfare": True,
            "optimum_welfare": opt,
            "optimal_ordered_tuples": [list(t) for t in opt_tuples],
            "distinct_optimal_supports": [list(t) for t in opt_supports],
            "coverage_by_ordered_tuple": [
                {"terminal": list(t), "welfare": unit_values[t][1]}
                for t in terminals
            ],
        },
        "full_history_spe": {
            "ordered_decision_histories": len(histories),
            "all_actions_including_self_comparisons": len(comparisons),
            "nonself_comparisons": len(histories) * (p - 1),
            "strict_nonself_comparisons": strict,
            "tied_nonself_comparisons": tied,
            "minimum_nonself_slack": rational(min_nonself) if min_nonself is not None else None,
            "violation_count": len(violations),
            "is_full_pure_spe": not violations,
            "all_comparisons": comparisons,
        },
        "actual": {
            "terminal": list(actual),
            "payoffs": [rational(Fraction(v, scale)) for v in actual_profits_scaled],
            "welfare": actual_welfare,
            "twice_welfare_minus_optimum": 2 * actual_welfare - opt,
        },
        "static_assignment": {
            "definition": "sum_i u_i(T_pi(i), z_-i), with all other actual topics frozen",
            "topic_by_player_payoff_matrix": [
                [rational(v) for v in row] for row in static_table
            ],
            "optimal_tuple_permutation_checks": len(assignment_checks),
            "distinct_topic_assignments": len(distinct_assignments),
            "minimum_sum": rational(minimum),
            "maximum_sum": rational(maxima),
            "minimum_minus_actual_welfare": rational(minimum - actual_welfare),
            "minimizing_assignments": minimum_assignments,
            "every_optimal_assignment_exceeds_actual_welfare": all(
                v > actual_welfare for v in distinct_assignments.values()
            ),
            "all_checks": assignment_checks,
        },
        "conclusion": {
            "seq242_existential_optimal_assignment_bridge_is_refuted_by_this_input": (
                not violations and minimum > actual_welfare
            ),
            "q_cag_half_is_refuted_by_this_input": 2 * actual_welfare < opt,
            "general_q_cag_half_status": "OPEN",
            "novelty_claim": False,
        },
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "N": len(unit_interests),
        "histories": len(histories),
        "comparisons": len(comparisons),
        "spe_violations": len(violations),
        "actual": list(actual),
        "payoffs": [str(Fraction(v, scale)) for v in actual_profits_scaled],
        "W": actual_welfare,
        "OPT": opt,
        "optimum_supports": opt_supports,
        "minimum_static_sum": str(minimum),
        "minimum_static_gap": str(minimum - actual_welfare),
        "all_optimal_assignments_fail_bridge": minimum > actual_welfare,
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
