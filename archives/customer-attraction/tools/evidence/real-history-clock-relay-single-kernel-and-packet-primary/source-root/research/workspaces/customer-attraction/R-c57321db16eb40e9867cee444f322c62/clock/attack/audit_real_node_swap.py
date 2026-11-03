#!/usr/bin/env python3
"""Exact full-history replay of two tiny chronological swap obstructions.

No solver or history compression is used. Every ordered history and unilateral
action is replayed under the one supplied complete strategy.
"""

from fractions import Fraction as F
from itertools import product
import json


def check(name, themes, root, middle, terminal):
    labels = tuple(themes)
    sigma = {(): root}
    sigma.update({(a,): middle[a] for a in labels})
    sigma.update({tuple(ab): c for ab, c in terminal.items()})

    def replay(history):
        history = tuple(history)
        while len(history) < 3:
            history += (sigma[history],)
        return history

    def payoff(path, i):
        return sum((F(1, sum(x in themes[a] for a in path))
                    for x in themes[path[i]]), F(0))

    def welfare(path):
        return len(set().union(*(themes[a] for a in path)))

    comparisons = []
    for depth in range(3):
        for history in product(labels, repeat=depth):
            actual = replay(history)
            value = payoff(actual, depth)
            for action in labels:
                deviation = replay(history + (action,))
                dev_value = payoff(deviation, depth)
                assert value >= dev_value, (name, history, action)
                comparisons.append({
                    "history": "".join(history), "action": action,
                    "actual": "".join(actual), "deviation": "".join(deviation),
                    "actual_value": str(value), "deviation_value": str(dev_value),
                })

    actual = replay(())
    swapped_prefix = (actual[1], actual[0])
    true_swap = replay(swapped_prefix)
    frozen_swap = swapped_prefix + actual[2:]
    result = {
        "name": name, "nodes": len(sigma), "comparisons": len(comparisons),
        "actual": "".join(actual), "true_swapped": "".join(true_swap),
        "frozen_swapped": "".join(frozen_swap),
        "actual_payoffs": list(map(str, (payoff(actual, i) for i in range(3)))),
        "true_swapped_payoffs": list(map(str, (payoff(true_swap, i) for i in range(3)))),
        "frozen_swapped_payoffs": list(map(str, (payoff(frozen_swap, i) for i in range(3)))),
        "welfares": [welfare(p) for p in (actual, true_swap, frozen_swap)],
        "all_comparisons": comparisons,
    }
    assert true_swap != frozen_swap
    return result


results = [
    check("two_singletons_individual", {"A": {0}, "B": {1}}, "A",
          {"A": "B", "B": "A"},
          {"AA": "B", "AB": "B", "BA": "A", "BB": "A"}),
    check("five_customers_aggregate", {"A": {0, 1}, "B": {2, 3}, "C": {4}}, "B",
          {"A": "B", "B": "A", "C": "A"},
          {"AA": "B", "AB": "A", "AC": "B", "BA": "C", "BB": "A",
           "BC": "A", "CA": "B", "CB": "A", "CC": "A"}),
]
assert results[0]["welfares"] == [2, 2, 2]
assert results[1]["welfares"] == [5, 4, 5]
print(json.dumps({"status": "pass", "results": results}, indent=2))
