"""Exact-outcome-set backward induction for small customer-attraction catalogs.

The primary computation uses float for search; verify_result reconstructs every
chosen ordered history with Fraction arithmetic before making a mathematical claim.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement

import numpy as np


def terminal_data(weights, players=6):
    """weights[mask] is the count of customers liking exactly mask of topics."""
    n = (len(weights) - 1).bit_length()
    masks = np.array([i for i in range(1, 1 << n) if weights[i]], dtype=int)
    w = np.array([weights[i] for i in masks], dtype=float)
    incidence = ((masks[:, None] & (1 << np.arange(n))) > 0).astype(int)
    terminals = tuple(combinations_with_replacement(range(n), players))
    counts = np.zeros((len(terminals), n), dtype=int)
    for row, q in enumerate(terminals):
        for a in q:
            counts[row, a] += 1
    load = counts @ incidence.T
    cover = (load > 0) @ w
    shares = np.zeros_like(load, dtype=float)
    np.divide(w[None, :], load, out=shares, where=load > 0)
    profit = shares @ incidence
    return terminals, counts, profit.T, cover


def solve(weights, players=6, tolerance=1e-9, witness=False):
    """Enumerate *all* possible terminal count outcomes under ordered SPE.

    Histories with the same count have the same feasible outcome set, but their
    prescribed outcomes are independent choices. Child alternatives are therefore
    minimized separately at each action, including history-dependent tie choices.
    """
    n = (len(weights) - 1).bit_length()
    terminals, final_counts, u, welfare = terminal_data(weights, players)
    ids = {tuple(c): k for k, c in enumerate(final_counts)}
    zero = (0,) * n

    @lru_cache(None)
    def outcomes(c):
        depth = sum(c)
        if depth == players:
            return (ids[c],)
        children = []
        mins = []
        for a in range(n):
            nxt = list(c)
            nxt[a] += 1
            child = outcomes(tuple(nxt))
            children.append(child)
            mins.append(min(u[a, q] for q in child))
        feasible = set()
        for a in range(n):
            threshold = max(mins[:a] + mins[a + 1 :], default=-float("inf"))
            feasible.update(q for q in children[a] if u[a, q] + tolerance >= threshold)
        if not feasible:
            raise AssertionError((c, children, mins))
        return tuple(sorted(feasible))

    possible = outcomes(zero)
    optimum = max(welfare[i] for i in range(len(terminals)))
    minimum = min(welfare[q] for q in possible)
    record = {
        "ratio": minimum / optimum if optimum else 1.0,
        "min_welfare": minimum,
        "optimum": optimum,
        "root_outcomes": len(possible),
        "root_min_count": tuple(final_counts[min(possible, key=lambda q: welfare[q])]),
        "states": outcomes.cache_info().currsize,
    }
    if witness:
        record["strategy"] = reconstruct(weights, players, u, welfare, outcomes,
                                         ids, min(possible, key=lambda q: welfare[q]), tolerance)
    return record


def reconstruct(weights, players, u, welfare, outcomes, ids, root_id, tolerance):
    """Return action at every ordered history, selecting witnesses recursively."""
    n = (len(weights) - 1).bit_length()
    strategy = {}

    def fill(history, q):
        c = tuple(history.count(a) for a in range(n))
        if len(history) == players:
            assert ids[c] == q
            return
        child = []
        minima = []
        for a in range(n):
            nxt = list(c)
            nxt[a] += 1
            opt = outcomes(tuple(nxt))
            child.append(opt)
            minima.append(min(u[a, r] for r in opt))
        choices = []
        for a in range(n):
            if q in child[a] and u[a, q] + tolerance >= max(minima[:a] + minima[a + 1 :], default=-float("inf")):
                choices.append(a)
        if not choices:
            raise AssertionError((history, q))
        selected = choices[0]
        strategy[history] = selected
        for a in range(n):
            target = q if a == selected else min(child[a], key=lambda r: (u[a, r], r))
            fill(history + (a,), target)

    fill((), root_id)
    return strategy


def verify_result(weights, strategy, players=6):
    """Exact rational check at *every ordered history* and every topic."""
    n = (len(weights) - 1).bit_length()
    assert len(strategy) == sum(n**i for i in range(players))

    @lru_cache(None)
    def leaf(h):
        if len(h) == players:
            return h
        return leaf(h + (strategy[h],))

    @lru_cache(None)
    def payoff(h, a):
        counts = tuple(h.count(j) for j in range(n))
        q = [h.count(j) for j in range(n)]
        for j in range(n):
            q[j] += 0
        return sum((Fraction(weights[mask], sum(q[b] for b in range(n) if mask & (1 << b)))
                    for mask in range(1, 1 << n) if weights[mask] and mask & (1 << a)), Fraction())

    def u(a, full):
        q = [full.count(j) for j in range(n)]
        return sum((Fraction(weights[mask], sum(q[b] for b in range(n) if mask & (1 << b)))
                    for mask in range(1, 1 << n) if weights[mask] and mask & (1 << a)), Fraction())

    tight = 0
    worst_slack = None
    for h, chosen in strategy.items():
        current = u(chosen, leaf(h))
        for a in range(n):
            alt = u(a, leaf(h + (a,)))
            slack = current - alt
            assert slack >= 0, (h, a, slack)
            tight += slack == 0
            worst_slack = slack if worst_slack is None else min(slack, worst_slack)
    actual = leaf(())
    count = tuple(actual.count(a) for a in range(n))
    actual_welfare = sum(weights[mask] for mask in range(1, 1 << n)
                         if weights[mask] and any(count[a] and mask & (1 << a) for a in range(n)))
    opt = max(sum(weights[mask] for mask in range(1, 1 << n)
                  if weights[mask] and any(mask & (1 << a) for a in actions))
              for actions in combinations_with_replacement(range(n), players))
    return {"W": actual_welfare, "OPT": opt, "tight": tight,
            "comparisons": len(strategy) * n, "actual": actual, "worst_slack": worst_slack}
