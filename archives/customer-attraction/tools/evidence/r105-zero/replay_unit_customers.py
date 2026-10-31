"""Fresh exact replay of one fixed 18-unit-customer deletion witness.

Written after reading both historical audits; this is not a blind audit.
No repository solver, search, simplifier, or historical audit is imported.
Every first-action/complete last-action table is checked, including rejected
last-player tables: 4 * 4**4 = 1024 complete strategies per background.
"""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "zero_regret_repair_witness.json").read_text())
TOPICS = DATA["topics"]
CUSTOMERS = tuple(
    frozenset(group["topics"])
    for group in DATA["customers"]
    for _ in range(group["multiplicity"])
)
CHOICES = tuple(range(len(TOPICS)))
assert len(CUSTOMERS) == 18


def payoff(leaf, actor):
    chosen = leaf[actor]
    return sum(
        (Fraction(1, sum(topic in client for topic in leaf))
         for client in CUSTOMERS if chosen in client),
        Fraction(0),
    )


def welfare(leaf):
    return sum(any(topic in client for topic in leaf) for client in CUSTOMERS)


def enumerate_game(prefix):
    """Return every complete pure SPE of the two remaining players."""
    first_index = len(prefix)
    last_index = first_index + 1
    utility = {
        (a, b): (
            payoff(prefix + (a, b), first_index),
            payoff(prefix + (a, b), last_index),
        )
        for a in CHOICES for b in CHOICES
    }
    last_table = [[utility[a, b][1] for b in CHOICES] for a in CHOICES]
    last_best = [max(row) for row in last_table]
    strategies = []
    checked = 0
    for first in CHOICES:
        for last in product(CHOICES, repeat=len(CHOICES)):
            checked += 1
            if any(utility[a, last[a]][1] != last_best[a] for a in CHOICES):
                continue
            first_values = tuple(utility[a, last[a]][0] for a in CHOICES)
            if first_values[first] != max(first_values):
                continue
            strategies.append({
                "first": first,
                "last_policy": list(last),
                "first_payoffs": list(map(str, first_values)),
                "tail_leaf": [first, last[first]],
                "tail_coverage": welfare((first, last[first])),
                "complete_leaf_coverage": welfare(prefix + (first, last[first])),
            })
    assert checked == 1024
    return {
        "prefix": list(prefix),
        "complete_strategies_checked": checked,
        "last_payoff_table": [list(map(str, row)) for row in last_table],
        "last_best_reply_sets": [
            [b for b in CHOICES if row[b] == max(row)] for row in last_table
        ],
        "all_complete_pure_SPEs": strategies,
    }


old = enumerate_game((0,))
deleted = enumerate_game(())
assert [(s["first"], s["last_policy"]) for s in old["all_complete_pure_SPEs"]] == [
    (2, [2, 2, 1, 2])
]
assert [(s["first"], s["last_policy"]) for s in deleted["all_complete_pure_SPEs"]] == [
    (3, [2, 3, 1, 1])
]

retained_policy = tuple(DATA["old_tail_strategy"]["last_after_first"])
first = DATA["old_tail_strategy"]["first_action"]
retained_leaf = (first, retained_policy[first])
retained_first_values = tuple(payoff((a, retained_policy[a]), 0) for a in CHOICES)
actual_last_values = tuple(payoff((first, b), 1) for b in CHOICES)
regrets = (
    max(retained_first_values) - retained_first_values[first],
    max(actual_last_values) - actual_last_values[retained_policy[first]],
)
assert regrets == (0, 0)
assert welfare(retained_leaf) == 17
assert deleted["all_complete_pure_SPEs"][0]["tail_coverage"] == 16

# Each first-action subgame of the empty-root three-player game is solved
# completely. Each has a unique tail terminal, although an off-path tie may
# permit several complete tail strategies. Thus continuation selection does
# not change the root payoff in this fixed witness.
root_children = []
for root in CHOICES:
    game = enumerate_game((root,))
    outcomes = sorted({tuple(s["tail_leaf"]) for s in game["all_complete_pure_SPEs"]})
    assert len(outcomes) == 1
    tail = outcomes[0]
    value = payoff((root,) + tuple(tail), 0)
    root_children.append({
        "root": root,
        "complete_tail_SPE_count": len(game["all_complete_pure_SPEs"]),
        "unique_tail_terminal": list(tail),
        "root_payoff": str(value),
    })
root_values = [Fraction(child["root_payoff"]) for child in root_children]
assert root_values == [Fraction(5), Fraction(13, 2), Fraction(11, 2), Fraction(6)]
assert root_values.index(max(root_values)) == 1

report = {
    "scope": "One fixed legal-background deletion witness; no random scan and no half theorem.",
    "independence": "Fresh implementation after reading historical material; not blind; no solver import.",
    "unit_customer_count": len(CUSTOMERS),
    "topic_labels": TOPICS,
    "old_game": old,
    "deleted_game": deleted,
    "retained_first_payoffs_after_deletion": list(map(str, retained_first_values)),
    "retained_actual_last_payoffs_after_deletion": list(map(str, actual_last_values)),
    "retained_actual_node_regrets": list(map(str, regrets)),
    "retained_deleted_coverage": welfare(retained_leaf),
    "deleted_OPT_2": max(welfare((a, b)) for a in CHOICES for b in CHOICES),
    "three_player_root_children": root_children,
    "three_player_unique_root": 1,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
