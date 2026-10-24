"""Two fixed-strategy cone attacks on 2m*u_root >= comparison coverage.

Finite negative search only; successful LP values do not prove a general bound.
"""
import itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog


def payoff(mask, outcome, index):
    if not (mask >> outcome[index]) & 1:
        return 0.0
    return 1.0 / sum(bool((mask >> action) & 1) for action in outcome)


def compare_cone(k, m, terminal, comparisons):
    masks = list(range(1, 1 << k))
    rows = []
    for i in range(m):
        for history in itertools.product(range(k), repeat=i):
            prescribed = terminal(history)
            for action in range(k):
                deviated = terminal(history + (action,))
                rows.append([payoff(mask, prescribed, i) - payoff(mask, deviated, i)
                             for mask in masks])
    root = terminal(())
    u_root = np.array([payoff(mask, root, 0) for mask in masks])
    best = None
    for topics in comparisons:
        cover_mask = sum(1 << action for action in topics)
        coverage = np.array([bool(mask & cover_mask) for mask in masks], dtype=float)
        result = linprog(-coverage, A_ub=-np.array(rows), b_ub=np.zeros(len(rows)),
                         A_eq=[u_root], b_eq=[1], bounds=(0, None), method="highs")
        if result.success and (best is None or result.fun < best.fun):
            best = result
            best_topics = topics
    print({"m": m, "path": root, "comparison": best_topics,
           "max_comparison_over_root": -best.fun, "direct_threshold": 2 * m})


def root_tax_terminal(history):
    original = {1: 12, 2: 8, 4: 4, 8: 8, 17: 6, 33: 6, 20: 3,
                36: 3, 49: 6, 50: 2, 52: 1, 56: 2}
    outcome = list(history)
    while len(outcome) < 4:
        if len(outcome) < 3:
            outcome.append(0)
        else:
            values = [sum(Fraction(weight, sum(bool((mask >> action) & 1)
                                                  for action in outcome + [a]))
                          for mask, weight in original.items() if (mask >> a) & 1)
                      for a in range(6)]
            outcome.append(max(range(6), key=lambda a: (values[a], a)))
    return tuple(outcome)


def group_terminal(history):
    outcome = list(history)
    while len(outcome) < 3:
        if not outcome:
            outcome.append(0)
        elif len(outcome) == 1:
            outcome.append(3 if outcome[0] < 3 else 0)
        else:
            first = (outcome[1] // 3) * 3
            outcome.append(min(a for a in range(first, first + 3) if a not in outcome))
    return tuple(outcome)


if __name__ == "__main__":
    compare_cone(6, 4, root_tax_terminal, [(0, 1, 2, 3)])
    compare_cone(6, 3, group_terminal, itertools.combinations(range(6), 3))
