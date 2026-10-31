"""Independent exact audit of a fixed-background tail-PNE domination counterexample.

No imports from parent code, canonical solvers, or stored certificates.
"""
from fractions import Fraction
from itertools import product
import json


MULTIPLICITY = {
    2: 7, 16: 1, 20: 6, 26: 4, 29: 1, 31: 1, 33: 5,
    35: 5, 39: 6, 45: 5, 47: 7, 55: 1, 58: 4, 62: 1,
}
REPLY = [1, 5, 5, 5, 5, 2]


def payoff(player, outcome):
    # Each multiplicity expands into distinct unit customers.
    total = Fraction()
    for mask, number in MULTIPLICITY.items():
        if (mask >> outcome[player]) & 1:
            load = sum((mask >> action) & 1 for action in outcome)
            total += Fraction(number, load)
    return total


def main():
    terminal_rows = []
    for first_action in range(6):
        values = [payoff(2, (1, first_action, last_action)) for last_action in range(6)]
        maxima = [action for action, value in enumerate(values) if value == max(values)]
        assert maxima == [REPLY[first_action]]
        terminal_rows.append({
            "first_tail_action": first_action,
            "last_tail_payoffs": list(map(str, values)),
            "unique_best_reply": maxima[0],
        })
    first_values = [payoff(1, (1, a, REPLY[a])) for a in range(6)]
    assert first_values == list(map(Fraction, ["53/3", "14", "15", "10", "25/2", "17"]))
    assert first_values[0] > max(first_values[1:])
    actual_old = payoff(0, (1, 0, REPLY[0]))
    assert actual_old == Fraction(44, 3)

    static_pne = []
    static_comparisons = 0
    for first_action, second_action in product(range(6), repeat=2):
        outcome = (1, first_action, second_action)
        stable = True
        for player in [1, 2]:
            for alternative in range(6):
                deviated = list(outcome)
                deviated[player] = alternative
                static_comparisons += 1
                if payoff(player, deviated) > payoff(player, outcome):
                    stable = False
        if stable:
            static_pne.append({
                "tail_actions": [first_action, second_action],
                "all_payoffs": [str(payoff(i, outcome)) for i in range(3)],
            })
    assert [row["tail_actions"] for row in static_pne] == [[2, 5], [5, 2]]
    assert all(row["all_payoffs"][0] == "21" for row in static_pne)
    print(json.dumps({
        "unit_customers": sum(MULTIPLICITY.values()),
        "fixed_old_action": 1,
        "tail_prescription": {"first": 0, "last_reply": REPLY},
        "last_tail_rows": terminal_rows,
        "first_tail_true_payoffs": list(map(str, first_values)),
        "actual_old_payoff": str(actual_old),
        "static_tail_profiles_checked": 36,
        "static_individual_comparisons_including_self": static_comparisons,
        "static_tail_pne": static_pne,
        "strict_old_payoff_gap": str(Fraction(21) - actual_old),
        "scope": "Fixed-background two-tail SPE only; no full-root SPE claim.",
    }, indent=2))


if __name__ == "__main__":
    main()
