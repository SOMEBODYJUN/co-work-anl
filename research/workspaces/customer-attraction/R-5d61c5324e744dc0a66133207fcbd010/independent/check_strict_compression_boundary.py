"""Exact definition-level check of the strict ordered-compression obstruction."""

from fractions import Fraction
import argparse
import itertools
import json
from pathlib import Path


def build(length):
    C = 20 * (length + 1) ** 2
    sizes = [C + 3 * i for i in range(length + 1)]
    types = {}
    overlaps = {}
    for i, j in itertools.combinations(range(length + 1), 2):
        if (i, j) == (0, 1):
            count = 2
        elif j == i + 1:
            count = 6 * i + (10 if j == length else 6)
        else:
            count = 6 * (i + j) + 6
        types[frozenset((i, j))] = count
        overlaps[i, j] = count
    for i, size in enumerate(sizes):
        shared = sum(count for (a, b), count in overlaps.items() if i in (a, b))
        assert size > shared
        types[frozenset((i,))] = size - shared
    return C, sizes, types


def payoff(types, first, last, player):
    chosen = first if player == 0 else last
    return sum((Fraction(count, int(first in mask) + int(last in mask))
                for mask, count in types.items() if chosen in mask), Fraction())


def welfare(types, first, last):
    return sum(count for mask, count in types.items()
               if first in mask or last in mask)


def check(length):
    C, sizes, types = build(length)
    p = C - 1
    menu = tuple(range(length + 1))
    replies = []
    root_payoffs = []
    strict_gap = None
    for first in menu:
        values = {last: payoff(types, first, last, 1) for last in menu}
        ordered = sorted(menu, key=values.get, reverse=True)
        assert values[ordered[0]] > values[ordered[1]]
        gap = values[ordered[0]] - values[ordered[1]]
        strict_gap = gap if strict_gap is None else min(strict_gap, gap)
        expected = first + 1 if first < length else length - 1
        assert ordered[0] == expected
        replies.append(expected)
        root_payoffs.append(payoff(types, first, expected, 0))
    assert root_payoffs == [Fraction(p)] + [Fraction(p - 2)] * (length - 2) + [Fraction(p - 4), Fraction(p - 1)]
    assert root_payoffs[0] > max(root_payoffs[1:])
    optimal = max(welfare(types, a, b) for a in menu for b in menu)
    optimal_pairs = {(a, b) for a in menu for b in menu
                     if welfare(types, a, b) == optimal}
    assert optimal == 2 * C + 1
    assert optimal_pairs == {(0, 1), (1, 0)}

    subset_count = 0
    min_deviation_gap = None
    for optional_mask in range(1 << (length - 1)):
        retained = {0, 1} | {i for i in range(2, length + 1)
                            if optional_mask >> (i - 2) & 1}
        if len(retained) == length + 1:
            continue
        missing = min(set(menu) - retained)
        deviant = missing - 1
        prev = deviant - 1
        values = {last: payoff(types, deviant, last, 1) for last in retained}
        assert all(values[prev] > value for last, value in values.items()
                   if last != prev)
        gap = payoff(types, deviant, prev, 0) - p
        assert gap == (3 if deviant == 1 else 1)
        min_deviation_gap = gap if min_deviation_gap is None else min(min_deviation_gap, gap)
        subset_count += 1
    return {"L": length, "topics": length + 1, "players": 2,
            "customer_count": sum(types.values()), "C": C,
            "sizes": sizes, "strict_last_replies": replies,
            "root_payoffs": [str(value) for value in root_payoffs],
            "minimum_last_reply_strict_gap": str(strict_gap),
            "welfare_equals_unique_optimum": optimal,
            "proper_retained_subcatalogs_checked": subset_count,
            "minimum_forced_root_deviation_gain": str(min_deviation_gap)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-L", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"scope": "finite definition-level check; the uniform proof is symbolic",
              "checks": [check(length) for length in range(3, args.max_L + 1)]}
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(payload)
    else:
        print(payload, end="")
