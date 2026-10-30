"""Definition-level replacement for a missing frozen discovery dependency.

This is new cleanup code, not the absent symmetric_ne_bridge_attack.py.
Only the names used by iid_conditional_dual_generator.py are supplied.
The policy and coefficients are reconstructed from iid_benchmark_source.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

import numpy as np
from scipy.optimize import linprog


def policy36(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def setup(n, m, policy):
    masks = list(range(1, 1 << m))
    histories = [h for k in range(n) for h in product(range(m), repeat=k)]

    def finish(history):
        history = tuple(history)
        while len(history) < n:
            history += (policy(history),)
        return history

    def coefficient(mask, action, terminal):
        if not (mask >> action & 1):
            return F(0)
        return F(1, sum(mask >> a & 1 for a in terminal))

    gamma = []
    for history in histories:
        terminal = finish(history)
        for action in range(m):
            deviated = finish(history + (action,))
            gamma.append(tuple(
                coefficient(mask, policy(history), terminal)
                - coefficient(mask, action, deviated)
                for mask in masks
            ))
    root = finish(())
    coverage = tuple(F(any(mask >> a & 1 for a in root)) for mask in masks)
    return masks, histories, finish, coefficient, gamma, coverage
