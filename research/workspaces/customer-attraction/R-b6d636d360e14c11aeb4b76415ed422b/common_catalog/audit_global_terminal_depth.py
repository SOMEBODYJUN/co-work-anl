"""Exact checks for the explicitly weakened system; not an SPE search."""
from fractions import Fraction as F
from itertools import product
from math import lcm
import json


def instance(m, k):
    K = lcm(*range(1, m + 1))
    sizes = [F(K)] * m + [F(K, m - j) for j in range(m - k)]
    actual = list(range(m, 2 * m - k)) + list(range(k))
    return K, sizes, actual


def action(h, m, k):
    if len(h) < m - k:
        return m + len(h)
    return next(a for a in range(m) if a not in h)


def continuation(h, m, k):
    h = tuple(h)
    while len(h) < m:
        h += (action(h, m, k),)
    return h


def payoff(terminal, i, sizes):
    return sizes[terminal[i]] / terminal.count(terminal[i])


def check_parameters(m, k):
    K, sizes, actual = instance(m, k)
    w = sum(sizes[a] for a in set(actual))
    hm = sum((F(1, r) for r in range(1, m + 1)), F())
    hk = sum((F(1, r) for r in range(1, k + 1)), F())
    assert w == K * (k + hm - hk)
    assert sum(sorted(sizes, reverse=True)[:m]) == m * K
    for j in range(m - k):
        u = payoff(tuple(actual), j, sizes)
        r = m - j
        bounds = [sizes[a] / (actual[:j].count(a) + r)
                  for a in range(len(sizes))]
        assert max(bounds) == u == F(K, r)
        dev = continuation(tuple(actual[:j]) + (0,), m, k)
        assert payoff(dev, j, sizes) == K > u
    return {"m": m, "k": k, "K": K, "W": str(w),
            "OPT": m * K, "OPT_over_W": str(m * K / w)}


def check_all_deep_histories(m, k):
    _, sizes, _ = instance(m, k)
    nodes = comparisons = 0
    for depth in range(m - k, m):
        for h in product(range(len(sizes)), repeat=depth):
            terminal = continuation(h, m, k)
            u = payoff(terminal, depth, sizes)
            assert u == sizes[0]
            for a in range(len(sizes)):
                dev = continuation(h + (a,), m, k)
                assert u >= payoff(dev, depth, sizes)
                comparisons += 1
            nodes += 1
    return {"m": m, "k": k, "ordered_deep_nodes": nodes,
            "true_deviation_comparisons": comparisons}


def check_three_atom_bounds(m):
    low = F(3 * (m - 2))
    high = F(m - 2) * (F(m) + F(3, 2)) / (m - 1)
    assert low > high
    assert low - high == F((m - 2) * (4 * m - 9), 2 * (m - 1))


def check_three_atom_original_rows(m):
    """Expand original S/Z/V, H and L separately for each one-client type."""
    cases = [
        (1, 0, [0] * (m - 2), F(2 - m),
         [-F(1, m - j) for j in range(m - 2)], [F()] * (m - 2)),
        (0, 0, [1] * (m - 2), F(m, m - 1),
         [F(1, m - 2)] * (m - 2), [-F(1, m - 1)] * (m - 2)),
        (0, 1, [0] * (m - 2), F(3, 2),
         [F()] * (m - 2), [F(1)] * (m - 2)),
    ]
    for a, b, early, expected_residual, expected_h, expected_l in cases:
        queries, replies = [1] + [0] * (m - 1), [0] * m
        p = sum(early)
        count = p + a + b
        ua = F(a, count) if a else F()
        ub = F(b, count) if b else F()
        s = sum((ua - F(t, p + 1 + r)
                 for t, r in zip(queries, replies)), F())
        z = sum((ub - F(r, p + 1 + a) for r in replies), F())
        v = sum((F(replies[i], p + 1 + queries[i])
                 - F(replies[j], p + 1 + queries[i])
                 for i in range(m) for j in range(m) if i != j), F())
        g = s + z / (2 * m) + v / m
        residual = 2 * int(count > 0) - int(any(queries)) - g
        h = [(F(e, count) if e else F())
             - (F(a, sum(early[:j]) + m - j) if a else F())
             for j, e in enumerate(early)]
        last = [ub - F(e, p + 1 + a) for e in early]
        assert residual == expected_residual
        assert h == expected_h
        assert last == expected_l


if __name__ == "__main__":
    for m in range(2, 61):
        for k in range(1, m):
            check_parameters(m, k)
    for m in range(3, 301):
        check_three_atom_bounds(m)
    for m in range(3, 61):
        check_three_atom_original_rows(m)
    report = {
        "scope": "weakened system only; no SPE counterexample",
        "parameter_pairs_checked": sum(range(1, 60)),
        "sample": check_parameters(8, 2),
        "appendix_original_rows_checked_m": [3, 60],
        "all_tree_terminal_history_checks": [
            check_all_deep_histories(4, 2),
            check_all_deep_histories(5, 2),
            check_all_deep_histories(5, 3),
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
