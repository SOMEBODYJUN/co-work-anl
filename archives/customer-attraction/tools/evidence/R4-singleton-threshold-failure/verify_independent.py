"""Read-only exact replay of one frozen report; no canonical-package imports.

Expand customer multiplicities into 36 unit customers and recurse on every
ordered history, rather than sharing the canonical solver's count cache.
This is a finite certificate replay, not a search over arbitrary catalogues.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "maximum_singleton_threshold_failure.json"
raw = SOURCE.read_bytes()
assert len(raw) == 4156
assert sha256(raw).hexdigest() == "cf45d02bce087cb8e17793e89bd9e2c6419ecafc0fb5da7d9e3b2e29fb15a660"
report = json.loads(raw)
instance = report["instance"]
assert instance["topics"] == ["X0", "X1", "X2", "Y0", "Y1", "Y2"]
assert instance["players"] == 3
expected_types = Counter({(x, y): 1 for x in range(3) for y in range(3, 6)})
expected_types.update({i + j: 3 for i in combinations(range(3), 2)
                       for j in combinations(range(3, 6), 2)})
actual_types = Counter({tuple(t["topics"]): t["multiplicity"]
                        for t in instance["customers"]})
assert len(instance["customers"]) == 18
assert actual_types == expected_types
customers = tuple(frozenset(t["topics"])
                  for t in instance["customers"]
                  for _ in range(t["multiplicity"]))
assert len(customers) == 36
actions = tuple(range(6))


def counts(history):
    return tuple(history.count(a) for a in actions)


@lru_cache(None)
def utilities(terminal):
    loads = tuple(sum(a in c for a in terminal) for c in customers)
    return tuple(sum((Fraction(1, load) for c, load in zip(customers, loads)
                      if a in c and load), Fraction()) if a in terminal else Fraction()
                 for a in actions)


def welfare(terminal):
    return sum(any(a in c for a in terminal) for c in customers)


thresholds = {}
@lru_cache(None)
def ordered_outcomes(history):
    if len(history) == 3:
        return frozenset({history})
    children = {a: ordered_outcomes(history + (a,)) for a in actions}
    floor = max(min(utilities(z)[a] for z in children[a]) for a in actions)
    thresholds[history] = floor
    result = frozenset(z for a in actions for z in children[a]
                       if utilities(z)[a] >= floor)
    assert result
    return result


root = ordered_outcomes(())
after = ordered_outcomes((0,))
root_counts = sorted({counts(z) for z in root})
after_counts = sorted({counts(z) for z in after})
assert root_counts == [tuple(z) for z in report["before_outcomes"]]
assert after_counts == [tuple(z) for z in report["after_outcomes"]]
assert set(root_counts) == {counts(z) for z in combinations(actions, 3)}
assert set(after_counts) == {counts(z) for z in [(0, 1, 2), (0, 3, 4), (0, 3, 5), (0, 4, 5)]}
assert report["background"] == [0] * 6
assert report["maximum_singleton_topic"] == 0
singletons = [sum(a in c for c in customers) for a in actions]
assert list(map(str, singletons)) == report["singleton_values"] == ["21"] * 6
assert str(thresholds[()]) == report["before_threshold"] == "10"
assert str(thresholds[(0,)]) == report["after_threshold"] == "12"
assert all(thresholds[(a,)] == 12 for a in actions)
assert report["source"] == "examples/customer_attraction/aggregate_theta_failure.json"
assert report["candidate_status"] == "FALSE"
assert len(root) == 48 and len(root_counts) == 20
assert len(after) == 8 and len(after_counts) == 4
assert len(thresholds) == 43


def group(a):
    return range(3) if a < 3 else range(3, 6)


def strategy(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    return min(a for a in group(history[1]) if a not in history)


def complete(history):
    while len(history) < 3:
        history = history + (strategy(history),)
    return history


node_rows = []
for length in range(3):
    for history in product(actions, repeat=length):
        prescribed = strategy(history)
        terminal = complete(history)
        payoff = utilities(terminal)[prescribed]
        alternatives = {a: utilities(complete(history + (a,)))[a] for a in actions}
        assert all(payoff >= value for value in alternatives.values())
        node_rows.append({"history": history, "action": prescribed,
                          "payoff": str(payoff),
                          "all_action_payoffs": [str(alternatives[a]) for a in actions]})
path = complete(())
assert path == (0, 3, 4)
assert [utilities(path)[a] for a in path] == [10, 12, 12]
assert welfare(path) == 34
assert max(welfare(z) for z in product(actions, repeat=3)) == 36
assert {welfare(z) for z in root} == {34, 36}

action_rows = []
for a in actions:
    child = ordered_outcomes((0, a))
    action_rows.append({"second_action": a,
                       "last_player_threshold": str(thresholds[(0, a)]),
                       "second_player_payoffs_over_last_best_replies": sorted({str(utilities(z)[a]) for z in child}),
                       "minimum": str(min(utilities(z)[a] for z in child))})

output = {
    "check_kind": "independent-expanded-unit-customer-ordered-history-exact-replay",
    "canonical_package_imported": False,
    "primary_source_sha256": sha256(raw).hexdigest(),
    "primary_bytes": len(raw),
    "customer_type_count": len(actual_types), "unit_customer_count": len(customers),
    "ordered_terminal_histories_examined": 216,
    "ordered_decision_histories_examined": len(thresholds),
    "singleton_values": list(map(str, singletons)),
    "before_threshold": str(thresholds[()]), "after_threshold": str(thresholds[(0,)]),
    "first_action_minimum_payoffs": [str(min(utilities(z)[a] for z in ordered_outcomes((a,)))) for a in actions],
    "all_one_action_prefix_thresholds": [str(thresholds[(a,)]) for a in actions],
    "second_action_rows_after_X0": action_rows,
    "before_ordered_spe_paths": len(root), "after_ordered_spe_paths": len(after),
    "before_count_outcomes": root_counts, "after_count_outcomes": after_counts,
    "root_spe_welfare_set": sorted({welfare(z) for z in root}),
    "optimum_three_topic_coverage": 36,
    "formula_strategy": {"path": path, "payoffs": ["10", "12", "12"],
                         "welfare": 34, "nodes": 43,
                         "all_comparisons_including_self": 258,
                         "changed_action_comparisons": 215,
                         "all_nodes": node_rows},
    "all_frozen_semantic_fields_match": True,
    "all_checks_passed": True,
    "scope": "One 36-unit-customer three-player instance; no general half proof or counterexample."
}
print(json.dumps(output, ensure_ascii=False, indent=2))
