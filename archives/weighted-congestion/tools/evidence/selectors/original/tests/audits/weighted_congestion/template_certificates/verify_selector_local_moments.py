#!/usr/bin/env python3
"""Exact finite implementation audit; no claim of a universal existence test."""
from fractions import Fraction
from itertools import product, combinations
from math import comb
from pathlib import Path
import hashlib
import json
import platform


def subsets(items, cap=None):
    items = tuple(items)
    for r in range(len(items) + 1 if cap is None else min(cap, len(items)) + 1):
        yield from combinations(items, r)


def signatures(action_counts, proper):
    choices = [range((1 << m) - int(proper)) for m in action_counts]
    for sig in product(*choices):
        if any(sig):
            yield sig


def uses(sig, i, action):
    return bool(sig[i] & (1 << action))


def cost(sig, degree, weights, state, i):
    if not uses(sig, i, state[i]):
        return 0
    load = sum(w for j, w in enumerate(weights) if uses(sig, j, state[j]))
    return load ** degree


def theta(weights, i, degree, context):
    return sum((-1) ** (len(context) - len(r))
               * (weights[i] + sum(weights[j] for j in r)) ** degree
               for r in subsets(context))


def audit_mobius():
    weights = (1, 3, 7, 11)
    checks = 0
    for i in range(len(weights)):
        others = tuple(j for j in range(len(weights)) if j != i)
        for degree in range(6):
            ts = {t: theta(weights, i, degree, t) for t in subsets(others)}
            for t, value in ts.items():
                assert (value > 0) if len(t) <= degree else (value == 0)
            for bits in product((0, 1), repeat=len(others)):
                z = dict(zip(others, bits))
                lhs = (weights[i] + sum(weights[j] * z[j] for j in others)) ** degree
                rhs = sum(v for t, v in ts.items() if all(z[j] for j in t))
                assert lhs == rhs
                checks += 1
    return {"weights": weights, "degree_range": [0, 5], "identities": checks}


def parity_selector(state):
    active = list(state[:-1])
    flag = state[-1]
    if flag == 0:
        mover = 0 if sum(active) % 2 == 0 else len(active)
    else:
        mover = next((j for j in range(1, len(active)) if active[j]), 0)
    target = list(state)
    target[mover] ^= 1
    return mover, tuple(target)


def recurrent_states(states, successors):
    result = set()
    for state in states:
        seen = {}
        trajectory = []
        while state not in seen:
            seen[state] = len(trajectory)
            trajectory.append(state)
            state = successors[state]
        result.update(trajectory[seen[state]:])
    return result


def audit_parity(degree, proper):
    active_count = degree + 2
    n = active_count + 1
    weights = tuple((j + 1) ** 2 + 1 for j in range(n))
    states = tuple(product((0, 1), repeat=n))
    successors = {}
    for s in states:
        mover, target = parity_selector(s)
        assert sum(a != b for a, b in zip(s, target)) == 1
        assert s[mover] != target[mover]
        successors[s] = target
    rec = recurrent_states(states, successors)
    q = (0,) * active_count + (1,)
    qp = (1,) + (0,) * (active_count - 1) + (1,)
    assert rec == {q, qp}
    support = tuple(s for s in states if s[-1] == 0 and sum(s[:-1]) % 2 == 0)
    assert len(support) == 2 ** (active_count - 1)
    assert not rec.intersection(support)
    assert all(parity_selector(s)[0] == 0 for s in support)
    assert {successors[s] for s in support} == {
        s for s in states if s[-1] == 0 and sum(s[:-1]) % 2 == 1}
    count = 0
    digest = hashlib.sha256()
    max_total = 0
    for sig in signatures((2,) * n, proper=proper):
        if proper:
            assert all(mask != 3 for mask in sig)
        for k in range(degree + 1):
            current = sum(cost(sig, k, weights, s, 0) for s in support)
            arrival = sum(cost(sig, k, weights, successors[s], 0) for s in support)
            assert current == arrival
            assert 2 * current - 3 * arrival <= 0
            max_total = max(max_total, current)
            digest.update(f"{sig}:{k}:{current}:{arrival}\n".encode())
            count += 1
    expected = ((3 if proper else 4) ** n - 1) * (degree + 1)
    assert count == expected
    return {
        "degree": degree, "proper_core_signatures": proper,
        "weights": weights, "players": n, "states": len(states),
        "dual_support_size": len(support), "dual_support_all_transient": True,
        "self_edges": 0, "recurrent_cycle": [q, qp],
        "columns": count, "alpha_checked": ["1", "3/2"],
        "all_alpha_1_column_products_exactly_zero": True,
        "max_unnormalized_current_cost_total": max_total,
        "column_totals_sha256": digest.hexdigest(),
    }


def first_column_dependence(vectors):
    """Return exact coefficients beta with sum beta_j vectors_j == 0, or None."""
    basis = {}
    q = len(vectors)
    for j, original in enumerate(vectors):
        v = [Fraction(x) for x in original]
        coeff = [Fraction(int(k == j)) for k in range(q)]
        for pivot in sorted(basis):
            if v[pivot]:
                factor = v[pivot]
                bv, bc = basis[pivot]
                v = [a - factor * b for a, b in zip(v, bv)]
                coeff = [a - factor * b for a, b in zip(coeff, bc)]
        pivot = next((r for r, value in enumerate(v) if value), None)
        if pivot is None:
            assert any(coeff)
            assert all(sum(coeff[k] * vectors[k][r] for k in range(q)) == 0
                       for r in range(len(original)))
            return coeff
        factor = v[pivot]
        basis[pivot] = ([x / factor for x in v], [x / factor for x in coeff])
    return None


def exact_column_rank(vectors):
    basis = {}
    for original in vectors:
        v = list(map(Fraction, original))
        for pivot in sorted(basis):
            if v[pivot]:
                factor = v[pivot]
                v = [a - factor * b for a, b in zip(v, basis[pivot])]
        pivot = next((r for r, value in enumerate(v) if value), None)
        if pivot is not None:
            factor = v[pivot]
            basis[pivot] = [x / factor for x in v]
    return len(basis)


def dimension_bound(action_counts, degree):
    n = len(action_counts)
    return sum(action_counts[i] * sum(
        product_int(action_counts[j] - 1 for j in t)
        for t in subsets((j for j in range(n) if j != i), degree))
        for i in range(n))


def product_int(items):
    result = 1
    for value in items:
        result *= value
    return result


def audit_compression(action_counts, weights, degree):
    n = len(action_counts)
    states = tuple(product(*(range(m) for m in action_counts)))
    types = tuple((sig, k) for sig in signatures(action_counts, True)
                  for k in range(degree + 1))
    vectors = [tuple(cost(sig, k, weights, s, i)
                     for s in states for i in range(n)) for sig, k in types]
    d_bound = dimension_bound(action_counts, degree)
    rank = exact_column_rank(vectors)
    assert rank <= d_bound
    old_coefficients = [Fraction(1 + j % 3) for j in range(len(types))]
    original_table = [sum(a * v[r] for a, v in zip(old_coefficients, vectors))
                      for r in range(n * len(states))]
    active = list(range(len(types)))
    coefficients = old_coefficients[:]
    eliminations = 0
    while True:
        relation = first_column_dependence([vectors[j] for j in active])
        if relation is None:
            break
        assert any(x > 0 for x in relation) and any(x < 0 for x in relation)
        step = min(coefficients[j] / beta for j, beta in zip(active, relation) if beta > 0)
        for j, beta in zip(active, relation):
            coefficients[j] -= step * beta
            assert coefficients[j] >= 0
        active = [j for j in active if coefficients[j]]
        eliminations += 1
    assert len(active) <= rank <= d_bound
    new_table = [sum(coefficients[j] * vectors[j][r] for j in active)
                 for r in range(n * len(states))]
    assert original_table == new_table
    # Retain selected signatures, then add distinct zero-cost singleton resources.
    selected_signatures = [types[j][0] for j in active]
    for i, m in enumerate(action_counts):
        for a in range(m):
            sig = [0] * n
            sig[i] = 1 << a
            selected_signatures.append(tuple(sig))
    for i, m in enumerate(action_counts):
        strategies = [set(r for r, sig in enumerate(selected_signatures) if uses(sig, i, a))
                      for a in range(m)]
        assert all(strategies)
        assert not set.intersection(*strategies)
        assert all(not (a <= b) for j, a in enumerate(strategies)
                   for k, b in enumerate(strategies) if j != k)
    digest = hashlib.sha256()
    for j in active:
        digest.update(f"{types[j]}:{coefficients[j]}\n".encode())
    return {
        "action_counts": action_counts, "weights": weights, "degree": degree,
        "states": len(states), "original_positive_monomial_types": len(types),
        "D_bound": d_bound, "exact_column_rank": rank,
        "compressed_positive_monomial_types": len(active),
        "zero_singleton_resources_added": sum(action_counts),
        "conic_elimination_steps": eliminations,
        "all_player_cost_table_entries_preserved": len(new_table),
        "compressed_game_is_nonempty_antichain_empty_intersection_core": True,
        "compressed_coefficients_sha256": digest.hexdigest(),
    }


def main():
    result = {
        "audit_scope": "Finite exact implementation audit of three proposed structural claims; no uniform existence conclusion.",
        "python": platform.python_version(), "arithmetic": "Python integers and fractions.Fraction; no numerical tolerances",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_note_sha256": 'f4541469f8aadbb57037b10e1248ed6b1db24d493e31d0d1974c0f85bb6aecbe',
        "mobius_expansion": audit_mobius(),
        "transient_parity": [audit_parity(d, True) for d in range(5)]
                            + [audit_parity(d, False) for d in range(4)],
        "cost_compression": [audit_compression((2, 2, 2), (1, 3, 5), 1),
                             audit_compression((2, 2, 2), (1, 3, 5), 2),
                             audit_compression((3, 3), (2, 7), 1)],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
