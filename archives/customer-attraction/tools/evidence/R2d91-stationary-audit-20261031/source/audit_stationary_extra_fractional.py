"""Exact check of one specified general construction, not a half counterexample.

The candidate was: take a stationary distribution of the mean true-tail
transition kernel, and use r times that distribution as a fractional static
background; its maximum extra query price should be <= the root SPE payoff.
No solver or discovery output is imported here.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import argparse
import json
from pathlib import Path


WEIGHTS = {
    1: 15, 2: 177, 4: 157, 9: 285, 10: 8, 12: 12, 13: 9,
    16: 202, 17: 9, 26: 3, 29: 36, 33: 77, 34: 33, 35: 9,
    36: 61, 42: 60, 43: 12, 44: 48, 46: 12, 48: 40, 50: 9,
}
CLIENTS = tuple(mask for mask, count in WEIGHTS.items() for _ in range(count))
TOPICS = range(6)
R = 3


def action(history):
    if len(history) == 0:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    group = range(3) if history[1] < 3 else range(3, 6)
    return min(a for a in group if a not in history)


def terminal(history):
    while len(history) < R:
        history += (action(history),)
    return history


def payoff(topic, profile):
    return sum(
        (F(1, sum(bool(mask & (1 << a)) for a in profile))
         for mask in CLIENTS if mask & (1 << topic)), F(0)
    )


def query_prices(q, mass):
    return [sum(
        (F(1) / (1 + mass * sum(q[a] for a in TOPICS if mask & (1 << a)))
         for mask in CLIENTS if mask & (1 << t)), F(0)
    ) for t in TOPICS]


def main():
    histories = 0
    comparisons = 0
    minimum_slack = None
    for length in range(R):
        for history in product(TOPICS, repeat=length):
            histories += 1
            topic = action(history)
            actual = payoff(topic, terminal(history))
            for alternative in TOPICS:
                comparisons += 1
                slack = actual - payoff(alternative, terminal(history + (alternative,)))
                assert slack >= 0, (history, alternative, slack)
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)

    actual_profile = terminal(())
    profits = [payoff(a, actual_profile) for a in actual_profile]
    welfare = sum(profits)
    optimum = max(sum(any(mask & (1 << a) for a in z) for mask in CLIENTS)
                  for z in combinations_with_replacement(TOPICS, R))

    # Every X root has tail (3,4); every Y root has tail (0,1).
    kernel = [[F(terminal((a,))[1:].count(b), R - 1) for b in TOPICS]
              for a in TOPICS]
    pi = [F(1, 4), F(1, 4), F(0), F(1, 4), F(1, 4), F(0)]
    assert [sum(pi[a] * kernel[a][b] for a in TOPICS) for b in TOPICS] == pi
    prices = query_prices(pi, R)
    assert prices[2] - profits[0] == F(1149, 910)

    # A free fractional background still caps below root payoff.
    uniform_prices = query_prices([F(1, 6)] * 6, R)
    assert max(uniform_prices) == F(441, 2) < profits[0]
    # A two-slot deterministic background also verifies v_3 <= 252.
    static_prices = [payoff(t, (t, 0, 5)) for t in TOPICS]
    assert max(static_prices) == 252

    result = {
        "scope": "Specified stationary r-mass fractional root cap only; not free extra-one, aggregate safety, or half",
        "players": R,
        "unit_customers": len(CLIENTS),
        "weights_by_mask": WEIGHTS,
        "ordered_histories": histories,
        "comparisons_including_self": comparisons,
        "minimum_spe_slack": str(minimum_slack),
        "actual_profile": actual_profile,
        "actual_profits": [str(x) for x in profits],
        "welfare": str(welfare),
        "optimum": optimum,
        "stationary_pi": [str(x) for x in pi],
        "stationary_fractional_query_prices": [str(x) for x in prices],
        "query_2_minus_root": str(prices[2] - profits[0]),
        "uniform_fractional_cap": str(max(uniform_prices)),
        "pure_two_slot_cap": str(max(static_prices)),
    }
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional new report; existing files are never overwritten")
    args = parser.parse_args()
    if args.output is not None:
        with args.output.open("x") as report:
            report.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: result[key] for key in (
        "unit_customers", "ordered_histories", "comparisons_including_self",
        "actual_profits", "welfare", "optimum", "query_2_minus_root",
        "uniform_fractional_cap", "pure_two_slot_cap")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
