"""Independent definition-level audit of the population-monotonicity witnesses.

No import from the author's checker or the repository CAG solver.  Exact
backward induction keeps sets of possible continuations and constructs one
full ordered-history policy for each requested terminal count.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json


def audit(weights, players, target=None):
    def utility(counts, action):
        return sum((Fraction(weight, sum(counts[j] for j in range(4)
                                        if mask >> j & 1))
                    for mask, weight in weights.items() if mask >> action & 1),
                   Fraction())

    def welfare(counts):
        return sum(weight for mask, weight in weights.items()
                   if any(counts[j] and mask >> j & 1 for j in range(4)))

    def child(counts, action):
        result = list(counts)
        result[action] += 1
        return tuple(result)

    @lru_cache(None)
    def outcomes(counts):
        if sum(counts) == players:
            return frozenset([counts])
        branches = [outcomes(child(counts, a)) for a in range(4)]
        threshold = max(min(utility(q, a) for q in branches[a])
                        for a in range(4))
        return frozenset(q for a in range(4) for q in branches[a]
                         if utility(q, a) >= threshold)

    policy = {}

    def complete(history, desired):
        if len(history) == players:
            assert tuple(history.count(a) for a in range(4)) == desired
            return
        counts = tuple(history.count(a) for a in range(4))
        branches = [outcomes(child(counts, a)) for a in range(4)]
        minima = [min(utility(q, a) for q in branches[a]) for a in range(4)]
        choices = [a for a in range(4) if desired in branches[a]
                   and utility(desired, a) >= max(minima)]
        action = choices[0]
        policy[history] = action
        for a in range(4):
            endpoint = (desired if a == action else
                        min(branches[a], key=lambda q: (utility(q, a), q)))
            complete(history + (a,), endpoint)

    initial = (0, 0, 0, 0)
    feasible = outcomes(initial)
    if target is None:
        target = min(feasible, key=lambda q: (welfare(q), q))
    assert target in feasible
    complete((), target)

    def rollout(history):
        while len(history) < players:
            history += (policy[history],)
        return history

    comparisons = 0
    strict = True
    min_gap = None
    for depth in range(players):
        for history in product(range(4), repeat=depth):
            baseline = rollout(history)
            counts = tuple(baseline.count(a) for a in range(4))
            current = utility(counts, policy[history])
            for alternative in range(4):
                terminal = rollout(history + (alternative,))
                alt_counts = tuple(terminal.count(a) for a in range(4))
                gap = current - utility(alt_counts, alternative)
                assert gap >= 0, (history, alternative, gap)
                comparisons += 1
                if alternative != policy[history]:
                    strict &= gap > 0
                    min_gap = gap if min_gap is None else min(min_gap, gap)
    opt = max(welfare(tuple(path.count(a) for a in range(4)))
              for path in combinations_with_replacement(range(4), players))
    return dict(players=players, total_customers=sum(weights.values()),
                all_terminal_counts=[list(q) for q in sorted(feasible)],
                minimum_welfare=min(map(welfare, feasible)), optimum=opt,
                audited_path=list(rollout(())), nodes=len(policy),
                comparisons_including_self=comparisons,
                all_comparisons_strict=strict, minimum_gap=str(min_gap))


def main():
    small = {3: 3, 4: 1, 6: 2, 9: 1, 11: 3, 12: 3}
    strict = {3: 9, 4: 1, 6: 7, 9: 2, 11: 11, 12: 10}
    results = {"small": [audit(small, m) for m in (1, 2, 3, 4)],
               "strict": [audit(strict, m) for m in (1, 2, 3, 4)]}
    assert [r["minimum_welfare"] for r in results["small"]] == [8, 13, 12, 13]
    assert [r["minimum_welfare"] for r in results["strict"]] == [27, 40, 39, 39]
    assert all(r["all_comparisons_strict"] for r in results["strict"])
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
