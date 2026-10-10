"""Order-insensitive root tax is false even for SPE-attainable PNE counts.

The companion appendix gives the arbitrary-n proof. This independent Fraction
audit checks one complete ordered strategy and finite family formula cases;
it does not refute correctly ordered SPE root tax or prove half coverage.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json


def audit(n, full_tree=False):
    hub, big, topics = n - 1, n, n + 1
    customers = [((leaf,), 2 * (n - 2)) for leaf in range(n - 1)]
    customers += [((leaf, hub), 2) for leaf in range(n - 1)]
    customers += [((big,), (n - 1) * (2 * n - 3))]
    actions = {}

    def counts(history):
        return tuple(history.count(a) for a in range(topics))

    @lru_cache(None)
    def payoff(q, action):
        return sum((Fraction(weight, sum(q[a] for a in likes))
                    for likes, weight in customers if action in likes), Fraction(0))

    def welfare(q):
        return sum(weight for likes, weight in customers if any(q[a] for a in likes))

    def tax(q):
        return sum((Fraction(weight * sum(q[a] for a in likes),
                             1 + sum(q[a] for a in likes))
                    for likes, weight in customers), Fraction(0))

    def build(history):
        if len(history) == n:
            return counts(history)
        branches = [build(history + (a,)) for a in range(topics)]
        if hub in history:
            action = big
        elif all(a == big for a in history):
            action = hub
        else:
            action = max(range(topics), key=lambda a: (payoff(branches[a], a), -a))
        actual = payoff(branches[action], action)
        assert all(actual >= payoff(q, a) for a, q in enumerate(branches))
        actions[history] = action
        return branches[action]

    q = counts((hub,) + (big,) * (n - 1))
    comparisons = 0
    if full_tree:
        assert build(()) == q

        def continuation(history):
            while len(history) < n:
                history += (actions[history],)
            return counts(history)

        # Recompute every true deviation from the saved complete strategy.
        for history, action in actions.items():
            actual = payoff(continuation(history), action)
            for alternative in range(topics):
                assert actual >= payoff(continuation(history + (alternative,)), alternative)
                comparisons += 1

    # Static PNE and both ordered tax calculations are separate checks.
    for action in range(topics):
        if not q[action]:
            continue
        for alternative in range(topics):
            changed = tuple(q[a] - (a == action) + (a == alternative) for a in range(topics))
            assert payoff(q, action) >= payoff(changed, alternative)
    optimum = max(welfare(tuple(int(a in support) for a in range(topics)))
                  for support in combinations(range(topics), n))
    assert welfare(q) == (n - 1) * (2 * n - 1)
    assert optimum == (n - 1) * (4 * n - 5)
    reordered_gap = optimum - welfare(q) - tax(counts((big,) * (n - 1)))
    SPE_slack = welfare(q) + tax(counts((hub,) + (big,) * (n - 2))) - optimum
    assert reordered_gap == Fraction((n - 1) * (n - 3), n) > 0
    assert SPE_slack == 1
    return {"n": n, "nodes": len(actions), "true_action_comparisons": comparisons,
            "reordered_tax_violation": str(reordered_gap), "ordered_SPE_tax_slack": str(SPE_slack)}


if __name__ == "__main__":
    complete = audit(4, full_tree=True)
    for players in range(4, 51):
        audit(players)
    print(json.dumps({"complete_strategy": complete, "family_formula_cases": 47,
                      "scope": "order-insensitive tax boundary only"}, indent=2))
