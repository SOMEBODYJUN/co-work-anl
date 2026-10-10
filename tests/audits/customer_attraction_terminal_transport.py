#!/usr/bin/env python3
"""Exact, independent audit of CA-TERMINAL-REPLY-DUAL-LIFT.

No model/solver/LP imports, no random search. Identities are checked in every
nonempty customer-type column of one complete formal strategy, not only the
three populated types of its equilibrium instance.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def member(a, mask):
    return int(bool(mask & (1 << a)))


def counts(history, topics):
    return tuple(history.count(a) for a in range(topics))


def deviation_rank(sigma, history):
    return sum(a != sigma[history[:i]] for i, a in enumerate(history))


def run(sigma, history, n):
    z = tuple(history)
    while len(z) < n:
        z += (sigma[z],)
    return z


def own_coeff(z, position, mask):
    numerator = member(z[position], mask)
    return F(numerator, sum(member(a, mask) for a in z)) if numerator else F(0)


def cover_coeff(z, mask):
    return F(int(any(member(a, mask) for a in z)))


def row(sigma, history, action, n, masks):
    position = len(history)
    source = run(sigma, history, n)
    target = run(sigma, history + (action,), n)
    return tuple(own_coeff(source, position, t) - own_coeff(target, position, t)
                 for t in masks)


def dot(vector, masks, masses):
    return sum((x * masses.get(t, 0) for x, t in zip(vector, masks)), F(0))


def add(*vectors):
    return tuple(sum(items, F(0)) for items in zip(*vectors))


def scale(factor, vector):
    return tuple(factor * x for x in vector)


def delta(leaf, action, old, new, masks):
    assert action in leaf
    out = []
    for t in masks:
        p = sum(member(a, t) for a in leaf)
        numerator = member(action, t) * (member(old, t) - member(new, t))
        out.append(F(numerator, p * (p + 1)) if numerator else F(0))
    return tuple(out)


def all_histories(topics, n):
    return [h for length in range(n) for h in product(range(topics), repeat=length)]


def audit_scalar_identities():
    checks = 0
    for p in list(range(33)) + [10**6]:
        for a, b in product(range(2), repeat=2):
            own_change = F(b - a, p + 1)
            incumbent_change = F(a - b, p + 1) if p else F(0)
            coverage_change = F(b - a) if not p else F(0)
            assert coverage_change == own_change + incumbent_change
            if p:
                individual_change = F(1, p + b) - F(1, p + a)
                assert individual_change == F(a - b, p * (p + 1))
                assert p * individual_change == incumbent_change
                assert abs(incumbent_change) <= F(1, p + 1)
                assert F(1, p + 1) <= F(1, 2)
                old_income = F(1, p + a)
                assert max(-individual_change, F(0)) <= old_income / 2
                assert max(individual_change, F(0)) <= old_income
            checks += 1
    return checks


def audit_normalization():
    topics, n = 3, 3
    masks = list(range(1, 1 << topics))
    histories = all_histories(topics, n)
    leaves = [h for h in histories if len(h) == n - 1]
    sigma = {(): 2, (0,): 2, (1,): 1, (2,): 0}
    replies = [2, 2, 1, 2, 2, 2, 2, 1, 1]
    sigma.update(dict(zip(leaves, replies)))
    masses = {3: 1, 6: 1, 4: 1}
    original_terminal = run(sigma, (), n)
    assert original_terminal == (2, 0, 2)
    original_rows = {(h, a): row(sigma, h, a, n, masks)
                     for h in histories for a in range(topics)}
    assert len(original_rows) == 39
    assert all(dot(v, masks, masses) >= 0 for v in original_rows.values())
    assert [dot(tuple(own_coeff(original_terminal, i, t) for t in masks),
                masks, masses) for i in range(n)] == [F(1)] * 3

    representatives = {}
    for leaf in leaves:
        representatives.setdefault(counts(leaf, topics), leaf)
    root_leaf = original_terminal[:-1]
    representatives[counts(root_leaf, topics)] = root_leaf
    normalized = dict(sigma)
    for leaf in leaves:
        normalized[leaf] = sigma[representatives[counts(leaf, topics)]]
    assert run(normalized, (), n) == original_terminal
    canonical_rows = {(h, a): row(normalized, h, a, n, masks)
                      for h in histories for a in range(topics)}
    negatives = {(h, a): dot(v, masks, masses)
                 for (h, a), v in canonical_rows.items()
                 if dot(v, masks, masses) < 0}
    assert negatives == {((2,), 1): F(-1, 3)}

    deltas = {(leaf, a): delta(leaf, a, sigma[leaf], normalized[leaf], masks)
              for leaf in leaves for a in set(leaf)}
    for (leaf, a), v in deltas.items():
        if leaf == representatives[counts(leaf, topics)]:
            assert all(x == 0 for x in v)

    checks, gauge_checks, rank_checks = 0, 0, 0
    for (h, a), original in original_rows.items():
        if len(h) < n - 1:
            source_leaf = run(sigma, h, n)[:-1]
            target_leaf = run(sigma, h + (a,), n)[:-1]
            predicted = add(original, deltas[source_leaf, sigma[h]],
                            scale(-1, deltas[target_leaf, a]))
            assert deviation_rank(sigma, source_leaf) == deviation_rank(sigma, h)
            assert deviation_rank(sigma, target_leaf) == (
                deviation_rank(sigma, h) + int(a != sigma[h]))
            rank_checks += 1
        else:
            reference = representatives[counts(h, topics)]
            predicted = add(original, original_rows[reference, sigma[h]])
            gauge = add(original_rows[h, sigma[reference]],
                        original_rows[reference, sigma[h]])
            assert all(x == 0 for x in gauge)
            gauge_checks += len(masks)
        assert canonical_rows[h, a] == predicted
        checks += len(masks)

    # Verify every incumbent delta and the aggregate terminal coverage identity.
    incumbent_checks = 0
    for leaf in leaves:
        old_terminal = leaf + (sigma[leaf],)
        new_terminal = leaf + (normalized[leaf],)
        for i, a in enumerate(leaf):
            actual_change = tuple(own_coeff(new_terminal, i, t)
                                  - own_coeff(old_terminal, i, t) for t in masks)
            assert actual_change == deltas[leaf, a]
            incumbent_checks += len(masks)
        coverage_change = tuple(cover_coeff(new_terminal, t)
                                - cover_coeff(old_terminal, t) for t in masks)
        last_change = tuple(own_coeff(new_terminal, n - 1, t)
                            - own_coeff(old_terminal, n - 1, t) for t in masks)
        prior_change = add(*(deltas[leaf, a] for a in leaf))
        assert coverage_change == add(last_change, prior_change)

    # Explicit nonnegative lifting, with general individually weighted rows.
    weights = {key: F(index + 1, 7)
               for index, key in enumerate(original_rows)}
    lifted = defaultdict(F)
    incidence = defaultdict(F)
    zero = (F(0),) * len(masks)
    correction = zero
    canonical_sum = zero
    for (h, a), weight in weights.items():
        canonical_sum = add(canonical_sum, scale(weight, canonical_rows[h, a]))
        lifted[h, a] += weight
        if len(h) < n - 1:
            source = (run(sigma, h, n)[:-1], sigma[h])
            target = (run(sigma, h + (a,), n)[:-1], a)
            incidence[source] += weight
            incidence[target] -= weight
            correction = add(correction, scale(weight, deltas[source]),
                             scale(-weight, deltas[target]))
        else:
            reference = representatives[counts(h, topics)]
            lifted[reference, sigma[h]] += weight
    assert all(x >= 0 for x in lifted.values())
    true_sum = zero
    for key, weight in lifted.items():
        true_sum = add(true_sum, scale(weight, original_rows[key]))
    assert canonical_sum == add(true_sum, correction)
    incidence_sum = zero
    for key, net in incidence.items():
        incidence_sum = add(incidence_sum, scale(net, deltas[key]))
    assert correction == incidence_sum

    # The exact negative correction at the concrete offending early deviation.
    key = ((2,), 1)
    critical_correction = add(canonical_rows[key], scale(-1, original_rows[key]))
    assert dot(original_rows[key], masks, masses) == F(1, 6)
    assert dot(critical_correction, masks, masses) == F(-1, 2)
    critical_target_income = dot(
        tuple(own_coeff(run(sigma, (2, 1), n), 1, t) for t in masks),
        masks, masses)
    assert critical_target_income == F(5, 6)
    assert F(1, 2) > critical_target_income / 2
    return {
        "nodes": len(histories), "comparisons": len(original_rows),
        "type_columns": len(masks), "row_transform_column_checks": checks,
        "reciprocal_gauge_column_checks": gauge_checks,
        "incumbent_column_checks": incumbent_checks,
        "deviation_rank_edge_checks": rank_checks,
        "root_terminal_preserved": list(original_terminal),
        "normalized_negative_rows": [
            {"history": list(h), "action": a, "slack": str(v)}
            for (h, a), v in negatives.items()],
        "critical_original_slack": "1/6",
        "critical_transfer_correction": "-1/2",
        "critical_normalized_slack": "-1/3",
        "general_lifting_identity_exact": True,
        "incidence_tensor_identity_exact": True,
        "general_lifting_correction_by_type": {
            str(t): str(x) for t, x in zip(masks, correction)},
        "note": "Negative corrections are retained; this is not a half-cover certificate."
    }


def audit_sharp_ties():
    out = []
    for m in [1, 7, 101]:
        n, topics = 2, 2
        masks = [1, 2, 3]
        masses = {1: 2 * m, 2: m}
        poor = {(): 0, (0,): 0, (1,): 0}
        rich = {(): 0, (0,): 1, (1,): 0}
        for sigma in [poor, rich]:
            for h in all_histories(topics, n):
                for a in range(topics):
                    assert dot(row(sigma, h, a, n, masks), masks, masses) >= 0
        poor_z, rich_z = run(poor, (), n), run(rich, (), n)
        welfare = [dot(tuple(cover_coeff(z, t) for t in masks), masks, masses)
                   for z in [poor_z, rich_z]]
        last_profit = [dot(tuple(own_coeff(z, 1, t) for t in masks), masks, masses)
                       for z in [poor_z, rich_z]]
        assert welfare == [2 * m, 3 * m]
        assert last_profit == [m, m]
        # Security primal: pure A. Security dual: fixed opponent A.
        query_vs_opponent = [[dot(tuple(own_coeff((a, b), 0, t) for t in masks),
                                 masks, masses) for b in range(topics)]
                             for a in range(topics)]
        assert min(query_vs_opponent[0]) == m
        assert max(query_vs_opponent[a][0] for a in range(topics)) == m
        cap = sum(F(masses.get(t, 0), 2) for t in masks if member(0, t))
        assert welfare[1] - welfare[0] == cap == m
        assert welfare[1] - welfare[0] > F(m, 2)
        out.append({"m": m, "poor_welfare": 2 * m, "rich_welfare": 3 * m,
                    "last_profit": m, "security_value": m,
                    "coverage_transfer": m, "prefix_half_cap": m})
    return out


def main():
    result = {"status": "exact identities verified; universal half-cover remains open",
              "scalar_identity_checks": audit_scalar_identities(),
              "normalization": audit_normalization(),
              "sharp_tie_examples": audit_sharp_ties()}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Exclusively create a new JSON report")
    args = parser.parse_args()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
