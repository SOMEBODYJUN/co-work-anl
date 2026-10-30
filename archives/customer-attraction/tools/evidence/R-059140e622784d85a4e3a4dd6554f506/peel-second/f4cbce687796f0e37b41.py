#!/usr/bin/env python3
"""Exact standalone audit of PEEL; no equilibrium or discovery imports.

The random trials check an algebraic identity for arbitrary forced branches.
The 36-unit-customer replay checks the complete ordered strategy and then
reports the new decomposition of its already-known covariance quantities.
This script performs no search for new examples or restricted-class theorem.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json
import random


def payoff(theme, loads, customers):
    return sum((Q(1, loads[x]) for x in customers[theme]), Q(0))


def load(themes, customers, n):
    out = [0] * n
    for a in themes:
        for x in customers[a]:
            out[x] += 1
    return out


def u(h, a, last, customers):
    return sum((Q(1, h[x] + 1 + (x in customers[last]))
                for x in customers[a]), Q(0))


def phi(h, a, last, customers):
    return u(h, a, last, customers) + sum(
        (Q(1, h[x] + 1) for x in customers[last]), Q(0))


def decompose(customers, b, middle, last, p):
    """middle[A] is its actual tuple; last[A] is its actual final action."""
    k, n = len(customers), len(b)
    h = {a: [b[x] + v for x, v in enumerate(load(middle[a], customers, n))]
         for a in range(k)}
    d = f = c = ell = delta = tax = Q(0)
    pair_min = None
    for a in range(k):
        d += p[a] * u(h[a], a, last[a], customers)
        for t in range(k):
            w = p[a] * p[t]
            f += w * u(h[a], t, last[a], customers)
            c += w * sum((Q(1, h[a][x] + (x in customers[a])
                               + (x in customers[last[a]]) + 1)
                          for x in customers[t]), Q(0))
            slack = (u(h[a], last[a], a, customers)
                     - u(h[a], last[t], a, customers))
            pair_min = slack if pair_min is None else min(pair_min, slack)
            ell += w * slack
            delta += w * (phi(h[a], a, last[t], customers)
                          - phi(h[t], a, last[t], customers))
            tax += w * sum((Q(1, (h[a][x] + (x in customers[last[a]]) + 1)
                                  * (h[a][x] + (x in customers[last[a]]) + 2))
                            for x in customers[a] & customers[t]), Q(0))
    assert d - f == ell + delta
    assert f - c == tax
    assert d - c == ell + delta + tax
    return {"D": d, "F_deleted": f, "C_extra": c, "last_BR": ell,
            "middle_drift": delta, "collision_tax": tax,
            "last_pair_min": pair_min}


def random_identity_trials(count=1500, seed=59140):
    rng = random.Random(seed)
    for _ in range(count):
        n, k, r = rng.randrange(1, 8), rng.randrange(1, 6), rng.randrange(2, 7)
        customers = [set(x for x in range(n) if rng.randrange(2)) for _ in range(k)]
        b = [rng.randrange(5) for _ in range(n)]
        middle = {a: tuple(rng.randrange(k) for _ in range(r - 2)) for a in range(k)}
        last = {a: rng.randrange(k) for a in range(k)}
        weights = [rng.randrange(5) for _ in range(k)]
        if not sum(weights):
            weights[0] = 1
        p = [Q(w, sum(weights)) for w in weights]
        decompose(customers, b, middle, last, p)
    return {"identity_trials": count, "seed": seed, "arithmetic": "Fraction",
            "equilibrium_claim": False}


def thirty_six_unit_replay():
    # Nine pair-interest customers and 27 four-interest customers, all distinct.
    interest = [set((x, y)) for x in range(3) for y in range(3, 6)]
    for xs in combinations(range(3), 2):
        for ys in combinations(range(3, 6), 2):
            interest.extend([set(xs + ys) for _ in range(3)])
    customers = [set(x for x, inc in enumerate(interest) if a in inc) for a in range(6)]
    m, k, n = 3, 6, len(interest)

    def choice(history):
        if not history:
            return 0
        if len(history) == 1:
            return 3 if history[0] < 3 else 0
        group = range(3) if history[-1] < 3 else range(3, 6)
        return min(a for a in group if a not in history)

    def finish(history):
        history = tuple(history)
        while len(history) < m:
            history += (choice(history),)
        return history

    comparisons, minimum = 0, None
    for depth in range(m):
        for history in product(range(k), repeat=depth):
            true = finish(history)
            own = payoff(true[depth], load(true, customers, n), customers)
            for a in range(k):
                dev = finish(history + (a,))
                value = payoff(a, load(dev, customers, n), customers)
                slack = own - value
                assert slack >= 0, (history, a, slack)
                comparisons += 1
                minimum = slack if minimum is None else min(minimum, slack)
    actual = finish(())
    actual_loads = load(actual, customers, n)
    utilities = [payoff(a, actual_loads, customers) for a in actual]
    p = [Q(0), Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2)]
    positions = []
    for i in range(m - 1):
        prefix = actual[:i]
        branch = {a: finish(prefix + (a,)) for a in range(k)}
        b = load(prefix, customers, n)
        middle = {a: branch[a][i + 1:-1] for a in range(k)}
        last = {a: branch[a][-1] for a in range(k)}
        record = decompose(customers, b, middle, last, p)
        assert record["last_pair_min"] >= 0
        record["actual_utility"] = utilities[i]
        record["current_IC"] = utilities[i] - record["D"]
        record["free_query_price"] = min(
            sum((p[t] * sum((Q(1, load(branch[a], customers, n)[x] + 1)
                               for x in customers[t]), Q(0)) for t in range(k)), Q(0))
            for a in range(k))
        record["free_column_gain"] = record["C_extra"] - record["free_query_price"]
        positions.append(record)
    return {"unit_customers": n, "ordered_nodes": 43, "comparisons": comparisons,
            "minimum_IC_slack": minimum, "actual": actual, "utilities": utilities,
            "W": sum(utilities), "query_p": p, "positions": positions,
            "scope": "Re-decomposition of existing 36-customer complete SPE, not a new counterexample"}


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: serial(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(val) for val in value]
    return value


if __name__ == "__main__":
    print(json.dumps(serial({"algebra": random_identity_trials(),
                             "existing_complete_SPE": thirty_six_unit_replay()}),
                     ensure_ascii=False, indent=2))
