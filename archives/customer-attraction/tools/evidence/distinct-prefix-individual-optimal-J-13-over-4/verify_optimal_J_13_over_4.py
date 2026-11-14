"""Exact check of the 13/4 distinct-prefix individual cone with optimal J."""

import json
from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations, product


TOPICS = tuple(range(5))
PLAYERS = 4
J = frozenset((0, 1, 3, 4))
MASKS = range(1, 1 << len(TOPICS))
CUSTOMERS = {1: 11, 5: 5, 6: 12, 12: 12, 20: 12}


def includes(mask, action):
    return bool(mask & (1 << action))


def strategy(h):
    return 2 if any(h) else 0


@cache
def finish(h):
    return h if len(h) == PLAYERS else finish(h + (strategy(h),))


def payoff(mask, action, terminal):
    if not includes(mask, action):
        return Fraction(0)
    return Fraction(1, sum(includes(mask, a) for a in terminal))


def coefficient(mask, h, a):
    return payoff(mask, strategy(h), finish(h)) - payoff(mask, a, finish(h + (a,)))


def coverage(mask, group):
    return int(any(includes(mask, a) for a in group))


def check():
    histories = [h for length in range(PLAYERS) for h in product(TOPICS, repeat=length)]
    individual = {
        (h, a): sum(coefficient(mask, h, a) * count for mask, count in CUSTOMERS.items())
        for h in histories
        for a in TOPICS
    }
    retained = {h: J.difference(h) for h in histories if len(h) == len(set(h)) and J.issuperset(h)}
    kept_rows = {(h, a): individual[h, a] for h, alternatives in retained.items() for a in sorted(alternatives)}
    average_rows = {
        h: sum(kept_rows[h, a] for a in alternatives) / len(alternatives)
        for h, alternatives in retained.items()
    }
    assert len(retained) == 41 and len(kept_rows) == 64 and len(individual) == 780
    assert len([k for k in kept_rows if k[1] != strategy(k[0])]) == 63
    assert min(kept_rows.values()) == min(average_rows.values()) == 0
    assert finish(()) == (0, 0, 0, 0)

    def witness_coverage(group):
        return sum(coverage(mask, group) * count for mask, count in CUSTOMERS.items())

    W, O = witness_coverage(finish(())), witness_coverage(J)
    OPT = max(witness_coverage(group) for group in combinations(TOPICS, PLAYERS))
    assert (W, O, OPT) == (16, 52, 52)
    assert O == sum(CUSTOMERS.values()) == W * Fraction(13, 4)

    queried = (1, 3, 4)
    assert all(kept_rows[(0,), a] == 0 for a in queried)
    columns = []
    for mask in MASKS:
        w = coverage(mask, finish(()))
        o = coverage(mask, J)
        rows = [coefficient(mask, (0,), a) for a in queried]
        rho = Fraction(13, 4) * w - o - 3 * sum(rows)
        anchor = int(includes(mask, 0))
        middle = int(includes(mask, 2))
        count = sum(includes(mask, a) for a in queried)
        assert rho == anchor + Fraction(3 * count, anchor + 1 + 2 * middle) - int(anchor + count > 0)
        assert rho >= 0
        if mask in CUSTOMERS:
            assert rho == 0
        columns.append({"mask": mask, "dual_rows": list(map(str, rows)), "remainder": str(rho)})

    negatives = [(h, a, str(v)) for (h, a), v in individual.items() if v < 0]
    assert len(negatives) == 13 and individual[(), 2] == Fraction(-25, 4)
    full_average = {h: sum(individual[h, a] for a in J) / len(J) for h in histories}
    assert {h: v for h, v in full_average.items() if v < 0} == {(0, 0): Fraction(-3, 2), (0, 0, 0): -6}
    return {
        "strategy": "Four positions, five labels; sigma(h)=0 iff all actions in h are zero, else 2.",
        "J": sorted(J),
        "witness_customers": CUSTOMERS,
        "W": W,
        "O_J": O,
        "OPT": OPT,
        "max_O_J_over_W": "13/4",
        "kept_histories": len(retained),
        "kept_individual_rows": len(kept_rows),
        "kept_individual_slack_histogram": {str(s): n for s, n in sorted(Counter(kept_rows.values()).items())},
        "kept_individual_slacks": [(h, a, str(v)) for (h, a), v in kept_rows.items()],
        "kept_average_slacks": [(h, str(v)) for h, v in average_rows.items()],
        "dual_rows": [{"history": [0], "alternative": a, "weight": 3} for a in queried],
        "columns": columns,
        "true_ic_negatives": negatives,
        "negative_full_J_averages": [(h, str(v)) for h, v in full_average.items() if v < 0],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
