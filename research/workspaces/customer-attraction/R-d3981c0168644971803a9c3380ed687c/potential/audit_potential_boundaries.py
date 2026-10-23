"""Exact definition-level audit for the personal potential boundary note."""
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
import json
from pathlib import Path


def harmonic(n):
    return sum((F(1, j) for j in range(1, n + 1)), F(0))


def loads(topics, history, customers):
    return {x: sum(x in topics[a] for a in history) for x in customers}


def potential(topics, history, background, customers):
    c = loads(topics, history, customers)
    return sum((harmonic(background.get(x, 0) + c[x])
                - harmonic(background.get(x, 0)) for x in customers), F(0))


def payoffs(topics, history):
    customers = set().union(*topics.values())
    c = loads(topics, history, customers)
    return tuple(sum((F(1, c[x]) for x in topics[a]), F(0)) for a in history)


cross_topics = {
    "A": {1, 2}, "B": {3, 4}, "C": {1, 3}, "D": {2, 4},
    "U": {1, 2, 3, 4}, "E": {5},
}
exchange_checks = 0
for t in range(13):
    b = {x: t for x in range(1, 5)}
    for r in range(2, 11):
        padding = ("E",) * (r - 2)
        p, q = ("A", "B") + padding, ("C", "D") + padding
        before = potential(cross_topics, p, b, range(1, 6)) + potential(cross_topics, q, b, range(1, 6))
        for j, other in (("C", "D"), ("D", "C")):
            pp, qq = (j, "B") + padding, ("A", other) + padding
            after = potential(cross_topics, pp, b, range(1, 6)) + potential(cross_topics, qq, b, range(1, 6))
            assert before - after == F(2, (t + 1) * (t + 2)) > 0
            exchange_checks += 1


cycle_topics = {"A": {"a"}, "B": {"b"}, "C": {"a", "c"},
                "D": {"b", "d"}, "E": {"e"}}
r0 = {"A": "B", "B": "D", "C": "A", "D": "A", "E": "A"}
r1 = {"A": "C", "B": "A", "C": "A", "D": "A", "E": "A"}
cycle_states = (("A", r0), ("A", r1), ("B", r1), ("B", r0))
movers = (1, 0, 1, 0)
cycle_checks = 0
cycle_report = []
for m in range(2, 10):
    histories = [tuple([a, r[a]] + ["E"] * (m - 2)) for a, r in cycle_states]
    utilities = [payoffs(cycle_topics, h) for h in histories]
    for k, mover in enumerate(movers):
        assert utilities[(k + 1) % 4][mover] - utilities[k][mover] == F(1, 2)
        cycle_checks += 1
    if m == 2:
        cycle_report = [{"terminal": list(h), "payoffs": [str(v) for v in u]}
                        for h, u in zip(histories, utilities)]


def query(topics, a, history, background, customers):
    c = loads(topics, history, customers)
    return sum((F(1, background.get(x, 0) + 1 + c[x]) for x in topics[a]), F(0))


def difference(function, extra):
    result = F(0)
    for mask in range(1 << len(extra)):
        chosen = tuple(extra[i] for i in range(len(extra)) if mask >> i & 1)
        result += (-1) ** (len(extra) - len(chosen)) * function(chosen)
    return result


mixed_checks = 0
labels = ("A", "B", "C", "D", "U", "E")
for t in range(4):
    background = {x: t for x in range(1, 5)}
    for h in ((), ("A",), ("C", "D"), ("U", "A", "A")):
        c = loads(cross_topics, h, range(1, 6))
        for a in labels:
            for k in range(5):
                for extra in product(("A", "C", "U"), repeat=k):
                    actual = (-1) ** k * difference(
                        lambda chosen: query(cross_topics, a, h + chosen, background, range(1, 6)), extra)
                    intersection = set(cross_topics[a])
                    for z in extra:
                        intersection &= cross_topics[z]
                    expected = F(0)
                    for x in intersection:
                        d = background.get(x, 0) + 1 + c[x]
                        denominator = 1
                        for j in range(k + 1):
                            denominator *= d + j
                        expected += F(factorial(k), denominator)
                    assert actual == expected >= 0
                    mixed_checks += 1

report = {
    "status": "exact audit passed; no half theorem or SPE counterexample claimed",
    "exchange_checks": exchange_checks,
    "strict_strategy_cycle_checks": cycle_checks,
    "two_player_cycle": cycle_report,
    "complete_monotonicity_checks": mixed_checks,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
output = Path(__file__).with_name("potential_boundaries_audit.json")
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
