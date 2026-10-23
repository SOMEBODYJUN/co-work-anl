"""Definition-level audit; no customer_attraction solver import."""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def payoff(topics, path, player):
    return sum((Fraction(1, sum(x in topics[a] for a in path))
                for x in topics[path[player]]), Fraction())


def two_player_equilibria(topics):
    p = len(topics)
    result = []
    for first in range(p):
        for replies in product(range(p), repeat=p):
            if any(payoff(topics, (a, replies[a]), 1)
                   < payoff(topics, (a, b), 1)
                   for a in range(p) for b in range(p)):
                continue
            actual = payoff(topics, (first, replies[first]), 0)
            if any(actual < payoff(topics, (a, replies[a]), 0)
                   for a in range(p)):
                continue
            result.append((first, replies))
    return result


def counts(path, p):
    return tuple(path.count(a) for a in range(p))


def boundary_checks():
    # Every strategy is an SPE in the all-zero game, including empty topics.
    zero = (frozenset(), frozenset())
    assert len(two_player_equilibria(zero)) == 2 ** 3
    # One player always maximizes plain coverage; empty and duplicate topics
    # are allowed, and ties must all survive.
    topics = (frozenset(), frozenset({0}), frozenset({0}))
    best = max(payoff(topics, (a,), 0) for a in range(3))
    assert [a for a in range(3) if payoff(topics, (a,), 0) == best] == [1, 2]
    # A two-player one-topic instance is forced and pays exactly one half.
    one = (frozenset({0}),)
    assert two_player_equilibria(one) == [(0, (0,))]
    assert payoff(one, (0, 0), 0) == Fraction(1, 2)


def main():
    boundary_checks()
    topics = (frozenset({0, 1}), frozenset({0, 1, 2}), frozenset({2, 3}))
    p = len(topics)
    expected_table = (
        (Fraction(1), Fraction(2), Fraction(2)),
        (Fraction(1), Fraction(3, 2), Fraction(3, 2)),
        (Fraction(2), Fraction(5, 2), Fraction(1)),
    )
    table = tuple(tuple(payoff(topics, (a, b), 1) for b in range(p))
                  for a in range(p))
    assert table == expected_table
    best_replies = tuple(tuple(b for b in range(p) if table[a][b] == max(table[a]))
                         for a in range(p))
    assert best_replies == ((1, 2), (1, 2), (1,))
    child_root = tuple(tuple(payoff(topics, (a, b), 0) for b in best_replies[a])
                       for a in range(p))
    threshold = max(map(min, child_root))
    assert threshold == Fraction(3, 2)
    equilibria = two_player_equilibria(topics)
    outcomes = sorted({counts((a, replies[a]), p) for a, replies in equilibria})
    assert outcomes == [(0, 1, 1), (0, 2, 0), (1, 0, 1)]
    assert len(equilibria) == 5

    def moment(path):
        return sum(sum(x in topics[a] for a in path) for x in (2, 3))

    assert all(moment((a, replies[a])) >= 2 for a, replies in equilibria)
    mixed_moment = (moment((0, 1)) + moment((0, 2))) / Fraction(2)
    mixed_root = (payoff(topics, (0, 1), 0) + payoff(topics, (0, 2), 0)) / 2
    assert mixed_moment == Fraction(3, 2) < 2
    assert mixed_root == threshold
    # Public chance after A chooses B,C; the other branches choose B.
    deviations = (mixed_root, payoff(topics, (1, 1), 0),
                  payoff(topics, (2, 1), 0))
    assert deviations == (threshold,) * 3
    for a, bs in enumerate(((1, 2), (1,), (1,))):
        assert all(table[a][b] == max(table[a]) for b in bs)

    report = {
        "status": "boundary checks and independent complete-strategy audit passed",
        "all_formal_pure_strategies": p ** (1 + p),
        "spe_strategies": len(equilibria),
        "spe_terminal_counts": outcomes,
        "last_player_payoff_table": [[str(x) for x in row] for row in table],
        "root_floor": str(threshold),
        "pure_spe_moment_lower_bound": "2",
        "convex_child_point_moment": str(mixed_moment),
        "public_chance_root_deviation_values": list(map(str, deviations)),
        "main_half_claim": "OPEN; this is not a half counterexample",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    Path(__file__).with_name("audit_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
