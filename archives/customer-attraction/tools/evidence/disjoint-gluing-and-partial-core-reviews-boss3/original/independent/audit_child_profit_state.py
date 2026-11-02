"""Independent expanded-unit audit of a specified aggregate-child relaxation.

Does not import the canonical model/solver or the proposed probe.
Prints a result or writes a new JSON file with exclusive creation.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json


def audit():
    root = Path(__file__).resolve().parents[5]
    data = json.loads((root / "examples/customer_attraction/root_tax_failure.json").read_text())
    labels = data["topics"]
    clients = [frozenset(t["topics"]) for t in data["customers"]
               for _ in range(t["multiplicity"])]
    assert len(clients) == 61

    def payoffs(profile):
        result = [Fraction(0) for _ in profile]
        for interests in clients:
            attracted = [i for i, a in enumerate(profile) if a in interests]
            if attracted:
                for i in attracted:
                    result[i] += Fraction(1, len(attracted))
        return tuple(result)

    def welfare(profile):
        return sum(any(a in interests for a in profile) for interests in clients)

    menus = [(0, 0, 0), (0, 0, 1), (0, 0, 2),
             (0, 0, 3), (0, 4, 4), (0, 5, 5)]
    branches = []
    for a, tail in enumerate(menus):
        values = [(sum(payoffs((a,) + q)[1:]), q)
                  for q in product(range(6), repeat=3)]
        optimum = max(v for v, q in values)
        optimizers = [q for v, q in values if v == optimum]
        profile = (a,) + tail
        utilities = payoffs(profile)
        tail_profit = sum(utilities[1:])
        assert tail_profit >= Fraction(3, 5) * optimum
        assert tail_profit >= Fraction(5, 8) * optimum
        branches.append({
            "root_action": labels[a],
            "tail": [labels[b] for b in tail],
            "F3": str(optimum),
            "F3_one_optimizer": [labels[b] for b in optimizers[0]],
            "F3_ordered_optimizer_count": len(optimizers),
            "root_payoff": str(utilities[0]),
            "tail_profit": str(tail_profit),
            "three_fifths_floor": str(Fraction(3, 5) * optimum),
            "profit_slack": str(tail_profit - Fraction(3, 5) * optimum),
            "tail_profit_over_F3": str(tail_profit / optimum),
            "terminal_welfare": welfare(profile),
        })
    root_values = [payoffs((a,) + menus[a])[0] for a in range(6)]
    assert root_values[0] == max(root_values) == Fraction(15, 2)
    optimum4 = max(welfare(q) for q in product(range(6), repeat=4))
    assert optimum4 == 61
    actual_welfare = welfare((0, 0, 0, 0))
    assert actual_welfare == 30 and 2 * actual_welfare < optimum4
    last_values = [payoffs((0, 0, 0, a))[-1] for a in range(6)]
    assert last_values == [Fraction(15, 2), Fraction(10), Fraction(11),
                           Fraction(10), Fraction(11), Fraction(11)]
    assert last_values[2] > last_values[0]
    expected_f3 = [36, 51, 50, 51, 42, 42]
    expected_tail = [Fraction(45, 2), Fraction(35), Fraction(71, 2),
                     Fraction(35), Fraction(97, 3), Fraction(97, 3)]
    expected_root = [Fraction(15, 2), Fraction(5), Fraction(11, 2),
                     Fraction(5), Fraction(17, 3), Fraction(17, 3)]
    assert [Fraction(b["F3"]) for b in branches] == expected_f3
    assert [Fraction(b["tail_profit"]) for b in branches] == expected_tail
    assert root_values == expected_root

    # Independently replay the actual complete original SPE, rather than the
    # relaxed menus. First three movers choose A; last mover has F>E>...>A ties.
    def original_action(history):
        if len(history) < 3:
            return 0
        return max(range(6), key=lambda a: (payoffs(history + (a,))[-1], a))

    def original_terminal(history):
        while len(history) < 4:
            history += (original_action(history),)
        return history

    comparison_count = 0
    minimum_gap = None
    for length in range(4):
        for history in product(range(6), repeat=length):
            actual = original_terminal(history)
            follow_value = payoffs(actual)[length]
            for a in range(6):
                alternative = original_terminal(history + (a,))
                gap = follow_value - payoffs(alternative)[length]
                assert gap >= 0
                minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
                comparison_count += 1
    actual_original = original_terminal(())
    assert actual_original == (0, 0, 0, 5)
    original_utilities = payoffs(actual_original)
    assert original_utilities == (Fraction(9), Fraction(9), Fraction(9), Fraction(11))
    f3_after_A = Fraction(branches[0]["F3"])
    assert optimum4 - f3_after_A == 25 > 2 * original_utilities[0] == 18
    return {
        "status": "exact_relaxation_countermodel_not_SPE",
        "unit_clients": len(clients),
        "root_child_enumerations": 6 * 6 ** 3,
        "root_menu_comparisons": 6,
        "four_player_optimum_enumerations": 6 ** 4,
        "branches": branches,
        "menu_root_action": "A",
        "menu_root_welfare": actual_welfare,
        "OPT4": optimum4,
        "half_gap_2W_minus_OPT": 2 * actual_welfare - optimum4,
        "last_node_AAA_action_values": dict(zip(labels, map(str, last_values))),
        "non_SPE_witness": "At ordered history AAA, the listed fourth A pays 15/2; C pays 11.",
        "original_complete_SPE": {
            "rule": "First three A; last exact best reply with F>E>D>C>B>A ties.",
            "verified_ordered_nodes": sum(6 ** t for t in range(4)),
            "verified_action_comparisons_including_self": comparison_count,
            "minimum_incentive_gap": str(minimum_gap),
            "actual_path": [labels[a] for a in actual_original],
            "actual_payoffs": list(map(str, original_utilities)),
            "F4_zero": optimum4,
            "F3_after_A": str(f3_after_A),
            "opportunity_gap": str(optimum4 - f3_after_A),
            "twice_root_utility": str(2 * original_utilities[0]),
            "violated_candidate": "F4(0)-F3(1_A) <= 2 u1",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(rendered)
    print(rendered)
