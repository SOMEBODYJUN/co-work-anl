"""Exact check for the four-player, fixed-policy distinct-prefix average cone."""

import argparse
import hashlib
import json
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from pathlib import Path


TOPICS = tuple(range(5))
COMPARISON = frozenset((1, 2, 3, 4))
PLAYERS = 4
MASKS = range(1, 1 << len(TOPICS))
ACTIONS = (
    "2",
    "00202",
    "0000020022022200002020022",
    "000020002002200220000200002022222000000222202020020200220202022202"
    "22220220222202020020222020200020200022222022000220202222220",
)
CUSTOMERS = {2: 19, 5: 96, 9: 38, 17: 45}
DUAL = {(2,): Fraction(9, 4), (2, 1): Fraction(1), (2, 3): Fraction(1, 2)}
BOUND = Fraction(33, 16)
ARCHIVE = Path("archives/customer-attraction/tools/evidence")
ORIGINAL_AVERAGE = ARCHIVE / "average-and-last-payoff-resumed-boss2/original/average_probe.json"
OLD_STRATEGIES = (
    ARCHIVE
    / "strategy-cones/original/evidence/runs/2026-10-09"
    / "customer_attraction_strategy_lp_m4p5_certified.json"
)
EXPECTED_REMAINDERS = (
    "0", "0", "0", "0", "0", "17/48", "17/48", "1/4",
    "0", "7/8", "19/24", "23/48", "19/48", "35/48", "11/16", "1/2",
    "0", "5/4", "3/4", "5/8", "7/16", "15/16", "3/4", "13/8",
    "7/8", "2", "17/12", "13/12", "13/16", "31/24", "17/16",
)


def includes(mask, topic):
    return bool(mask & (1 << topic))


def payoff_column(mask, topic, terminal):
    if not includes(mask, topic):
        return Fraction(0)
    load = sum(includes(mask, chosen) for chosen in terminal)
    return Fraction(1, load)


def archive_bindings(repo, actions):
    original_path = repo / ORIGINAL_AVERAGE
    old_path = repo / OLD_STRATEGIES
    original_bytes = original_path.read_bytes()
    old_bytes = old_path.read_bytes()
    original = json.loads(original_bytes)["failures"]["permutation_prefix"]
    old = json.loads(old_bytes)["cone_proofs"]
    assert len(old) == 70 and original["cone_index"] == 9
    assert frozenset(original["J"]) == COMPARISON
    assert original["actions"] == old[9]["actions"]
    assert len(original["actions"]) == len(actions)
    assert {tuple(row["history"]): row["action"] for row in original["actions"]} == actions
    return {
        str(ORIGINAL_AVERAGE): hashlib.sha256(original_bytes).hexdigest(),
        str(OLD_STRATEGIES): hashlib.sha256(old_bytes).hexdigest(),
    }


def check(repo):
    assert [len(line) for line in ACTIONS] == [1, 5, 25, 125]
    actions = {
        history: int(action)
        for depth, line in enumerate(ACTIONS)
        for history, action in zip(product(TOPICS, repeat=depth), line, strict=True)
    }
    assert len(actions) == 156 and set(actions.values()) == {0, 2}

    @cache
    def terminal(history):
        if len(history) == PLAYERS:
            return history
        return terminal(history + (actions[history],))

    def slack(history, alternative, mask):
        return (
            payoff_column(mask, actions[history], terminal(history))
            - payoff_column(mask, alternative, terminal(history + (alternative,)))
        )

    def average_row(history, alternatives):
        return tuple(
            sum(slack(history, topic, mask) for topic in alternatives) / len(alternatives)
            for mask in MASKS
        )

    def on_witness(coefficients):
        return sum(coefficients[mask - 1] * count for mask, count in CUSTOMERS.items())

    retained = {
        h: average_row(h, COMPARISON.difference(h))
        for h in actions
        if len(set(h)) == len(h) and COMPARISON.issuperset(h)
    }
    assert len(retained) == 41 and min(map(on_witness, retained.values())) == 0
    assert all(on_witness(retained[h]) == 0 for h in DUAL)

    root_terminal = terminal(())
    assert root_terminal == (2, 2, 2, 2)
    welfare = tuple(int(any(includes(mask, a) for a in root_terminal)) for mask in MASKS)
    comparison = tuple(int(any(includes(mask, a) for a in COMPARISON)) for mask in MASKS)
    actual_welfare = on_witness(welfare)
    comparison_welfare = on_witness(comparison)
    optimum = max(
        sum(count for mask, count in CUSTOMERS.items() if any(includes(mask, a) for a in group))
        for group in combinations(TOPICS, PLAYERS)
    )
    assert (actual_welfare, comparison_welfare, optimum) == (96, 198, 198)
    assert sum(CUSTOMERS.values()) == optimum
    assert Fraction(comparison_welfare, actual_welfare) == BOUND
    assert BOUND * actual_welfare == comparison_welfare

    assert all(weight > 0 for weight in DUAL.values())
    remainders = tuple(
        BOUND * welfare[k] - comparison[k]
        - sum(weight * retained[history][k] for history, weight in DUAL.items())
        for k in range(len(MASKS))
    )
    assert tuple(map(str, remainders)) == EXPECTED_REMAINDERS
    assert min(remainders) == 0
    assert all(remainders[mask - 1] == 0 for mask in CUSTOMERS)

    individual = {
        (h, a): on_witness(tuple(slack(h, a, mask) for mask in MASKS))
        for h in actions
        for a in TOPICS
    }
    assert len(individual) == 780 and sum(v < 0 for v in individual.values()) == 92
    assert individual[(), 0] / actual_welfare == Fraction(-83, 384)
    filtered_individual = {key: v for key, v in individual.items()
                           if key[0] in retained and key[1] in COMPARISON.difference(key[0])}
    assert len(filtered_individual) == 64 and sum(v < 0 for v in filtered_individual.values()) == 3

    all_history = {h: on_witness(average_row(h, COMPARISON)) / actual_welfare for h in actions}
    negative_all_history = {h: v for h, v in all_history.items() if v < 0}
    assert negative_all_history == {(2, 2): Fraction(-5, 256), (2, 2, 2): Fraction(-5, 64)}

    # Domain endpoints and the three exact terminal substitutions.
    assert (welfare[0], comparison[0], remainders[0]) == (0, 0, 0)
    assert (welfare[MASKS.stop - 2], comparison[MASKS.stop - 2]) == (1, 1)
    assert terminal((2, 4)) == (2, 4, 0, 0)
    assert terminal((2, 1, 3)) == (2, 1, 3, 0)
    assert terminal((2, 3, 4)) == (2, 3, 4, 2)
    return {
        "scope": "Only the specified policy, J, and 41 distinct-prefix averaged rows.",
        "archive_sha256": archive_bindings(repo, actions) if repo is not None else {},
        "histories": len(actions),
        "retained_average_rows": len(retained),
        "normalized_retained_average_slacks": [
            {"history": h, "slack": str(on_witness(row) / actual_welfare)}
            for h, row in retained.items()
        ],
        "witness_customers": CUSTOMERS,
        "W": actual_welfare,
        "O_J": comparison_welfare,
        "OPT": optimum,
        "bound": str(BOUND),
        "dual": [
            {"history": h, "weight": str(weight), "witness_slack": str(on_witness(retained[h])),
             "own_terminal": terminal(h),
             "deviation_terminals": {a: terminal(h + (a,)) for a in sorted(COMPARISON.difference(h))}}
            for h, weight in DUAL.items()
        ],
        "columns": [
            {"mask": mask, "w": welfare[mask - 1], "o": comparison[mask - 1],
             "dual_row_coefficients": [str(retained[h][mask - 1]) for h in DUAL],
             "remainder": str(remainders[mask - 1])}
            for mask in MASKS
        ],
        "true_rows": len(individual),
        "negative_true_rows": sum(v < 0 for v in individual.values()),
        "retained_individual_rows": len(filtered_individual),
        "negative_retained_individual_rows": [
            {"history": h, "alternative": a, "normalized_slack": str(v / actual_welfare)}
            for (h, a), v in filtered_individual.items() if v < 0
        ],
        "negative_full_history_averages": [
            {"history": h, "normalized_slack": str(v)} for h, v in negative_all_history.items()
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, help="Also bind the policy to the archived source bytes.")
    args = parser.parse_args()
    print(json.dumps(check(args.repo), ensure_ascii=False, indent=2))
