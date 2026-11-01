"""Exact independent check of ROOT's named root-row-minus-K counterexample.

This constructs a complete count-state BI strategy, then explicitly checks
every ordered decision history. It does not use a myopic greedy shortcut.
No instance search or parameter scan is performed.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


M = 6
SIZES = (3, 3, 1, 1, 1, 1)
ACTIONS = tuple(range(len(SIZES)))
policy = {}


def add(q, a):
    out = list(q)
    out[a] += 1
    return tuple(out)


@lru_cache(None)
def complete(q):
    if sum(q) == M:
        return q
    # Action comparisons use the fully completed child, not immediate return.
    candidates = [(Fraction(SIZES[a], complete(add(q, a))[a]), a)
                  for a in ACTIONS]
    best = max(value for value, _ in candidates)
    a = min(a for value, a in candidates if value == best)
    policy[q] = a
    return complete(add(q, a))


zero = (0,) * len(SIZES)
actual_leaf = complete(zero)
count_state_comparisons = 0
for q, a in policy.items():
    actual = Fraction(SIZES[a], complete(q)[a])
    for b in ACTIONS:
        forced = Fraction(SIZES[b], complete(add(q, b))[b])
        assert actual >= forced, (q, a, b, actual, forced)
        count_state_comparisons += 1

ordered_histories = 0
ordered_comparisons = 0
for depth in range(M):
    for h in product(ACTIONS, repeat=depth):
        q = tuple(h.count(a) for a in ACTIONS)
        a = policy[q]
        actual = Fraction(SIZES[a], complete(q)[a])
        for b in ACTIONS:
            forced = Fraction(SIZES[b], complete(add(q, b))[b])
            assert actual >= forced, (h, a, b, actual, forced)
            ordered_comparisons += 1
        ordered_histories += 1

actual_path = []
q = zero
while sum(q) < M:
    a = policy[q]
    actual_path.append(a)
    q = add(q, a)

root_queries = [Fraction(SIZES[a], complete(add(zero, a))[a])
                for a in ACTIONS]
row = sum(root_queries)
welfare = sum(size for size, count in zip(SIZES, actual_leaf) if count)
optimum = sum(SIZES)
largest = max(SIZES)
assert actual_leaf == (3, 3, 0, 0, 0, 0)
assert welfare == 6 and optimum == 10 and largest == 3
assert root_queries == [Fraction(1)] * 6
assert row == 6 < optimum - largest == 7
assert row >= optimum - welfare == 4
assert 2 * welfare >= optimum
assert count_state_comparisons == 2772
assert ordered_histories == 9331 and ordered_comparisons == 55986

result = {
    "status": "PASS",
    "scope": "Named root-row-minus-largest-theme auxiliary counterexample only",
    "players": M,
    "disjoint_theme_sizes": SIZES,
    "strategy": "Full backward induction; smallest label among maximizing completed-child payoffs",
    "actual_path": actual_path,
    "actual_counts": actual_leaf,
    "actual_welfare": welfare,
    "optimum": optimum,
    "largest_theme": largest,
    "root_true_query_payoffs": [str(x) for x in root_queries],
    "root_true_query_completed_counts": [complete(add(zero, a)) for a in ACTIONS],
    "query_row_sum": str(row),
    "helper_rhs_opt_minus_largest": optimum - largest,
    "original_net_row_rhs_opt_minus_welfare": optimum - welfare,
    "complete_count_decision_states": len(policy),
    "count_state_IC_comparisons_including_self": count_state_comparisons,
    "ordered_decision_histories": ordered_histories,
    "ordered_IC_comparisons_including_self": ordered_comparisons,
    "target_half_holds": True,
    "actual_net_row_holds": True,
}

if __name__ == "__main__":
    target = Path(__file__).with_name("root_size_helper_independent_audit.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
