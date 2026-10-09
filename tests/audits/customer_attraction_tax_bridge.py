"""Definition-level exact audit of the zero-background first-step tax failure.

The complete ordered-history certificate and all optimization values are checked
directly after expanding the fifteen unit customers. This imports neither the
canonical outcome recurrence nor its certificate verifier. The accompanying
proof is an explicit finite counterexample, not a universal theorem inferred
from a search count.
"""

from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import platform
import subprocess


def run():
    root = Path(__file__).resolve().parents[2]
    input_path = root / "examples/customer_attraction/tax_bridge_failure.json"
    instance = json.loads(input_path.read_text())
    labels = instance["topics"]
    players = instance["players"]
    p = len(labels)
    units = tuple(frozenset(customer["topics"])
                  for customer in instance["customers"]
                  for _ in range(customer["multiplicity"]))
    assert players == 3 and p == 4 and len(units) == 15

    def payoff(path, position):
        action = path[position]
        return sum((Fraction(1, sum(topic in customer for topic in path))
                    for customer in units if action in customer), Fraction(0))

    def residual_value(background, path):
        result = Fraction(0)
        for customer in units:
            incumbent = sum(topic in customer for topic in background)
            current = sum(topic in customer for topic in path)
            if current:
                result += Fraction(current, incumbent + current)
        return result

    def tax(background, path):
        return sum((Fraction(1, 1 + sum(topic in customer for topic in background))
                    - Fraction(1, 1 + sum(topic in customer for topic in background)
                               + sum(topic in customer for topic in path))
                    for customer in units), Fraction(0))

    def optimum(background, remaining):
        candidates = tuple(combinations_with_replacement(range(p), remaining))
        values = {path: residual_value(background, path) for path in candidates}
        maximum = max(values.values())
        return maximum, tuple(path for path, value in values.items() if value == maximum)

    # Full history dependence is retained: the map explicitly covers every node.
    actions = {history: 1 for length in range(players)
               for history in product(range(p), repeat=length)}
    node_table = []
    checked_deviations = 0

    def walk(history):
        nonlocal checked_deviations
        if len(history) == players:
            return history
        terminal = [walk(history + (action,)) for action in range(p)]
        chosen = actions[history]
        chosen_value = payoff(terminal[chosen], len(history))
        alternatives = [payoff(path, len(history)) for path in terminal]
        for alternative in range(p):
            if alternative != chosen:
                assert chosen_value >= alternatives[alternative]
                checked_deviations += 1
        node_table.append({
            "history": list(history),
            "chosen": chosen,
            "branch_terminal_histories": [list(path) for path in terminal],
            "branch_payoffs": [str(value) for value in alternatives],
        })
        return terminal[chosen]

    actual = walk(())
    assert actual == (1, 1, 1)
    assert len(actions) == 21 and checked_deviations == 63
    actual_payoffs = tuple(payoff(actual, i) for i in range(players))
    assert actual_payoffs == (Fraction(3),) * 3
    actual_welfare = len([customer for customer in units
                          if any(topic in customer for topic in actual)])
    assert actual_welfare == 9

    # Independently check the stronger finite fact used by the direct proof:
    # B weakly dominates each leaf against every pair of fixed other actions.
    dominance_checks = 0
    for others in product(range(p), repeat=players - 1):
        good = payoff((1,) + others, 0)
        for leaf in (0, 2, 3):
            assert good >= payoff((leaf,) + others, 0)
            dominance_checks += 1
    assert dominance_checks == 48

    root_optima = {remaining: optimum((), remaining)
                   for remaining in (1, 2, 3)}
    assert [root_optima[k][0] for k in (1, 2, 3)] == [9, 11, 15]
    after_B = optimum((1,), 2)
    after_BB = optimum((1, 1), 1)
    assert after_B[0] == 7 and after_BB[0] == 3
    first_tax = tax((), (1,))
    assert first_tax == Fraction(9, 2)
    bridge_right = actual_payoffs[0] + first_tax + after_B[0]
    bridge_gap = root_optima[3][0] - bridge_right
    assert bridge_right == Fraction(29, 2) and bridge_gap == Fraction(1, 2)
    entire_tax = tax((), actual[:-1])
    total_tax_right = sum(actual_payoffs) + entire_tax
    assert entire_tax == 6 and total_tax_right == root_optima[3][0] == 15

    pair_values = [{
        "themes": list(path),
        "value": str(residual_value((1,), path)),
    } for path in combinations_with_replacement(range(p), 2)]
    strategy = {
        "terminal_counts": [0, 3, 0, 0],
        "actions": [{"history": list(history), "action": action}
                    for history, action in sorted(actions.items(),
                                                  key=lambda item: (len(item[0]), item[0]))],
    }
    return {
        "audit": "customer_attraction_first_step_tax_bridge_failure",
        "scope": "exact finite counterexample to equation (9); total root tax equality",
        "arithmetic": "fractions.Fraction on individually expanded unit customers",
        "python_version": platform.python_version(),
        "base_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "unit_customers": len(units),
        "legal_prefix": [],
        "remaining_players": players,
        "full_strategy_certificate": strategy,
        "verified_decision_histories": len(actions),
        "verified_actual_continuation_deviations": checked_deviations,
        "weak_dominance_checks": dominance_checks,
        "actual_path": list(actual),
        "actual_payoffs": [str(value) for value in actual_payoffs],
        "actual_welfare": actual_welfare,
        "root_optima": {str(k): {"value": str(value),
                                 "attaining_theme_multisets": [list(path) for path in paths]}
                        for k, (value, paths) in root_optima.items()},
        "F2_after_B": str(after_B[0]),
        "F2_after_B_all_theme_pairs": pair_values,
        "F1_after_BB": str(after_BB[0]),
        "first_step_tax": str(first_tax),
        "first_step_bridge_rhs": str(bridge_right),
        "first_step_bridge_violation": str(bridge_gap),
        "entire_tax": str(entire_tax),
        "total_tax_rhs": str(total_tax_right),
        "total_tax_is_equality": True,
        "main_half_coverage_target_is_satisfied": True,
        "complete_node_incentive_table": sorted(node_table,
                                                 key=lambda row: (len(row["history"]), row["history"])),
        "universal_claim_from_finite_search": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
