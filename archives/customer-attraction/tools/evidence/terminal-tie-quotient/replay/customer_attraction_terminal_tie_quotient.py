#!/usr/bin/env python3
"""Exact audit of terminal reciprocal-row quotient transport.

Reconstructs complete ordered-history strategies directly. No model, solver,
optimizer, or other audit is imported. Finite checks audit the algebra and the
stated examples; they do not establish universal half coverage.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def hit(action, mask):
    return int(bool(mask & (1 << action)))


def histories(m, n):
    return [h for j in range(n) for h in product(range(m), repeat=j)]


def run(sigma, h, n):
    z = tuple(h)
    while len(z) < n:
        z += (sigma[z],)
    return z


def income(z, i, t):
    return F(1, sum(hit(a, t) for a in z)) if hit(z[i], t) else F(0)


def row(sigma, h, a, n, masks):
    old, new = run(sigma, h, n), run(sigma, h + (a,), n)
    return tuple(income(old, len(h), t) - income(new, len(h), t)
                 for t in masks)


def add(*vs):
    return tuple(sum(xs, F(0)) for xs in zip(*vs))


def scale(k, v):
    return tuple(k * x for x in v)


def dot(v, masks, w):
    return sum((x * w.get(t, 0) for x, t in zip(v, masks)), F(0))


def qcount(h, m):
    return tuple(h.count(a) for a in range(m))


def normalize(sigma, m, n):
    leaves = list(product(range(m), repeat=n - 1))
    reps = {}
    for leaf in leaves:
        reps.setdefault(qcount(leaf, m), leaf)
    root_leaf = run(sigma, (), n)[:-1]
    reps[qcount(root_leaf, m)] = root_leaf
    bar = dict(sigma)
    for leaf in leaves:
        bar[leaf] = sigma[reps[qcount(leaf, m)]]
    return bar, reps


def delta(leaf, action, old, new, masks):
    assert action in leaf
    out = []
    for t in masks:
        p = sum(hit(a, t) for a in leaf)
        numerator = hit(action, t) * (hit(old, t) - hit(new, t))
        out.append(F(numerator, p * (p + 1)) if numerator else F(0))
    return tuple(out)


def transport(sigma, bar, weights, m, n, masks, reps):
    """Lift each normalized row separately and return its exact error."""
    zero = (F(0),) * len(masks)
    error, incidence, lifted = zero, defaultdict(F), defaultdict(F)
    for (h, a), weight in weights.items():
        assert weight >= 0
        lifted[h, a] += weight
        if len(h) == n - 1:
            lifted[reps[qcount(h, m)], sigma[h]] += weight
            continue
        old_leaf = run(sigma, h, n)[:-1]
        dev_leaf = run(sigma, h + (a,), n)[:-1]
        incoming = (old_leaf, sigma[h])
        outgoing = (dev_leaf, a)
        incidence[incoming] += weight
        incidence[outgoing] -= weight
        old_delta = delta(old_leaf, sigma[h], sigma[old_leaf], bar[old_leaf], masks)
        dev_delta = delta(dev_leaf, a, sigma[dev_leaf], bar[dev_leaf], masks)
        error = add(error, scale(weight, old_delta), scale(-weight, dev_delta))
    normalized_sum = zero
    true_sum = zero
    for key, weight in weights.items():
        normalized_sum = add(normalized_sum, scale(weight, row(bar, *key, n, masks)))
    for key, weight in lifted.items():
        true_sum = add(true_sum, scale(weight, row(sigma, *key, n, masks)))
    assert normalized_sum == add(true_sum, error)
    # Split every incidence into its common q-proportional part and a
    # zero-total incumbent redistribution. This includes p=0 columns.
    split_error = zero
    for leaf in product(range(m), repeat=n - 1):
        q = qcount(leaf, m)
        common = sum((incidence[leaf, s] for s in set(leaf)), F(0)) / (n - 1)
        balanced = {s: incidence[leaf, s] - common * q[s] for s in set(leaf)}
        assert sum(balanced.values(), F(0)) == 0
        reciprocal = row(sigma, leaf, bar[leaf], n, masks)
        uncovered = tuple(reciprocal[i] if not sum(hit(a, t) for a in leaf)
                          else F(0) for i, t in enumerate(masks))
        split_error = add(split_error, scale(common, reciprocal),
                          scale(-common, uncovered))
        for s, net in balanced.items():
            split_error = add(split_error, scale(net, delta(
                leaf, s, sigma[leaf], bar[leaf], masks)))
    assert error == split_error
    return error, incidence, lifted


def signed_tie_payment(sigma, leaf, representative, coefficient, n, masks):
    """Express coefficient times the reciprocal row by nonnegative true rows."""
    forward = row(sigma, leaf, sigma[representative], n, masks)
    reverse = row(sigma, representative, sigma[leaf], n, masks)
    assert forward == scale(-1, reverse)
    key = (leaf, sigma[representative]) if coefficient >= 0 else (
        representative, sigma[leaf])
    weight = abs(coefficient)
    assert scale(coefficient, forward) == scale(weight, row(sigma, *key, n, masks))
    return key, weight, scale(coefficient, forward)


def three_player_strategy():
    sigma = {(): 2, (0,): 2, (1,): 1, (2,): 0}
    sigma.update(dict(zip(product(range(3), repeat=2),
                          [2, 2, 1, 2, 2, 2, 2, 1, 1])))
    return sigma


def audit_natural_target():
    m, n = 3, 3
    masks = list(range(1, 1 << m))
    sigma = three_player_strategy()
    bar, reps = normalize(sigma, m, n)
    masses = {3: 1, 4: 1, 6: 1}
    keys = [(h, a) for h in histories(m, n) for a in range(m)]
    assert len(keys) == 39
    assert all(dot(row(sigma, *key, n, masks), masks, masses) >= 0 for key in keys)
    z = run(sigma, (), n)
    assert z == (2, 0, 2)
    # Comparison tuple (A,B,C) covers every nonempty customer-interest type.
    target = tuple(F(2 * int(any(hit(a, t) for a in z)) - 1) for t in masks)
    weights = {((0,), 0): F(2), ((2,), 1): F(1), ((2,), 2): F(1)}
    error, _, lifted = transport(sigma, bar, weights, m, n, masks, reps)
    bar_sum = add(*(scale(k, row(bar, *key, n, masks)) for key, k in weights.items()))
    remainder = add(target, scale(-1, bar_sum))
    assert remainder == tuple(map(F, [0, 0, 1, F(1, 2), F(5, 6), F(2, 3), 1]))
    assert all(x >= 0 for x in remainder)
    raw = add(remainder, error)
    assert raw == tuple(map(F, [0, F(-1, 2), F(1, 2), F(-1, 2), F(1, 2), F(2, 3), 1]))
    assert min(raw) < 0
    gauge = (F(0),) * len(masks)
    for leaf, representative, coefficient in [((0, 2), (2, 0), F(-2)),
                                               ((2, 1), (1, 2), F(3))]:
        key, k, payment = signed_tie_payment(sigma, leaf, representative,
                                             coefficient, n, masks)
        lifted[key] += k
        gauge = add(gauge, payment)
    final_remainder = add(raw, scale(-1, gauge))
    assert final_remainder == tuple(map(F, [0, 0, 0, 0, F(4, 3), F(2, 3), 1]))
    assert all(x >= 0 for x in final_remainder)
    original_sum = add(*(scale(k, row(sigma, *key, n, masks))
                         for key, k in lifted.items()))
    assert target == add(original_sum, final_remainder)
    # A single negative error cannot be erased even by all original rows:
    # its scalar product with a fully verified original SPE is strictly negative.
    critical = {((2,), 1): F(1)}
    bad_error, _, _ = transport(sigma, bar, critical, m, n, masks, reps)
    assert dot(bad_error, masks, masses) == F(-1, 2)
    # Keeping an arbitrary valid normalized certificate's early weights fails
    # even for the same natural target. Any added true row has nonnegative
    # scalar product with this original SPE witness, so it cannot repair this.
    bad_weights = {((0,), 0): F(4), ((2,), 1): F(1), ((2,), 2): F(2)}
    bad_error, _, _ = transport(sigma, bar, bad_weights, m, n, masks, reps)
    bad_bar_sum = add(*(scale(k, row(bar, *key, n, masks))
                        for key, k in bad_weights.items()))
    bad_remainder = add(target, scale(-1, bad_bar_sum))
    assert bad_remainder == tuple(map(F, [0, 0, 1, 0, 1, 0, 1]))
    assert all(x >= 0 for x in bad_remainder)
    bad_raw = add(bad_remainder, bad_error)
    assert bad_raw == tuple(map(F, [0, F(-1, 2), F(1, 2), -2, F(1, 3), 0, 1]))
    assert dot(bad_raw, masks, masses) == F(-3, 2)
    return {"nodes": len(sigma), "comparisons": len(keys), "type_columns": len(masks),
            "natural_target": [str(x) for x in target],
            "normalized_remainder": [str(x) for x in remainder],
            "raw_lift_remainder": [str(x) for x in raw],
            "quotient_remainder": [str(x) for x in final_remainder],
            "single_error_full_cone_separator": "-1/2",
            "bad_natural_target_normalized_remainder": [str(x) for x in bad_remainder],
            "bad_natural_target_raw_remainder": [str(x) for x in bad_raw],
            "bad_natural_target_full_cone_separator": "-3/2",
            "natural_target_original_nonnegative_identity": True}


def audit_four_edge_cancellation():
    m, n = 3, 4
    masks = list(range(1, 1 << m))
    sigma = {h: 2 for h in histories(m, n)}
    sigma.update({(0,): 0, (0, 0): 2, (0, 2): 1,
                  (1,): 1, (1, 1): 2, (1, 0): 2,
                  (0, 2, 1): 0, (1, 0, 2): 1})
    bar, reps = normalize(sigma, m, n)
    assert [h for h in sigma if sigma[h] != bar[h]] == [(0, 2, 1), (1, 0, 2)]
    weights = {((0,), 2): F(1), ((0, 2), 0): F(1),
               ((1,), 0): F(1), ((1, 0), 1): F(1)}
    error, incidence, _ = transport(sigma, bar, weights, m, n, masks, reps)
    assert all(x == 0 for x in error)
    first = tuple(incidence[(0, 2, 1), a] for a in range(m))
    second = tuple(incidence[(1, 0, 2), a] for a in range(m))
    assert first == (F(0), F(1), F(-1))
    assert second == (F(-1), F(0), F(1))
    assert len(set(first)) > 1 and len(set(second)) > 1
    # Audit every normalized-row transform, rather than only the four rows.
    checks = 0
    for h in histories(m, n):
        for a in range(m):
            transport(sigma, bar, {(h, a): F(1)}, m, n, masks, reps)
            checks += len(masks)
    return {"nodes": len(sigma), "row_transform_column_checks": checks,
            "changed_leaf_incidence": [list(map(str, first)), list(map(str, second))],
            "four_real_rows_zero_error": True, "uniform_incidence": False}


def audit_cross_count_payment():
    m, n = 2, 4
    masks = list(range(1, 1 << m))
    sigma = {h: 1 for h in histories(m, n)}
    sigma.update({(0, 1, 0): 0, (1, 0, 1): 0})
    bar, reps = normalize(sigma, m, n)
    error, _, lifted = transport(sigma, bar, {((0, 1), 0): F(1)}, m, n, masks, reps)
    assert error == (F(-1, 6), F(0), F(0))
    gauge = (F(0),) * len(masks)
    for leaf, representative, coefficient in [((0, 1, 0), (0, 0, 1), F(2, 5)),
                                               ((1, 0, 1), (0, 1, 1), F(-3, 5))]:
        key, k, payment = signed_tie_payment(sigma, leaf, representative,
                                             coefficient, n, masks)
        lifted[key] += k
        gauge = add(gauge, payment)
    assert error == gauge
    # This first count's sole reciprocal row has a nonzero B-only coordinate;
    # therefore its span cannot contain the error, whose B-only coordinate is 0.
    r1 = row(sigma, (0, 1, 0), 1, n, masks)
    assert r1 == (F(1, 3), F(-1, 2), F(0))
    assert error[0] != 0 and error[1] == 0 and r1[1] != 0
    final = add(*(scale(k, row(sigma, *key, n, masks)) for key, k in lifted.items()))
    assert final == row(bar, (0, 1), 0, n, masks)
    return {"type_columns": len(masks), "error": [str(x) for x in error],
            "cross_count_coefficients": ["2/5", "-3/5"],
            "single_count_membership": False, "global_reciprocal_payment": True}


def local_coefficient_condition(q, b, K, eta):
    m = len(q)
    if sum(eta) != 0 or any(eta[i] and not q[i] for i in range(m)):
        return False
    for i in range(m):
        linear = sum((K.get((a, i), 0) * (int(a == i) - int(b == i))
                      for a in range(m)), F(0))
        if linear != q[i] * eta[i]:
            return False
        for j in range(i + 1, m):
            pair = sum((K.get((a, i), 0) * (int(a == j) - int(b == j))
                        + K.get((a, j), 0) * (int(a == i) - int(b == i))
                        for a in range(m)), F(0))
            if pair != q[i] * eta[j] + q[j] * eta[i]:
                return False
    return True


def local_type_condition(q, b, K, eta):
    m = len(q)
    for t in range(1, 1 << m):
        p = sum(q[i] * hit(i, t) for i in range(m))
        N = sum((K.get((a, i), 0) * hit(i, t) * (hit(a, t) - hit(b, t))
                 for a in range(m) for i in range(m)), F(0))
        error = F(N, p * (p + 1)) if p else F(0)
        reciprocal = F(sum(eta[i] * hit(i, t) for i in range(m)), p + 1)
        if error != reciprocal:
            return False
    return True


def audit_quadratic_characterization():
    checks = 0
    for q in [(1, 1, 1), (1, 2, 0), (0, 1, 2)]:
        slots = [(a, i) for a in (0, 1) for i in range(3) if q[i]]
        for entries in product((-1, 0, 1), repeat=len(slots)):
            K = dict(zip(slots, entries))
            for ea, eb in product((-1, 0, 1), repeat=2):
                eta = (ea, eb, -ea - eb)
                assert local_coefficient_condition(q, 2, K, eta) == (
                    local_type_condition(q, 2, K, eta))
                checks += 1
    # The polynomial identity N=pJ alone misses the p=0 column.
    q, K, eta = (1, 0), {(0, 0): 1}, (1, -1)
    for t in range(1, 4):
        p = hit(0, t)
        assert hit(0, t) * (hit(0, t) - hit(1, t)) == (
            p * (eta[0] * hit(0, t) + eta[1] * hit(1, t)))
    assert not local_type_condition(q, 1, K, eta)
    assert not local_coefficient_condition(q, 1, K, eta)
    return {"coefficient_vs_all_type_equivalence_checks": checks,
            "zero_prefix_load_missing_constraint_detected": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"claim": "CA-TERMINAL-TIE-QUOTIENT-LIFT",
              "arithmetic": "fractions.Fraction", "universal_half_coverage_proved": False,
              "natural_target": audit_natural_target(),
              "four_edge_cancellation": audit_four_edge_cancellation(),
              "cross_count_payment": audit_cross_count_payment(),
              "quadratic_characterization": audit_quadratic_characterization()}
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
