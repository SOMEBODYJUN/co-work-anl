"""Independent exact audit: no imports from model, BI solver, or SPE verifier."""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import json


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, width - 1):
                yield (first,) + tail


def new_family(r):
    m = r + 1
    # Each tuple is one unit customer's entire set of accepted topic labels.
    clients = [(0,), (0,)] + [(1,)] * r
    clients += [(a,) for a in range(2, r + 1)]
    q = r + 1

    def payoff(path, player):
        action = path[player]
        return sum((Q(1, sum(a in likes for a in path))
                    for likes in clients if action in likes), Q(0))

    policy = {}
    comparison_count = 0

    @lru_cache(None)
    def continuation(h):
        nonlocal comparison_count
        if len(h) == m:
            return h
        terminals = [continuation(h + (a,)) for a in range(q)]
        values = [payoff(z, len(h)) for z in terminals]
        if 0 in h:
            chosen = 1
        elif all(a == 1 for a in h):
            chosen = 0
        else:
            chosen = max(range(q), key=lambda a: values[a])
        assert values[chosen] == max(values), (r, h, values, chosen)
        comparison_count += q
        policy[h] = chosen
        return terminals[chosen]

    actual = continuation(())
    assert actual == (0,) + (1,) * r
    assert [payoff(actual, j) for j in range(m)] == [Q(2)] + [Q(1)] * r

    # Recheck every history by executing the separately stored complete policy.
    def execute(h):
        while len(h) < m:
            h += (policy[h],)
        return h

    independently_replayed = 0
    for depth in range(m):
        for h in product(range(q), repeat=depth):
            base = payoff(execute(h), depth)
            for a in range(q):
                assert base >= payoff(execute(h + (a,)), depth)
                independently_replayed += 1

    best = Q(0)
    checked = 0
    for counts in compositions(r, q):
        value = Q(0)
        for likes in clients:
            c = sum(counts[a] for a in likes)
            if c:
                value += Q(c, int(0 in likes) + c)
        best = max(best, value)
        checked += 1
    assert best == 2 * r - 1
    return dict(r=r, unit_customers=len(clients), decision_histories=len(policy),
                action_comparisons=comparison_count, replay_comparisons=independently_replayed,
                tail_count_vectors=checked, Ftail=str(best))


def overlap_tail(n):
    """Rebuild old overlap input directly; exhaust all tail multisets."""
    x = n - 2
    clients = []
    for j in range(n - 1):
        leaf = j + 2
        clients.extend([(leaf,)] * x)
        clients.append((0, leaf))
        clients.extend([(1, leaf)] * x)
    leaf = n + 1
    clients.extend([(leaf,)] * x)
    clients.extend([(1, leaf)] * x)
    clients.extend([(0, 1, leaf)] * (n - 1))
    best = Q(0)
    checked = 0
    for counts in compositions(n - 1, n + 2):
        value = Q(0)
        for likes in clients:
            c = sum(counts[a] for a in likes)
            if c:
                value += Q(c, int(0 in likes) + c)
        best = max(best, value)
        checked += 1
    claimed = Q(2 * (n - 1) * (n - 2)) + Q(7 * n - 13, 6)
    assert best == claimed
    optimum = 2 * n * n - 2 * n - 2
    assert Q(optimum) - best == Q(17 * n - 23, 6)
    return dict(n=n, tail_count_vectors=checked, Ftail=str(best))


def main():
    rows = [new_family(r) for r in range(1, 6)]
    overlap = [overlap_tail(n) for n in range(4, 9)]
    n = 64
    h = min(Q(j) + Q(n, j) for j in range(1, n + 1))
    assert h == 16
    lower0 = Q(-1, 2)
    lower1 = (2 - h) / n
    upper = (Q(23 - 5 * n, 6) - Q(2, n)) / (n - 1)
    gap = lower0 + lower1 - upper
    assert (lower1, upper, gap) == (Q(-7, 32), Q(-1585, 2016), Q(17, 252))
    print(json.dumps(dict(
        scope="Independent finite audit; arbitrary-r proof is analytic, not extrapolated",
        dependencies="Python standard library only; no normative model/solver/verifier imports",
        new_family=rows, overlap_profit_reconstruction=overlap,
        total_decision_histories=sum(z['decision_histories'] for z in rows),
        common_r=n - 1, f10_lower=str(lower0), f1r_lower=str(lower1),
        joint_upper=str(upper), contradiction_gap=str(gap)), indent=2))


if __name__ == '__main__':
    main()
