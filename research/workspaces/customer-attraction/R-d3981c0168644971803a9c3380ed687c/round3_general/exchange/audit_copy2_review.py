"""Independent COPY2 review from 35 explicitly distinct unit customers.

No author source, canonical model, BI solver, or certificate verifier is imported.
"""
from fractions import Fraction as Q
from itertools import product
import json


def audit():
    core = {f"c{i}" for i in range(6)}
    private = {f"p{i}" for i in range(12)}
    shared = {f"x{i}" for i in range(8)}
    y1 = {f"y1_{i}" for i in range(2)}
    y2 = {f"y2_{i}" for i in range(2)}
    z = {f"z{i}" for i in range(5)}
    topics = [core | private, shared, y1 | y2 | z,
              core | shared | y1, core | shared | y2]
    names = ["A", "E", "D", "F1", "F2"]
    assert len(set.union(*topics)) == 35
    assert list(map(len, topics)) == [18, 8, 9, 16, 16]
    assert len({frozenset(a) for a in topics}) == 5

    def utility(terminal, player):
        return sum((Q(1, sum(client in topics[a] for a in terminal))
                    for client in topics[terminal[player]]), Q())

    # First complete all final nodes by the lowest-index best reply.
    last = {}
    for first, second in product(range(5), repeat=2):
        values = [utility((first, second, a), 2) for a in range(5)]
        last[first, second] = min(a for a in range(5) if values[a] == max(values))

    # Independently check and install the five specified replies in the A child.
    specified = [3, 2, 3, 4, 3]
    last_a_rows = []
    for second, action in enumerate(specified):
        values = [utility((0, second, a), 2) for a in range(5)]
        assert values[action] == max(values)
        last[0, second] = action
        last_a_rows.append(list(map(str, values)))

    second = {}
    second_rows = []
    for first in range(5):
        values = [utility((first, a, last[first, a]), 1) for a in range(5)]
        second[first] = min(a for a in range(5) if values[a] == max(values))
        if first == 0:
            second[first] = 1
        assert values[second[first]] == max(values)
        second_rows.append(list(map(str, values)))

    policy = {(): 0}
    policy.update({(a,): b for a, b in second.items()})
    policy.update({(a, b): c for (a, b), c in last.items()})

    def leaf(history):
        history = tuple(history)
        while len(history) < 3:
            history += (policy[history],)
        return history

    comparisons = 0
    minimum_slack = None
    for history in policy:
        player = len(history)
        actual_value = utility(leaf(history), player)
        for forced in range(5):
            alternative_value = utility(leaf(history + (forced,)), player)
            slack = actual_value - alternative_value
            assert slack >= 0, (history, forced, slack)
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            comparisons += 1
    assert len(policy) == 31 and comparisons == 155

    actual = leaf(())
    copied = leaf((0, 0))
    original_profit = utility(actual, 0)
    copied_profit = utility(copied, 1)
    assert actual == (0, 1, 2)
    assert copied == (0, 0, 3)
    assert original_profit == 18 and copied_profit == 8
    assert copied_profit < original_profit / 2
    assert utility(actual, 0) > 2 * utility(actual, 1)
    welfare = len(set.union(*(topics[a] for a in actual)))
    optimum = max(len(set.union(*(topics[a] for a in terminal)))
                  for terminal in product(range(5), repeat=3))
    assert welfare == optimum == 35
    return {
        "customers": 35,
        "names": names,
        "topic_sizes": list(map(len, topics)),
        "last_payoffs_after_A": last_a_rows,
        "second_payoffs": second_rows,
        "second_actions": [names[second[a]] for a in range(5)],
        "last_action_table": [[names[last[a, b]] for b in range(5)] for a in range(5)],
        "root_deviation_profits": [str(utility(leaf((a,)), 0)) for a in range(5)],
        "decision_nodes": len(policy),
        "SPE_comparisons_including_self": comparisons,
        "minimum_SPE_slack": str(minimum_slack),
        "actual_leaf": [names[a] for a in actual],
        "actual_profits": [str(utility(actual, i)) for i in range(3)],
        "copy_leaf": [names[a] for a in copied],
        "copy_profits": [str(utility(copied, i)) for i in range(3)],
        "copy2_deficit": str(original_profit / 2 - copied_profit),
        "actual_profit_ratio2_gap": str(utility(actual, 0) - 2 * utility(actual, 1)),
        "welfare": welfare,
        "optimum": optimum,
        "scope": "COPY2 and u1<=2u2 both fail; half is met.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
