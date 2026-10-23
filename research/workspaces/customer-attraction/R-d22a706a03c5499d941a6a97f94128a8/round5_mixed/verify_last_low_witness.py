"""Direct exact last-two-player analysis of one three-block low-action barrier.

No BI/model imports. Each list entry represents a distinct unit customer.
"""
from fractions import Fraction as F
import json


CUSTOMERS = []
for block in range(3):
    for interested, amount in (((0,), 2), ((1, 3), 4), ((0, 2), 6), ((2, 3), 3), ((0, 1, 2, 3), 1)):
        for _ in range(amount):
            CUSTOMERS.append(tuple(4*block + a for a in interested))
assert len(CUSTOMERS) == 48


def add(profile, action):
    q = list(profile)
    q[action] += 1
    return tuple(q)


def payoff(profile, action):
    return sum((F(1, sum(profile[t] for t in interested))
                for interested in CUSTOMERS if action in interested), F(0))


def name(action):
    return "ABCD"[action % 4] + str(action // 4)


def main():
    witness = (1, 0, 1, 1, 2, 1, 0, 0, 2, 1, 0, 0)
    # Force the current (third-last) player to choose D1.
    background = add(witness, 7)
    immediate = [payoff(add(background, a), a) for a in range(12)]
    expected = [F(13,4), F(9,4), F(13,4), F(13,4), F(43,15), F(23,15),
                F(37,10), F(91,30), F(35,12), F(9,4), F(21,4), F(21,4)]
    assert immediate == expected
    choices = []
    for first in range(12):
        q = add(background, first)
        alternatives = [(payoff(add(q, last), last), last) for last in range(12)]
        best = max(value for value, _ in alternatives)
        br = [last for value, last in alternatives if value == best]
        choices.append([(add(q, last), last) for last in br])
    floor = max(min(payoff(q, a) for q, _ in choices[a]) for a in range(12))
    assert floor == F(37, 10)
    terminals = {q for a in range(12) for q, _ in choices[a] if payoff(q, a) >= floor}
    expected_terminals = {add(add(background, a), b) for a, b in ((6,10), (6,11), (10,11))}
    assert terminals == expected_terminals
    assert {last for _, last in choices[6]} == {10, 11}
    assert {last for _, last in choices[10]} == {6, 11}
    assert {last for _, last in choices[11]} == {6, 10}
    assert max(value for a, value in enumerate(immediate) if a not in (6,10,11)) == F(13,4)
    forced_player_payoffs = sorted({payoff(q, 7) for q in terminals})
    assert forced_player_payoffs == [F(37,10), F(21,4)]
    print(json.dumps({"status": "PASS", "scope": "one legal 9-player prefix, forced D1, exact last-two subtree",
                      "unit_customers": len(CUSTOMERS), "witness_counts": witness,
                      "insertion_table_after_D1": {name(a):str(v) for a,v in enumerate(immediate)},
                      "last_two_first_player_floor": str(floor),
                      "last_two_SPE_terminals": sorted(terminals),
                      "forced_D1_possible_payoffs": list(map(str, forced_player_payoffs)),
                      "D0_prescribed_target_payoff": "13/4", "D1_deviation_minimum": "37/10"}, indent=2))


if __name__ == "__main__":
    main()
